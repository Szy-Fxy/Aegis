# 全局通用准则

> 所有技术栈、所有项目均适用。优先级高于各技术栈规则。
>
> **Tradeoff**: 这些准则偏向工程严谨而非交付速度。对于简单任务（typo修复、单行改动），无需全部执行。

---

## AI 行为准则

> 来自 Karpathy 对 LLM 编程常见错误的总结。这些告诉 AI **怎么写代码**。

### 1. 先想再做 (Think Before Coding)

```
❌ 不假设、不隐藏困惑、不要默默选一个解释就开始写代码
✅ 不确定就问。多种理解就列出来。有更简单的方案就说。
```

```python
# 用户说："加一个导出用户数据的功能"

# ❌ AI 默默假设：导出全部用户、JSON 格式、写到本地文件
def export_users():
    users = User.query.all()
    with open('users.json', 'w') as f:
        json.dump([u.to_dict() for u in users], f)

# ✅ AI 先反问：
# 1. 导出全部用户还是筛选后的？
# 2. JSON / CSV / Excel？
# 3. 浏览器下载还是后台任务发邮件？
```

### 2. 简洁至上 (Simplicity First)

```
❌ 不过度设计、不加没被要求的功能、不为「未来可能需要」写抽象
✅ 最小代码解决问题。200 行能写成 50 行就重写
```

```python
# 用户说："写个折扣计算函数"

# ❌ 过度设计：策略模式 + ABC + dataclass，30 行框架代码只为了算 10% 折扣
from abc import ABC, abstractmethod
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float: ...

# ✅ 简洁方案：
def calculate_discount(amount: float, percent: float) -> float:
    return amount * (percent / 100)
```

> 自问：「一个高级工程师会觉得这是过度设计吗？」如果是，简化。

### 3. 精准修改 (Surgical Changes)

```
❌ 不改无关代码、不顺手格式化、不「顺便」重构、不改注释
✅ 只动你该动的。每行改动都应该能追溯到用户的需求
```

```typescript
// 用户说："修复邮件为空时崩溃的 bug"

// ❌ 顺手加了 username 验证、改了引号风格、加了 docstring
function validateUser(userData: any): boolean {
    /** Validate user data. */       // ← 没叫加
    const email = userData.email.trim()  // ← 改了引号风格
    if (!email || !email.includes("@")) throw Error("Invalid email")
    if (!userData.username || userData.username.length < 3) throw Error("Username too short")  // ← 没叫加
    return true
}

// ✅ 精准：只修 email 空值
function validateUser(userData) {
    const email = userData.email || ''  // ← 只加了这一行
    if (!email || !email.trim()) throw Error("Email required")
    ...
}
```

### 4. 目标驱动 (Goal-Driven Execution)

```
❌ 不把"做 XXX"当成目标。目标必须可验证
✅ 把任务变成可验证的检查点，循环直到全部通过
```

| 模糊任务 | 可验证目标 |
|----------|-----------|
| "加校验" | "写无效输入测试 → 让测试通过" |
| "修Bug" | "写能复现 Bug 的测试 → 让测试通过" |
| "重构X" | "重构前后测试全部通过" |

```
多步骤任务输出计划：
1. 加基础限流 → 验证: 10 次请求后返回 429
2. 提取为中间件 → 验证: 所有接口受保护
3. 升级 Redis 后端 → 验证: 重启后限流状态不丢失
```

---

### 常见反模式速查

> 这些不是"错误代码"，而是**时机错误**的代码 — 在不需要的时候引入了复杂度。

| 原则 | 反模式 | 修正 |
|------|--------|------|
| 先想再做 | 默默假设文件格式、字段、范围 | 明确列出假设，不确定就问 |
| 简洁至上 | 单个折扣计算用了策略模式 + ABC | 一个函数就够了，等真正需要多类型时再重构 |
| 精准修改 | 修 Bug 时改了引号风格、加了类型标注、加了 docstring | 只改导致 Bug 的那几行 |
| 目标驱动 | "我先审查代码再改进" | "写 Bug X 的复现测试 → 让测试通过 → 确认无回归" |

> **核心洞察**：好代码是解决今天问题的代码，不是提前解决明天问题的代码。复杂度可以在真正需要时再加 — 那时你有更多信息做出更好的设计。

---

## 架构原则（SOLID + 设计模式）

> 以下原则来自 Robert C. Martin 的 SOLID 原则、GoF 设计模式及业界实践经验。
> **关键理解**：原则是指导方向，不是教条。每个原则都有其适用场景和代价。

### SRP：单一职责原则

> A class should have only one reason to change. — Uncle Bob

- **正确理解**：「一个类只应有一个引起它变化的原因」，不是「一个类只做一件事」
- 判断标准：如果你能用「因为……所以需要改这个类」来描述变更，且只有一种「因为」，则满足 SRP

```csharp
// ❌ 违反 SRP：计分规则变了、UI 改了、音效改了 → 都需要修改这个类
class GameManager {
    void AddScore(int points)           { /* 计分逻辑 */ }
    void UpdateScoreUI()                { /* UI 刷新 */ }
    void PlayScoreSound()               { /* 音效播放 */ }
}

// ✅ 符合 SRP：每个类只有一个变化原因
class ScoreModel  { int Value; void Add(int p); }          // 变化原因：计分规则
class ScoreUI     { void Display(int score); }              // 变化原因：UI 设计
class ScoreAudio  { void PlayCollectSound(); }              // 变化原因：音效需求
```

> ⚠️ 代价：过度拆分会导致类爆炸。当某个「变化原因」从未独立变化过，不需要拆。

### OCP：开闭原则

> Open for extension, closed for modification.

```csharp
// ❌ 违反 OCP：每加一种敌人就要改 switch
void SpawnEnemy(string type) {
    switch(type) {
        case "tank":  /* 坦克逻辑 */ break;
        case "drone": /* 无人机逻辑 */ break;
        // 新敌人 → 改这里 → 可能引入 Bug
    }
}

// ✅ 符合 OCP：新敌人 = 新类，不改已有代码
interface IEnemy { void Spawn(); }
class TankEnemy  : IEnemy { public void Spawn() { /* 坦克 */ } }
class DroneEnemy : IEnemy { public void Spawn() { /* 无人机 */ } }
```

> ⚠️ 2-3 种变体用 switch 更清晰，5+ 种且还在增长时才值得抽接口。

### LSP：里氏替换原则

> Subtypes must be substitutable for their base types.

```csharp
// ❌ 违反 LSP：矩形能独立设宽高，正方形不能 → Square 不能替换 Rectangle
class Rectangle {
    public virtual int Width  { get; set; }
    public virtual int Height { get; set; }
}
class Square : Rectangle {
    public override int Width  { set { base.Width = base.Height = value; } }
    public override int Height { set { base.Width = base.Height = value; } }
}

// ✅ 符合 LSP：各自独立，不强行继承
interface IShape { int Area(); }
class Rectangle : IShape { ... }
class Square    : IShape { ... }
```

> ⚠️ 最常见违反：子类覆写方法但什么都不做（空方法）。

### ISP：接口隔离原则

> Many specific interfaces are better than one general interface.

```csharp
// ❌ 违反 ISP：士兵被迫实现「飞」的方法
interface IUnit {
    void Move();
    void Attack();
    void Heal();
    void Fly();      // ← 士兵不会飞
}
class Soldier : IUnit {
    void Fly() { /* 空着，抛异常 */ }  // ← 判断方法就来自这里
}

// ✅ 符合 ISP：按职责拆小接口
interface IMovable  { void Move(); }
interface IAttacker { void Attack(); }
interface IFlyable  { void Fly(); }
class Soldier : IMovable, IAttacker { ... }
class Drone   : IMovable, IFlyable  { ... }
```

### DIP：依赖倒转原则

> Depend on abstractions, not on concretions.

```csharp
// ❌ 违反 DIP：Tank 直接 new Bullet()，换子弹类型要改 Tank 代码
class Tank {
    void Shoot() { new Bullet().Fire(); }
}

// ✅ 符合 DIP：依赖 IBulletFactory 抽象
class Tank {
    readonly IBulletFactory _factory;
    public Tank(IBulletFactory factory) { _factory = factory; }
    void Shoot() { _factory.Create().Fire(); }
}
```

### 组合优于继承

> Favor object composition over class inheritance. — GoF

- 用「持有引用 + 委托调用」替代深层继承链
- 继承的代价：编译时绑定、破坏封装、深层链难维护

```csharp
// ❌ 继承滥用：为了复用代码而继承
class Bird {
    void Fly() { /* 飞 */ }
}
class Penguin : Bird {
    void Fly() { throw new Exception("企鹅不会飞"); }  // ← LSP 一起违反
}

// ✅ 组合：行为是可替换的组件
interface IFlyBehavior { void Fly(); }
class Bird {
    IFlyBehavior _flyBehavior;
    void PerformFly() { _flyBehavior.Fly(); }
}
```

> ⚠️ 当「子类是父类的一种（is-a）」且行为差异不大时，继承是合适的。

### 迪米特法则（最少知识原则）

> Only talk to your immediate friends.

- 一个对象应对其他对象有尽可能少的了解
- 链式调用 `a.GetB().GetC().DoSomething()` 是典型违反信号

### 实用的「不要」清单

- **不要过度设计**：一个接口只有一个实现，就不要抽接口
- **不要提前抽象**：等第二个场景出现时再考虑抽象，而不是猜未来
- **不要为了模式而模式**：如果最简单的写法已经够清晰，就用最简单的
- **不要顺手格式化**：修 Bug 时只修 Bug，不改代码风格
- **防御性保留**：不确定是否该删的代码，标记 `// TODO(@owner, YYYY-MM-DD): 确认是否可删除`，超过 30 天未确认的视为可清理

## 依赖管理

- 优先用语言标准库，其次用社区最主流库（NPM 周下载量 > 100k / PyPI 月下载 > 1M 级别）
- 新增第三方库前，先检查项目是否已有类似功能的库
- 锁定版本号，避免隐式升级（package-lock.json / poetry.lock / Pipfile.lock）

## 错误处理

- 不吞异常 — 要么真正处理，要么向上传播
- 对外接口做好入参校验（类型 + 范围 + 非空）
- 关键路径加日志，但绝不暴露：秘钥、token、密码、用户隐私、API Key

## 安全与合规

> ⚠️ **安全是工程的基础，不是后期修补的补丁。** 以下规则在所有需求级别（L1/L2/L3）中均适用，不可跳过。

### 认证与授权

- **绝不硬编码**：任何密钥、token、密码、连接字符串、API Key 不得出现在代码中
- **环境变量管理**：敏感配置使用 `.env` 文件管理，`.env` **必须**加入 `.gitignore`
- **最小权限原则**：API Key / Token 仅获取完成功能所需的最小权限范围
- **凭据轮换**：长期运行的项目必须支持凭据过期和轮换机制

### 敏感数据保护

- **不记录敏感信息**：日志中绝不输出密钥、token、密码、用户隐私数据
- **不将敏感信息输入 AI**：代码中包含真实密钥/密码时，向 AI 提问前先替换为占位符
- **数据传输加密**：敏感数据在网络上传输必须使用 HTTPS/TLS
- **数据脱敏**：日志/调试输出中对邮箱、手机号、身份证号等 PII（个人身份信息）做脱敏处理

### 输入安全

- **永远不信任外部输入**：用户输入、API 响应、文件内容均需校验和清洗
- **参数化查询**：数据库操作使用参数化查询 / ORM，杜绝 SQL 拼接
- **XSS 防护**：Web 项目中对用户生成内容做输出编码
- **文件上传安全**：校验文件类型、大小，限制上传目录权限

### 依赖安全

- **锁定版本**：依赖锁定具体版本号（package-lock.json / poetry.lock / Pipfile.lock）
- **定期审计**：`npm audit` / `pip audit` / `cargo audit` 定期检查已知漏洞
- **最小依赖**：新增第三方库前必须确认项目无替代方案，避免引入不必要依赖链

### AI 使用安全

- **不将生产数据喂给 AI**：代码示例中的数据必须是虚构/脱敏的
- **不将完整密钥/密码告诉 AI**：讨论配置问题时使用占位符 `YOUR_API_KEY_HERE`
- **审查 AI 生成代码**：AI 可能生成含有安全漏洞的代码（如未校验输入、硬编码凭据），必须人工复查

### 合规检查清单（每次提交前）

```
□ 代码中无硬编码凭据
□ .env 在 .gitignore 中
□ 新增依赖无已知高危漏洞
□ 用户输入有校验和清洗
□ 日志中无敏感数据
□ 未将生产数据/真实凭据暴露给 AI
```

## 跨技术栈通用约定

- 文件名：多单词用 `-` 连接（kebab-case）或 `_` 连接（snake_case），按语言惯例
- 缩进：2 空格（JS/TS/YAML）或 4 空格（Python），按语言惯例
- 行尾：LF（`\n`），不要 CRLF
- 文件末尾：保留一个空行