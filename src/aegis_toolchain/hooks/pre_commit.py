"""pre-commit hook — commit 前的 Aegis 合规检查

用法:
  在 .pre-commit-config.yaml 中配置:
    - repo: local
      hooks:
        - id: aegis-check
          name: Aegis Compliance Check
          entry: python -m aegis_toolchain.hooks.pre_commit
          language: system
          pass_filenames: false
          always_run: true
"""

import sys
from pathlib import Path


def main() -> int:
    """pre-commit hook 入口。返回 0 通过，1 阻断。"""
    project_path = Path.cwd()

    # 检查是否是 Aegis 项目
    state_path = project_path / "Aegis" / "state" / "state.json"
    if not state_path.exists():
        return 0

    # 加载 state.json
    try:
        from aegis_toolchain.core.state_manager import StateManager

        manager = StateManager(project_path)
        state = manager.load()
    except Exception as e:
        print(f"[Aegis Hook] ⚠️ 无法读取 state.json: {e}")
        print("[Aegis Hook] 跳过 Aegis 检查，允许提交")
        return 0

    # 查找 implementing 需求
    active = state.find_implementing()
    if active is None:
        return 0

    # 执行 BOUNDARY CHECK
    try:
        from aegis_toolchain.core.boundary_checker import BoundaryChecker

        checker = BoundaryChecker(project_path)
        report = checker.check(active)

        if report.all_passed:
            print(f"[Aegis Hook] ✅ REQ-{active.id} ({active.title}) BOUNDARY CHECK 全部通过")
            return 0
        else:
            print(f"[Aegis Hook] ❌ REQ-{active.id} ({active.title}) BOUNDARY CHECK 未通过:")
            for r in report.results:
                status = "✅" if r.passed else "✗"
                print(f"  {status} {r.name}: {r.detail}")
            print()
            print("[Aegis Hook] 提交已被阻断。请完成以上缺失项后重试。")
            print("[Aegis Hook] 提示: 运行 'aegis check' 查看详情")
            return 1
    except Exception as e:
        print(f"[Aegis Hook] ⚠️ BOUNDARY CHECK 执行失败: {e}")
        print("[Aegis Hook] 允许提交（避免阻塞正常开发）")
        return 0


if __name__ == "__main__":
    sys.exit(main())
