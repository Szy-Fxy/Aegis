# Aegis Toolchain 使用指南

## 安装（用户只需这两步）

 ```bash
pip install git+https://github.com/Szy-Fxy/Aegis.git
cd 我的游戏项目
aegis init
```

## 安装后你的项目结构

```
我的游戏项目/
├── Aegis/
│   ├── rules/
│   │   ├── global.md              ← AI 全局准则
│   │   ├── TechStack/             ← 技术栈规范 (9个)
│   │   ├── TempData/              ← 临时研究资料
│   │   └── DevLogs/               ← 开发日志
│   └── skills/
│       └── dev-workflow/
│           ├── SKILL.md           ← 工作流引擎
│           ├── sub-agents/        ← 子代理审查 (4个)
│           └── templates/         ← 文档模板 (9个)
└── Aegis_Specs/
    └── INDEX.md                   ← 需求索引
```

## 怎么用

打开 Hana，正常对话。AI 会自动：
1. 读 Aegis 规则文件
2. 分类 L1/L2/L3
3. 按流程走：设计 → 检查 → 实现 → 日志 → 完成
4. 自动调子代理审查（L3）

**你不需要手动敲 aegis 命令。** 它们是给 AI 在后台用的。

## 命令速查（AI 专用）

| 命令 | 作用 |
|------|------|
| `aegis start "标题"` | 登记新需求 |
| `aegis start "标题" -l L2` | 指定等级 |
| `aegis status` | 查看所有需求 |
| `aegis check` | BOUNDARY CHECK |
| `aegis advance` | 推进到下一阶段 |
| `aegis devlog write REQ-001 -m "摘要"` | 写 DevLog |
| `aegis preprocess "用户消息"` | 分类 + 注入规则到 prompt |

## 需求等级

| 等级 | 什么时候用 | 流程 |
|------|-----------|------|
| L1 | 修 bug、改配置 | 登记 → 改代码 → DevLog → 完成 |
| L2 | 加功能、优化 | 设计 → 实现 → DevLog → 完成 |
| L3 | 架构重构 | 7 阶段 + 4 子代理审查 |

## Git Hook（可选）

```bash
pip install pre-commit
pre-commit install
```

提交时自动验证 Aegis 合规性。

## 故障排除

| 症状 | 试试 |
|------|------|
| `aegis init` 找不到包 | 先 `pip install git+https://github.com/Szy-Fxy/Aegis.git` |
| `aegis` 命令不存在 | 重启终端 |
| state.json 报错 | 删 `Aegis/state/state.json` |
| 中文乱码 | `chcp 65001` |
| init 后文件不全 | `aegis init --force` |
