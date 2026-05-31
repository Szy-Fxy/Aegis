# 全局通用准则

> 所有技术栈、所有项目均适用。优先级高于各技术栈规则。

---

## 代码风格

- 不添加无意义注释 — 注释只解释「为什么这样写」不解释「这段代码做什么」
- 命名清晰自解释，不追求缩写。函数名要能望文生义
- 保持和已有代码一致的风格，不做不必要的格式化或重构
- 函数保持短小精悍，做好一件事（但不能为了短而强行拆碎语义完整的逻辑）

## 架构原则（SOLID + 设计模式）

> 以下原则来自 Robert C. Martin 的 SOLID 原则、GoF 设计模式及业界实践经验。
> **关键理解**：原则是指导方向，不是教条。每个原则都有其适用场景和代价。

### SRP：单一职责原则

> A class should have only one reason to change. — Uncle Bob

- **正确理解**：「一个类只应有一个引起它变化的原因」，不是「一个类只做一件事」
- 判断标准：如果你能用「因为……所以需要改这个类」来描述变更，且只有一种「因为」，则满足 SRP
- 例如：`GameManager` 同时管 UI、分数、游戏胜负、敌人计数 = 4 个变化原因 → 违反 SRP

```csharp
// ❌ 违反 SRP：这个类因为「计分规则变了」「UI改了」「音效改了」都需要修改
class GameManager {
    void AddScore(int points) { ... }
    void UpdateScoreUI() { ... }
    void PlayScoreSound() { ... }
}

// ✅ 符合 SRP：每个类只有一个变化原因
class ScoreModel { int Value; void Add(int p); }        // 变化原因：计分规则
class ScoreUI { void Display(int score); }               // 变化原因：UI 设计
class ScoreAudio { void PlayCollectSound(); }            // 变化原因：音效需求
```

> ⚠️ 代价：过度拆分会导致类爆炸和调用链过长。当某个「变化原因」从未独立变化过，不需要拆。

### OCP：开闭原则

> Open for extension, closed for modification.

- 对扩展开放：新增行为时不需要改已有代码
- 对修改关闭：已有代码稳定后不应再被改动
- 实现手段：接口/抽象类 + 策略模式/模版方法模式

```csharp
// ❌ 违反 OCP：每加一种敌人就要改 switch
void SpawnEnemy(string type) {
    switch(type) {
        case "tank": ... break;
        case "drone": ... break;
        // 加新敌人 → 改这里
    }
}

// ✅ 符合 OCP：新敌人 = 新类，不改已有代码
interface IEnemy { void Spawn(); }
class TankEnemy : IEnemy { ... }
class DroneEnemy : IEnemy { ... }
```

> ⚠️ 代价：过度抽象。2-3 种变体时用 switch 更清晰，5+ 种且还在增长时才值得抽接口。

### LSP：里氏替换原则

> Subtypes must be substitutable for their base types.

- 子类应该能无缝替换父类，不破坏程序的正确性
- 违反信号：`if (obj is SpecificType) { 特殊处理… }`

```csharp
// ❌ 违反 LSP：矩形是正方形的前提不成立
class Rectangle {
    public virtual int Width { get; set; }
    public virtual int Height { get; set; }
}
class Square : Rectangle {
    public override int Width { set { base.Width = base.Height = value; } }  // 破坏了 Rectangle 的语义
}

// ✅ 符合 LSP：独立的抽象
interface IShape { int Area(); }
```

> ⚠️ 现实中最常见的违反是「空方法覆写」——子类覆写了一个方法但什么都不做。

### ISP：接口隔离原则

> Many specific interfaces are better than one general interface.

- 客户端不应该被迫依赖它不使用的方法
- 大接口拆成多个小接口，按需实现
- 判断方法：类有没有实现接口的某个方法时「空着」或「抛 NotImplementedException」？有就说明接口太大了

```csharp
// ❌ 违反 ISP
interface IUnit {
    void Move();
    void Attack();
    void Heal();
    void Fly();
}
class Soldier : IUnit { void Fly() { /* 士兵不会飞！*/ } }

// ✅ 符合 ISP
interface IMovable { void Move(); }
interface IAttacker { void Attack(); }
interface IFlyable { void Fly(); }
class Soldier : IMovable, IAttacker { ... }
```

### DIP：依赖倒转原则

> Depend on abstractions, not on concretions.

- 高层模块不依赖低层模块，两者都依赖抽象
- 具体手段：依赖注入（DI）、接口

```csharp
// ❌ 违反 DIP：Tank 直接依赖具体的 Bullet 类
class Tank {
    void Shoot() { new Bullet().Fire(); }
}

// ✅ 符合 DIP：依赖 IBullet 抽象
class Tank {
    readonly IBulletFactory _factory;
    void Shoot() { _factory.Create().Fire(); }
}
```

### 组合优于继承

> Favor object composition over class inheritance. — GoF

- 用「持有其他对象的引用 + 委托调用」替代继承链
- 继承的问题：编译时绑定、破坏封装、深层继承链难维护
- 组合的优势：运行时灵活替换、职责清晰

> ⚠️ 当「子类 是 父类的一种（is-a）」且行为差异不大时，继承是合适的。别为了「复用代码」而继承。

### 迪米特法则（最少知识原则）

> Only talk to your immediate friends.

- 一个对象应对其他对象有尽可能少的了解
- 链式调用 `a.GetB().GetC().DoSomething()` 是典型违反信号

### 实用的「不要」清单

- **不要过度设计**：一个接口只有一个实现，就不要抽接口
- **不要提前抽象**：等第二个场景出现时再考虑抽象，而不是猜未来
- **不要为了模式而模式**：如果最简单的写法已经够清晰，就用最简单的
- **防御性保留**：不确定是否该删的代码，标记 `// TODO(@owner, YYYY-MM-DD): 确认是否可删除`，超过 30 天未确认的视为可清理

## 依赖管理

- 优先用语言标准库，其次用社区最主流库（NPM 周下载量 > 100k / PyPI 月下载 > 1M 级别）
- 新增第三方库前，先检查项目是否已有类似功能的库
- 锁定版本号，避免隐式升级（package-lock.json / poetry.lock / Pipfile.lock）

## 错误处理

- 不吞异常 — 要么真正处理，要么向上传播
- 对外接口做好入参校验（类型 + 范围 + 非空）
- 关键路径加日志，但绝不暴露：秘钥、token、密码、用户隐私、API Key

## 安全红线

- 绝不硬编码任何密钥、token、密码、连接字符串
- 环境变量用 `.env` 文件管理，`.env` 加入 `.gitignore`
- 用户输入永远做校验和清洗，不信任任何外部数据
- 数据库操作使用参数化查询，杜绝 SQL 拼接

## 跨技术栈通用约定

- 文件名：多单词用 `-` 连接（kebab-case）或 `_` 连接（snake_case），按语言惯例
- 缩进：2 空格（JS/TS/YAML）或 4 空格（Python），按语言惯例
- 行尾：LF（`\n`），不要 CRLF
- 文件末尾：保留一个空行