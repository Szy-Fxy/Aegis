"""INDEX.md 表格的结构化读写"""

import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from loguru import logger


class IndexManager:
    """INDEX.md 的管理器，提供结构化增删改查"""

    def __init__(self, project_path: Path) -> None:
        self.path = project_path / "Aegis_Specs" / "INDEX.md"

    def read_all(self) -> list[dict[str, str]]:
        """解析 INDEX.md 表格，返回需求列表"""
        if not self.path.exists():
            return []

        content = self.path.read_text(encoding="utf-8")
        entries: list[dict[str, str]] = []

        # 匹配表格行: | REQ-001 | xxx | L2 | ✅ done | 2026-06-04 | 2026-06-04 |
        pattern = r"\|\s*(REQ-\d{3})\s*\|\s*(.+?)\s*\|\s*(L[123])\s*\|\s*(\S+(?:\s+\S+)*?)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|"
        for m in re.finditer(pattern, content):
            entries.append({
                "id": m.group(1),
                "title": m.group(2).strip(),
                "level": m.group(3),
                "status": m.group(4).strip(),
                "start_date": m.group(5),
                "last_activity": m.group(6),
            })

        return entries

    def add_entry(self, req_id: str, title: str, level: str, status: str) -> None:
        """在 INDEX.md 表格末尾新增一行"""
        today = datetime.now().strftime("%Y-%m-%d")
        safe_title = title.replace("|", "/").replace("\n", " ")

        if not self.path.exists():
            self._create_new(safe_title, req_id, level, status, today)
            return

        content = self.path.read_text(encoding="utf-8")

        # 找到表格最后一行数据，在后面插入
        lines = content.split("\n")
        insert_idx = -1
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip().startswith("|") and "REQ-" in lines[i]:
                insert_idx = i + 1
                break

        if insert_idx == -1:
            # 表格为空，在表头后插入
            for i, line in enumerate(lines):
                if "|---" in line:
                    insert_idx = i + 1
                    break

        if insert_idx == -1:
            logger.warning("无法定位 INDEX.md 表格位置，追加到文件末尾")
            insert_idx = len(lines)

        new_row = f"| {req_id} | {safe_title} | {level} | {status} | {today} | {today} |"
        lines.insert(insert_idx, new_row)
        self.path.write_text("\n".join(lines), encoding="utf-8")
        logger.info(f"INDEX.md: 新增 {req_id} — {safe_title}")

    def update_status(self, req_id: str, status: str) -> None:
        """更新指定需求的状态列和最后活动日期"""
        if not self.path.exists():
            logger.warning(f"INDEX.md 不存在，无法更新 {req_id}")
            return

        content = self.path.read_text(encoding="utf-8")
        today = datetime.now().strftime("%Y-%m-%d")

        # 匹配并替换状态列（第4列）和最后活动列（第6列）
        pattern = rf"(\|\s*{re.escape(req_id)}\s*\|.+?\|\s*L[123]\s*\|)\s*\S+(?:\s+\S+)*?(\s*\|\s*\d{{4}}-\d{{2}}-\d{{2}}\s*\|)\s*(\d{{4}}-\d{{2}}-\d{{2}})"
        replacement = rf"\1 {status} \2 {today}"

        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            self.path.write_text(new_content, encoding="utf-8")
            logger.info(f"INDEX.md: 更新 {req_id} 状态 → {status}")
        else:
            logger.warning(f"INDEX.md: 未找到 {req_id}，状态未更新")

    def find_entry(self, req_id: str) -> Optional[dict[str, str]]:
        """查找指定需求"""
        entries = self.read_all()
        for entry in entries:
            if entry["id"] == req_id:
                return entry
        return None

    def get_implementing_id(self) -> Optional[str]:
        """返回当前 implementing 的需求 ID"""
        entries = self.read_all()
        for entry in entries:
            if "implementing" in entry["status"].lower():
                return entry["id"]
        return None

    def _create_new(self, title: str, req_id: str, level: str, status: str, date: str) -> None:
        """创建全新的 INDEX.md"""
        template = f"""# 需求索引

> Aegis 项目需求追踪。新需求登记时立即更新此文件。

| ID | 需求名 | 级别 | 状态 | 开始日期 | 最后活动 |
|----|--------|------|------|----------|----------|
| {req_id} | {title} | {level} | {status} | {date} | {date} |

---

## 状态说明

| 状态 | 含义 |
|------|------|
| 📋 brainstorm | 方案讨论中 |
| 📋 proposal | 方案已定，待审核 |
| 📐 design | 技术设计中 |
| 📋 review_design | 设计审查中 |
| 📝 spec | 需求规格编写中 |
| 📋 review | 集成审核中 |
| 🔨 implementing | 代码实现中 |
| 📋 review_code | 代码审查中 |
| ✅ verify | 验收中 |
| ✅ done | 已完成 |
| ⏸️ paused | 暂停 |
| ❌ cancelled | 取消 |

## 并发规则

- 同时只有一个需求处于 `🔨 implementing`
- L1 需求可插队执行，不阻塞当前 L2/L3
- L3 过程中收到 L2 需求：完成后从 DevLog 恢复 L3 进度

> AI 会在需求状态变更时自动更新此表。
"""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(template, encoding="utf-8")
