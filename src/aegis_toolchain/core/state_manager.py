"""StateManager — state.json 的并发安全读写"""

import json
from pathlib import Path
from typing import Optional

from filelock import FileLock, Timeout
from loguru import logger

from aegis_toolchain.models.state import AegisState, Requirement, RequirementLevel, RequirementPhase
from aegis_toolchain.utils.fs import atomic_write, ensure_dir


class StateCorruptedError(Exception):
    """state.json 数据损坏异常，附带修复建议"""

    def __init__(self, detail: str) -> None:
        self.detail = detail
        super().__init__(
            f"状态文件似乎被破坏了。{detail}\n"
            "建议: 1) 检查 Aegis/state/state.json 是否为合法 JSON\n"
            "       2) 或删除 state.json 后重新运行 aegis start"
        )


class StateManager:
    """state.json 管理器，提供线程/进程安全的 CRUD 操作"""

    LOCK_TIMEOUT = 2  # 秒（每次拿锁等待时间）
    SAVE_RETRIES = 5  # save 失败重试次数

    def __init__(self, project_path: Path) -> None:
        self.project_path = project_path
        self.state_dir = project_path / "Aegis" / "state"
        self.state_path = self.state_dir / "state.json"
        self.lock_path = self.state_dir / "state.json.lock"
        ensure_dir(self.state_dir)

    def load(self) -> AegisState:
        """加载 state.json，文件不存在时返回默认空状态"""
        lock = FileLock(str(self.lock_path), timeout=self.LOCK_TIMEOUT)

        try:
            with lock.acquire(timeout=self.LOCK_TIMEOUT):
                return self._load_unlocked()
        except Timeout:
            logger.warning("filelock 获取超时，重试一次")
            try:
                with lock.acquire(timeout=self.LOCK_TIMEOUT * 2):
                    return self._load_unlocked()
            except Timeout:
                logger.error("filelock 重试仍超时，以无锁模式加载（可能读到不一致数据）")
                return self._load_unlocked()

    def _load_unlocked(self) -> AegisState:
        if not self.state_path.exists():
            return AegisState()

        try:
            raw = self.state_path.read_text(encoding="utf-8")
            data = json.loads(raw)
            return AegisState.model_validate(data)
        except json.JSONDecodeError as e:
            raise StateCorruptedError(f"JSON 格式错误 (行 {e.lineno}, 列 {e.colno}): {e.msg}")
        except Exception as e:
            raise StateCorruptedError(f"数据校验失败: {e}")

    def save(self, state: AegisState) -> None:
        """原子写入 state.json（临时文件 + rename，带重试）"""
        import time as _time

        for attempt in range(self.SAVE_RETRIES):
            lock = FileLock(str(self.lock_path), timeout=self.LOCK_TIMEOUT)
            try:
                with lock.acquire(timeout=self.LOCK_TIMEOUT):
                    json_str = state.model_dump_json(indent=2, ensure_ascii=False)
                    atomic_write(self.state_path, json_str + "\n")
                    return
            except Timeout:
                if attempt < self.SAVE_RETRIES - 1:
                    delay = 0.5 * (2 ** attempt)
                    logger.warning(f"filelock 获取超时，{delay}s 后重试 ({attempt + 1}/{self.SAVE_RETRIES})")
                    _time.sleep(delay)
                else:
                    logger.error("filelock 获取超时，state.json 未保存")
                    raise RuntimeError(
                        "状态文件被其他进程占用，重试 3 次仍超时。请稍后重试。"
                    )

    def get_active_requirement(self) -> Optional[Requirement]:
        """获取当前 implementing 的需求"""
        state = self.load()
        return state.find_implementing()

    def get_requirement(self, req_id: str) -> Optional[Requirement]:
        """按 ID 查找需求"""
        state = self.load()
        for r in state.active_requirements + state.completed_requirements:
            if r.id == req_id:
                return r
        return None

    def add_requirement(self, req: Requirement) -> Requirement:
        """新增需求，自动检查并发冲突并分配 ID"""
        state = self.load()

        # 并发检查
        if req.level != RequirementLevel.L1:
            implementing = state.find_implementing()
            if implementing is not None:
                raise RuntimeError(
                    f"需求 {implementing.id}（{implementing.title}）仍在 implementing 中。"
                    f"请先完成或暂停该需求后再开始新的。"
                )

        # 分配 ID
        req.id = state.get_next_id()

        # L2/L3 自动设初始阶段
        if req.level == RequirementLevel.L2:
            req.phase = RequirementPhase.DESIGN
        elif req.level == RequirementLevel.L3:
            req.phase = RequirementPhase.BRAINSTORM

        state.active_requirements.append(req)
        self.save(state)
        logger.info(f"新增需求: {req.id} [{req.level.value}] {req.title}")
        return req

    def update_requirement(self, req_id: str, **kwargs) -> None:
        """更新需求字段，支持 phase、boundary_checks、files_changed 等"""
        from datetime import datetime

        state = self.load()

        found = False
        for r in state.active_requirements + state.completed_requirements:
            if r.id == req_id:
                found = True
                if "phase" in kwargs:
                    r.phase = kwargs["phase"]
                if "boundary_checks" in kwargs:
                    for key, value in kwargs["boundary_checks"].items():
                        setattr(r.boundary_checks, key, value)
                if "files_changed" in kwargs:
                    r.files_changed = kwargs["files_changed"]
                if "devlog_written" in kwargs:
                    r.boundary_checks.devlog_written = kwargs["devlog_written"]
                r.last_activity = datetime.now()
                break

        if not found:
            logger.warning(f"update_requirement: 未找到 {req_id}")
            return

        self.save(state)
        logger.debug(f"更新需求: {req_id}")

    def get_next_id(self) -> str:
        """生成下一个需求 ID"""
        return self.load().get_next_id()
