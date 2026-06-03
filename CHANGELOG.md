# Aegis 版本历史

> 集中版本日志。自举时同步更新此处。

---

| 日期 | 版本 | 改动 |
|------|------|------|
| 2026-05-30 | v1.0 | 初始版本：7 阶段线性流程 |
| 2026-05-30 | v1.1 | 加入 L1/L2/L3 三级分级触发、技术栈自动发现 |
| 2026-05-30 | v1.2 | 分层重构（global + TechStack + TempData + DevLogs） |
| 2026-05-30 | v1.3 | 修复架构原则（完整 SOLID + GoF）+ My_Fish_01 实战测试 |
| 2026-05-30 | v2.0 | 完整 spec 格式 + 00/04 边界 + 需求输入引导 + 持续改进机制 |
| 2026-05-31 | v3.0 | 路径 .trae→Aegis；SKILL.md 拆分；审查双版本；进程恢复；迭代退回；收尾仪式；并发 INDEX；存量代码协作；跨 IDE 安装脚本 |
| 2026-05-31 | v3.0.1 | 四代理审查修复：命名规范化、消除 DRY、矩阵补维度、DevLog 强化、收尾失败处理、用户手册、提炼标准简化、一键安装 |
| 2026-05-31 | v3.0.2 | 融合 Karpathy Skills：完整 Aegis_Protocol.md 生成、.cursor/rules/aegis.mdc、Anti-Patterns 速查表、Key Insight 循环验证、README 升级、跨 IDE 支持矩阵、How to Know It's Working |
| 2026-05-31 | v3.0.3 | 命名重构：Aegis_Protocol.md + Aegis_Specs/ + Aegis_Intro.md；安装脚本不复制到项目；强制 Checklist 协议入口 |
| 2026-05-31 | v3.0.4 | L3-7 强化：07-verify 顶部强制验收标准速查表；收尾加步骤 0（文档完整性检查）；05-tasks 加验收对照；Protocol 加文档产出约束 |
| 2026-06-01 | v3.0.4 | Critical 修复：SKILL.md 编码修复（GB2312→UTF-8）；global.md 安全与合规（6 子章节）；4 个子代理审查定义；TechStack 补全 Go/Rust/Java/Docker；design.md 和 spec-L3.md 模板增强；DevLog 标准化 |
| 2026-06-01 | v3.0.5 | 文件结构重构：Aegis_Protocol.md → AGENTS.md（跨平台通用入口）；新增 aegis-boot Skill（自动触发）；L1 强制记录 DevLog + INDEX.md；INDEX.md 生命周期规范；安装脚本交互式平台选择 + VCS 忽略提示 |
| 2026-06-02 | v3.0.5 | 移除内置 .cursor（入口由脚本按需生成）；新增 .trae/rules/ 入口（Trae IDE）；安装选项增至 7 个；Boot Skill 改为兜底方案（始终安装）；INDEX.md 模板增加状态说明 |
| 2026-06-02 | v3.0.5 | Hotfix：Set-Content 全体加 -Encoding UTF8（解决中文乱码）；install-aegis.ps1 TechStack 补全至 9 个 |
| 2026-06-02 | v3.0.5 | 自举规范化：建立 CHANGELOG.md + BOOTSTRAP.md；INDEX.md 恢复纯模板（清 REQ 记录）；子代理增加「大白话」讲解；模板补全并发规则章节 |
| 2026-06-02 | v3.0.6 | L2 强化：每阶段增加 BOUNDARY CHECK + 失败恢复 + 阶段边界检查；aegis-boot 全面升级（MANDATORY SEQUENCE + 可执行边界检查）；SKILL.md 版本号 3.0 → 3.0.6 |

---

## Tags

| Tag | 描述 |
|-----|------|
| [v3.0.4](https://github.com/Szy-Fxy/Aegis/releases/tag/v3.0.4) | 验证流程强化 + 安全治理落地 |
| [v3.0.5](https://github.com/Szy-Fxy/Aegis/releases/tag/v3.0.5) | 文件结构重构 + 多入口安装 + 自举规范化 |
| [v3.0.6](https://github.com/Szy-Fxy/Aegis/releases/tag/v3.0.6) | L2 流程强化 + aegis-boot 升级 |