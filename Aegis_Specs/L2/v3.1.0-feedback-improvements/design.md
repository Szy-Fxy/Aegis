# v3.1.0 — 流程强化：INDEX.md 登记 + 验收标准 + 风险边界

## 背景

基于三份输入：
1. **AI 用户自检反馈 06-02**（窗口自适应重构）— 验收标准方向错误、三层容器方案被推翻
2. **AI 用户自检反馈 06-03**（综合收尾）— 先写代码后补设计、hover 方案改 4 次
3. **AI 用户流程缺陷报告** — L2 缺少 INDEX.md 登记步骤，全局规则漂浮无锚点

## 改动范围

| 文件 | 改动 |
|------|------|
| `skills/aegis-boot/SKILL.md` | L1/L2 流程 + 边界检查全面修改 |
| `skills/dev-workflow/SKILL.md` | L1/L2 流程 + 边界检查 + 反借口表同步修改 |
| `skills/dev-workflow/templates/spec-L2.md` | 内部标题去歧义 + 新增方案风险边界 section |
| `skills/dev-workflow/templates/design.md` | 新增方案风险边界 section |
| `skills/dev-workflow/templates/proposal.md` | 新增方案风险边界 section |

## 详细设计

### 改进 1：INDEX.md 登记步骤（L1 + L2）

**问题**：L2 流程从分类到 L2-3 之间，没有任何步骤让你往 INDEX.md 写新行。L2-3 用「更新」一词暗含条目已存在。全局规则「新需求登记时立即更新 INDEX.md」漂浮无锚点。L1 同理。

**修复**：

L1 步骤改为：
```
0. 登记到 INDEX.md（状态 🔨 implementing）
1. 修改代码
2. 展示改动摘要 → 等用户确认
3. 写 DevLog
4. 更新 INDEX.md（标记 ✅ done）
```

L2-1 步骤改为（新增 Step 0）：
```
Step 0: 登记到 INDEX.md（状态 📐 design）
Step 1: 创建 design.md
Step 2: 展示方案
Step 3: 验收标准用户视角检查
Step 4: 等用户确认
```

L2-2 步骤改为（新增 Step 0）：
```
Step 0: 更新 INDEX.md 状态为 🔨 implementing
Step 1: 按 design.md 写代码
Step 2: 运行 typecheck / lint / build
Step 3: 展示改动摘要
Step 4: 等用户确认
```

**L2-1 Boundary Check 追加**：
- [ ] INDEX.md 中已有当前需求条目（状态 📐 design）？
- [ ] 验收标准已用用户语言表述？

**L2-2 Boundary Check 追加**：
- [ ] INDEX.md 状态 = 🔨 implementing？

### 改进 2：验收标准用户视角检查

**位置**：aegis-boot L2-1 Step 3 + dev-workflow L2-1

**新增检查**：
- 验收标准是否用了用户自己的语言描述？（而非技术语言）
- 自问：「如果我是用户，看到这个验收标准，我知道验收时该看什么吗？」
- 如果验收标准是技术视角（如"无溢出"、"无报错"），必须补充用户视角描述

### 改进 3：方案风险边界

**位置**：spec-L2.md、design.md、proposal.md 模板

**新增 section**：
```markdown
## 方案风险边界
| 什么情况下这个方案会失败？ | 为什么？ |
|--------------------------|----------|
| {场景 1} | {原因} |
| {场景 2} | {原因} |
```
规则：至少列出 2 个风险场景。

### 改进 4：模板命名去歧义

`templates/spec-L2.md` 内部标题从 `# design.md 模板（L2）` 改为 `# L2 方案设计模板`

## 不受影响的部分

- L3 完整 7 阶段
- global.md 全局规则
- 安装脚本（仅版本号更新）
- BOOTSTRAP.md
- 其他模板文件

## 版本号

v3.0.7 → v3.1.0（L2 改动，MINOR +1, PATCH 归零）