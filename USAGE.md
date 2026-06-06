# Aegis Toolchain 使用指南

> 从零开始，逐步上手

---

## 第一步：安装

```bash
# 前提：Python ≥ 3.11 已安装
git clone https://github.com/Szy-Fxy/Aegis.git aegis-toolchain
cd aegis-toolchain
pip install -e .
```

验证安装：
```bash
aegis --help
```
你应该看到 6 个命令：`start` `check` `advance` `status` `devlog` `preprocess`

## 第二步：在你的项目里初始化

进入你已有的 Aegis 项目目录（确保有 `Aegis/rules/global.md`）：

```bash
cd /path/to/your-project
```

如果你还没有 Aegis 项目，先创建一个最小骨架：

```bash
mkdir -p my-project/Aegis/rules/DevLogs
mkdir -p my-project/Aegis/rules/TechStack
mkdir -p my-project/Aegis/skills/dev-workflow
mkdir -p my-project/Aegis_Specs
echo "# 全局规则" > my-project/Aegis/rules/global.md
echo "# 工作流引擎" > my-project/Aegis/skills/dev-workflow/SKILL.md
cd my-project
```

## 第三步：创建第一个需求

```bash
aegis start "修复登录页按钮颜色" --level auto
```

输出示例：
```
🔍 自动分类: L1 (置信度 75%)
   理由: 匹配 L1 关键词: 修复, 颜色

✅ 已登记 REQ-001 [L1] 修复登录页按钮颜色
   阶段: 🔨 implementing
   下一步: aegis check
```

> **发生了什么？** 系统自动分类了需求等级（L1），在 `Aegis/state/state.json` 中记录了需求，在 `Aegis_Specs/INDEX.md` 中登记了一行。

## 第四步：查看状态

```bash
aegis status
```

```
活跃需求:
──────────────────────────────────────────────────────────────────────
  REQ-001  修复登录页按钮颜色                   [L1]  🔨 implementing

总计: 1 活跃, 0 已完成
```

查看单个需求详情：
```bash
aegis status REQ-001
```

## 第五步：执行 BOUNDARY CHECK

```bash
aegis check
```

对于 L1 需求，系统会检查 INDEX.md 登记和 DevLog。如果 DevLog 还没写，会显示 ✗。

## 第六步：写 DevLog 并完成

```bash
aegis devlog write REQ-001 -m "修复了登录按钮的 CSS 颜色变量"
aegis advance
```

```
✅ BOUNDARY CHECK 全部通过 (2/2)
✅ REQ-001 修复登录页按钮颜色: implementing → ✅ done
🎉 REQ-001 已完成！
```

## L2 需求完整流程

L2 需求比 L1 多一个设计阶段。完整流程：

```bash
# 1. 开始
aegis start "捕鱼炮台系统" --level L2

# 2. 创建 design.md（手动或用 AI 写）
mkdir -p Aegis_Specs/L2/捕鱼炮台系统
echo "# 炮台系统设计" > Aegis_Specs/L2/捕鱼炮台系统/design.md
echo "验收标准：玩家点击炮台按钮后，炮台在 0.5s 内出现并可发射子弹" >> Aegis_Specs/L2/捕鱼炮台系统/design.md

# 3. 检查设计阶段
aegis check    # 应该 3/3 通过

# 4. 推进到实现
aegis advance  # design → 🔨 implementing

# 5. 写代码...

# 6. 写 DevLog
aegis devlog write REQ-001 -m "实现了炮台生成、瞄准和子弹发射"

# 7. 完成
aegis advance  # implementing → ✅ done
```

## 常用命令速查

| 想做什么 | 命令 |
|---------|------|
| 开始需求 | `aegis start "标题" -l L2` |
| 自动分类 | `aegis start "标题" --level auto` |
| 看所有需求 | `aegis status` |
| 看一个需求 | `aegis status REQ-001` |
| 看 JSON 状态 | `aegis status --json` |
| 检查当前阶段 | `aegis check` |
| 检查指定需求 | `aegis check REQ-001` |
| 推进到下一阶段 | `aegis advance` |
| 强制推进 | `aegis advance -f` |
| 写 DevLog | `aegis devlog write REQ-001 -m "内容"` |
| 看 DevLog | `aegis devlog show` |
| 预处理消息 | `aegis preprocess "帮我修bug"` |

## 配合 AI 使用

在 Hana 中开发时，流程是：

1. 你在对话框说需求
2. AI 收到后调用 `aegis preprocess` 获取增强 prompt
3. AI 调用 `aegis start` 登记需求
4. AI 写设计文档，调用 `aegis check` 验证
5. 你确认后，AI 调用 `aegis advance` 推进
6. AI 写代码，调用 `aegis devlog` 记录
7. AI 调用 `aegis advance` 完成
8. `git commit` 时 pre-commit hook 自动验证合规性

## 安装 pre-commit hook（可选但推荐）

```bash
# 在你的项目目录下
pip install pre-commit
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: local
    hooks:
      - id: aegis-check
        name: Aegis Compliance Check
        entry: python -m aegis_toolchain.hooks.pre_commit
        language: system
        pass_filenames: false
        always_run: true
EOF
pre-commit install
```

之后每次 `git commit` 都会自动检查 Aegis 合规性。不通过会阻断提交。

## 故障排除

| 问题 | 解决 |
|------|------|
| `aegis: command not found` | 确认 `pip install -e .` 成功，检查 Python Scripts 目录在 PATH 中 |
| `state.json 被破坏` | 删除 `Aegis/state/state.json`，重新 `aegis start` |
| `filelock 超时` | 可能有另一个 aegis 进程在运行，等待 5 秒或关闭其他终端 |
| check 总是失败 | 确认 `Aegis_Specs/INDEX.md` 存在且表格格式正确 |
