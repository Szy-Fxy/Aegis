# 技术设计：Aegis Toolchain

> L3-3 | 2026-06-05 | Phase 1 技术设计

## 新 API

### CLI 命令组

```python
# src/aegis_toolchain/cli/main.py
import typer

app = typer.Typer(
    name="aegis",
    help="Aegis 开发治理工具链",
    no_args_is_help=True,
)

# 子命令组
app.add_typer(start_app, name="start", help="开始一个新需求")
app.add_typer(check_app, name="check", help="执行 BOUNDARY CHECK")
app.add_typer(status_app, name="status", help="查看项目状态")
app.add_typer(advance_app, name="advance", help="推进到下一阶段")
app.add_typer(devlog_app, name="devlog", help="DevLog 操作")
app.add_typer(preprocess_app, name="preprocess", help="预处理器")
```

#### aegis start

```python
# src/aegis_toolchain/cli/start.py
@app.command()
def start(
    title: str = typer.Argument(..., help="需求名称"),
    level: str = typer.Option("auto", "--level", "-l", help="需求等级: L1/L2/L3/auto"),
    description: str = typer.Option("", "--desc", "-d", help="需求描述"),
) -> None:
    """开始一个新需求，自动分类并登记到 INDEX.md 和 state.json"""
```

#### aegis check

```python
# src/aegis_toolchain/cli/check.py
@app.command()
def check(
    requirement_id: str = typer.Argument(None, help="需求 ID，默认当前活跃需求"),
) -> None:
    """执行当前阶段的 BOUNDARY CHECK，输出通过/失败和缺失项"""
```

#### aegis advance

```python
# src/aegis_toolchain/cli/advance.py
@app.command()
def advance(
    requirement_id: str = typer.Argument(None, help="需求 ID"),
    force: bool = typer.Option(False, "--force", "-f", help="跳过 check 强制推进"),
) -> None:
    """推进需求到下一阶段（前置条件：BOUNDARY CHECK 全部通过）"""
```

#### aegis status

```python
# src/aegis_toolchain/cli/status.py
@app.command()
def status(
    requirement_id: str = typer.Argument(None, help="需求 ID，默认显示全部"),
    json_output: bool = typer.Option(False, "--json", help="JSON 格式输出"),
) -> None:
    """查看项目当前状态"""
```

#### aegis devlog

```python
# src/aegis_toolchain/cli/devlog.py
@app.command()
def devlog_write(
    requirement_id: str = typer.Argument(..., help="需求 ID"),
    message: str = typer.Option("", "--message", "-m", help="DevLog 内容"),
    editor: bool = typer.Option(False, "--editor", "-e", help="打开编辑器编写"),
) -> None:
    """写入 DevLog 条目"""

@app.command()
def devlog_show(
    requirement_id: str = typer.Argument(None, help="需求 ID，默认最新"),
) -> None:
    """查看 DevLog"""
```

#### aegis preprocess

```python
# src/aegis_toolchain/cli/preprocess_cmd.py
@app.command()
def preprocess(
    user_message: str = typer.Argument(..., help="用户原始消息"),
    project_path: str = typer.Option(".", "--project", "-p", help="项目路径"),
) -> None:
    """预处理用户消息，输出增强后的 system prompt"""
```

---

### 核心模块 API

#### StateManager

```python
# src/aegis_toolchain/core/state_manager.py
from pydantic import BaseModel
from pathlib import Path

class StateManager:
    """state.json 的线程/进程安全读写，带 filelock"""

    def __init__(self, project_path: Path) -> None:
        """初始化，确定 state.json 和 lock 文件路径
        
        state_path = project_path / "Aegis" / "state" / "state.json"
        lock_path  = state_path.with_suffix(".json.lock")
        """

    def load(self) -> AegisState:
        """加载 state.json，文件不存在时返回默认空状态
        Raises: StateCorruptedError — JSON 损坏或 schema 校验失败
        """

    def save(self, state: AegisState) -> None:
        """原子写入 state.json（写入临时文件 + 重命名）"""

    def get_active_requirement(self) -> Requirement | None:
        """获取当前 🔨 implementing 的需求"""

    def get_requirement(self, req_id: str) -> Requirement | None:
        """按 ID 查找需求"""

    def add_requirement(self, req: Requirement) -> None:
        """新增需求，自动检查并发（不能同时两个 implementing）"""

    def update_requirement(self, req_id: str, **kwargs) -> None:
        """更新需求字段（phase、checks 等）"""

    def get_next_id(self) -> str:
        """生成下一个需求 ID（REQ-003, REQ-004...）"""
```

#### BoundaryChecker

```python
# src/aegis_toolchain/core/boundary_checker.py
from dataclasses import dataclass, field

@dataclass
class CheckResult:
    """单条检查结果"""
    name: str
    passed: bool
    detail: str  # 通过/失败的具体原因

@dataclass
class BoundaryReport:
    """BOUNDARY CHECK 完整报告"""
    requirement_id: str
    phase: str  # design / implement / verify
    results: list[CheckResult] = field(default_factory=list)
    
    @property
    def all_passed(self) -> bool: ...

class BoundaryChecker:
    """执行各阶段的 BOUNDARY CHECK"""

    def __init__(self, project_path: Path) -> None: ...

    def check(self, requirement: Requirement) -> BoundaryReport:
        """根据需求当前阶段，执行对应 BOUNDARY CHECK
        L1: INDEX.md 登记 + DevLog
        L2-design: INDEX.md + design.md 存在 + 用户语言验收标准
        L2-implement: INDEX.md 状态 + 代码编译
        L2-verify: INDEX.md 更新 + DevLog 写入
        L3: 各阶段对应文档存在性
        """
```

#### RuleLoader

```python
# src/aegis_toolchain/core/rule_loader.py
class RuleLoader:
    """加载 Aegis 规则文件，用于预处理器注入"""

    def __init__(self, project_path: Path) -> None: ...

    def load_all(self) -> dict[str, str]:
        """加载所有规则，返回 {文件名: 内容}"""

    def load_global(self) -> str:
        """加载 Aegis/rules/global.md"""

    def load_workflow(self) -> str:
        """加载 Aegis/skills/dev-workflow/SKILL.md"""

    def load_techstack(self, keywords: list[str]) -> str:
        """根据关键词匹配技术栈文件"""

    def load_project_context(self) -> str:
        """加载项目 AGENTS.md / README.md"""
```

#### IndexManager

```python
# src/aegis_toolchain/core/index_manager.py
class IndexManager:
    """INDEX.md 的结构化读写"""

    def __init__(self, project_path: Path) -> None: ...

    def read_all(self) -> list[dict]:
        """解析 INDEX.md 表格，返回需求列表"""

    def add_entry(self, req_id: str, title: str, level: str, status: str) -> None:
        """在 INDEX.md 表格末尾新增一行"""

    def update_status(self, req_id: str, status: str) -> None:
        """更新指定需求的状态列和最后活动日期"""
```

---

### Pydantic 数据模型

```python
# src/aegis_toolchain/models/state.py
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from enum import Enum

class RequirementLevel(str, Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"

class RequirementPhase(str, Enum):
    BRAINSTORM = "brainstorm"
    PROPOSAL = "proposal"
    DESIGN = "design"
    SPEC = "spec"
    REVIEW = "review"
    IMPLEMENTING = "implementing"
    DONE = "done"
    PAUSED = "paused"
    CANCELLED = "cancelled"

class BoundaryChecks(BaseModel):
    """各阶段 BOUNDARY CHECK 的记录"""
    index_registered: bool = False
    design_created: bool = False
    user_approved: bool = False
    code_compiles: bool = False
    devlog_written: bool = False

class Requirement(BaseModel):
    """单个需求条目"""
    id: str = Field(..., pattern=r"^REQ-\d{3}$")
    title: str = Field(..., min_length=1, max_length=100)
    level: RequirementLevel
    phase: RequirementPhase = RequirementPhase.IMPLEMENTING  # L1 默认 implementing；L2/L3 由 aegis start 按 level 覆盖为 design/brainstorm
    created: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    description: str = ""
    files_changed: list[str] = Field(default_factory=list)
    boundary_checks: BoundaryChecks = Field(default_factory=BoundaryChecks)

    @field_validator("level")
    @classmethod
    def validate_level_phase_match(cls, v, info):
        """L1 不应有 brainstorm/proposal/design/spec/review 阶段"""
        ...

class AegisState(BaseModel):
    """state.json 顶层 schema"""
    version: str = "1.0.0"
    active_requirements: list[Requirement] = Field(default_factory=list)
    completed_requirements: list[Requirement] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.now)
```

```python
# src/aegis_toolchain/models/config.py
from pydantic import BaseModel

class AegisConfig(BaseModel):
    """aegis-toolchain 自身配置（可选，未来扩展）"""
    project_name: str = ""
    rules_path: str = "Aegis/rules"
    specs_path: str = "Aegis_Specs"
    devlogs_path: str = "Aegis/rules/DevLogs"
    state_path: str = "Aegis/state/state.json"
```

---

### 预处理器

```python
# src/aegis_toolchain/preprocessor/classifier.py
from enum import Enum

class TaskLevel(Enum):
    L1 = "L1"
    L2 = "L2" 
    L3 = "L3"

class ClassificationResult:
    level: TaskLevel
    confidence: float  # 0.0 ~ 1.0
    keywords_matched: list[str]
    reason: str

def classify(user_message: str) -> ClassificationResult:
    """关键词 + 规则分类
    L3 关键词: 架构, 重构, 重写, 大改, 重新设计
    L2 关键词: 新增, 功能, 模块, 优化, feature, 实现
    L1 关键词: 修复, fix, 改个, 小改, 配置, typo, 颜色, 文案
    未匹配 → 默认 L2, confidence=0.3
    """

# src/aegis_toolchain/preprocessor/injector.py
def build_system_prompt(
    classification: ClassificationResult,
    rules: dict[str, str],
    project_state: AegisState | None,
) -> str:
    """根据分类结果和规则内容，组装增强版 system prompt
    格式: [AEGIS MANDATORY RULES] + 分类 + 流程要求 + 规则摘要
    """
```

---

### Git Hook

```python
# src/aegis_toolchain/hooks/pre_commit.py
def main() -> int:
    """pre-commit hook 入口
    1. 检查 state.json 是否有活跃需求
    2. 验证当前阶段 BOUNDARY CHECK
    3. 检查 INDEX.md 是否被修改（如果需求已完成）
    4. 返回 0（通过）或 1（阻断）
    """
```

---

## 修改 API

无。Phase 1 只做增量，不修改现有 Aegis 内核。

## 删除

| 删除项 | 替代方案 |
|--------|----------|
| 无 | Phase 1 纯增量 |

## 保留

| 保留项 | 原因 |
|--------|------|
| Aegis/rules/DevLogs/ 文本 DevLog | 与 state.json 并存过渡期，CLI 同时维护两者 |
| Aegis_Specs/INDEX.md 手动维护能力 | CLI 辅助写，但不剥夺手动改的能力 |
| Aegis/skills/aegis-boot/SKILL.md 现有流程 | 只加自检指令块，不改原有流程定义 |
| Aegis/skills/dev-workflow/SKILL.md | 不动核心工作流引擎 |
| 所有现有规则文件 | 不破坏已有 Aegis 部署 |

## 数据流

### 用户消息处理流程

```
用户输入 "帮我加个炮台系统"
        │
        ▼
┌───────────────────┐
│  preprocessor     │
│  classify()       │  → 分类结果: L2, confidence=0.8
│  + load_rules()   │  → global.md + unity.md + workflow
│  + build_prompt() │  → 增强 system prompt
└───────┬───────────┘
        │
        ▼
┌───────────────────┐
│  增强后的 prompt   │  → [AEGIS MANDATORY] 本次任务 L2...
│  到达 AI          │
└───────┬───────────┘
        │
        ▼
   AI 执行开发流程
        │
        ├──→ 调用 aegis start "炮台系统" --level L2
        │    └──→ StateManager.add_requirement()
        │         IndexManager.add_entry()
        │
        ├──→ AI 创建设计文档
        │
        ├──→ 调用 aegis check REQ-003
        │    └──→ BoundaryChecker.check() → BoundaryReport
        │         检查: design.md 存在✓ | 用户确认?
        │
        └──→ git commit 触发 pre-commit hook
             └──→ 验证 state.json + INDEX.md 一致性
```

### 状态恢复流程

```
跨会话恢复
        │
        ▼
  aegis status --json
        │
        ▼
┌───────────────────┐
│ state.json        │
│ {                 │
│   active: [{      │
│     id: "REQ-003",│
│     phase: "design│
│     checks: {     │
│       design_ok:✓ │
│       approved:✗  │  ← 精确知道卡在哪
│     }             │
│   }]              │
│ }                 │
└───────────────────┘
        │
        ▼
  AI 读取后告知用户:
  "上次 REQ-003（炮台系统）在设计阶段，design.md 已创建，等待确认。
   继续？"
```

## 依赖关系

```
┌──────────────┐
│  CLI 层       │  typer 子命令
│  (cli/)       │
└──────┬───────┘
       │ 调用
       ▼
┌──────────────┐     ┌──────────────────┐
│  Core 层      │────→│  Models 层        │
│  (core/)      │     │  (models/)        │
│              │     │  Pydantic schema  │
│ StateManager │◄────│  AegisState       │
│ BoundaryChkr │◄────│  Requirement      │
│ RuleLoader   │     │  BoundaryReport   │
│ IndexManager │     └──────────────────┘
└──────┬───────┘
       │ 使用
       ▼
┌──────────────┐
│  文件系统      │
│  state.json   │
│  INDEX.md     │
│  *.md 规则    │
│  DevLogs/     │
└──────────────┘
```

```
┌──────────────┐     独立调用
│  Preprocessor │────→ RuleLoader → 规则文件
│  (preprocessor)│
└──────────────┘

┌──────────────┐     Git 触发
│  Git Hook     │────→ StateManager → state.json
│  (hooks/)     │────→ IndexManager → INDEX.md
└──────────────┘
```

依赖关系原则：CLI 不直接访问文件系统，全部通过 Core 层。Core 层是唯一知道文件路径和格式的地方。

## 错误处理策略

### 正常路径

| 场景 | 处理方式 |
|------|---------|
| state.json 不存在 | 返回默认空 AegisState，不报错 |
| state.json 格式损坏 | 抛出 StateCorruptedError，提示备份旧文件并重建 |
| INDEX.md 不存在 | 提示用户"非 Aegis 项目，是否初始化？" |
| 需求 ID 重复 | 拒绝添加，提示已存在 |
| 两个 implementing 并发 | 拒绝添加，提示先完成当前需求 |

### 异常路径降级

| 场景 | 降级方案 |
|------|---------|
| filelock 获取超时（>5s） | 以只读模式加载 state，不写入 |
| 规则文件缺失 | 跳过该文件，输出 warning，继续处理 |
| Git 命令不可用（Hook 中） | 跳过 Hook，输出 "Git not found, skipping Aegis check" |
| 预处理器分类置信度 <0.5 | 标记为"不确定"，让 AI 自行判断 |

### 用户可见的错误

```
❌ aegis start "炮台" --level auto
   → "需求 REQ-001（v3.1.0-feedback）仍在 🔨 implementing 中。
      请先完成或暂停该需求后再开始新的。"

❌ aegis advance REQ-003
   → "BOUNDARY CHECK 未通过 (1/3):
      ✗ design.md 不存在 (Aegis_Specs/L2/炮台/design.md)
      ✓ INDEX.md 已登记
      ✓ 验收标准已用用户语言
      请完成缺失项后重试。"

✅ aegis status
   → "活跃需求: REQ-003 炮台系统 [L2] 📐 design
      BOUNDARY CHECK: 1/3 通过
      缺少: design.md, 用户确认"
```

## 安全考量

- **无敏感数据**：state.json 只存需求元数据（标题/等级/阶段），不含密码、密钥、Token
- **文件路径校验**：所有文件操作限制在项目路径内，拒绝 `../` 穿越
- **JSON 注入防护**：Pydantic schema 校验拒绝非法字段和类型
- **无网络请求**：Phase 1 为纯本地工具，不上传数据
- **Hook 权限最小化**：pre-commit hook 只读取项目文件，不执行外部命令（除 git 自身）

## 测试策略

| 层级 | 覆盖 | 关键用例 |
|------|------|---------|
| **单元测试** | 所有 Core/Models | StateManager CRUD、BoundaryChecker 各阶段、Classifier 分类准确性、Pydantic schema 校验 |
| **集成测试** | CLI + Core 联动 | `aegis start` → `aegis check` → `aegis advance` 完整流程、并发锁测试、bad state.json 恢复 |
| **边界用例** | 异常路径 | state.json 损坏、filelock 超时、INDEX.md 空文件、L3 文档缺失、Windows/Unix 路径差异 |

### 关键测试场景

1. **完整 L2 流程**：start → check(design fail) → 创建 design.md → check(design pass) → advance → check(implement) → 修改代码 → check(implement pass) → advance → devlog → 验证 state.json 和 INDEX.md 一致
2. **并发锁**：两个进程同时 save state.json，确认只有一个写入成功，另一个超时降级
3. **分类准确性**：用 20 条典型需求消息测试 classify()，要求 L1/L2/L3 准确率 ≥80%

## 方案风险边界

| 什么情况下这个方案会失败？ | 为什么？ |
|---|---|
| AI 不调用 `aegis check`，直接跳到写代码 | CLI 依赖 AI 主动调用，没有强制钩子。**缓解**：SKILL.md 自检指令 + pre-commit hook 兜底阻断 |
| 预处理器无法嵌入 Hana 的消息链路 | 目前 Hana 没有"消息预处理钩子"的公开 API。**降级**：预处理器以 `aegis preprocess` 子命令存在，AI 在流程中手动调用 |
| state.json 和文本 DevLog/INDEX.md 数据不一致 | 并存过渡期可能出现 AI 更新了 INDEX.md 但没调 CLI。**缓解**：`aegis check` 同时校验两者一致性 |

### 已知限制

- 预处理器在 Hana 平台缺乏原生钩子的情况下，只能作为被动工具而非自动拦截
- 不保证 AI 一定在正确时机调用 CLI 命令（这是 Phase 2 MCP 要解决的核心问题）
- state.json 的 filelock 对网络文件系统（NAS/NFS）的锁行为未经充分测试
- 当前仅支持单个项目，不支持 monorepo 多子项目场景

---

> 基于提案 02-proposal.md + 四份调研报告的技术设计
> 下一阶段：L3-4 需求规格（将 API 展开为详细的功能需求）
