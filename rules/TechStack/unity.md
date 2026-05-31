# Unity / C# 游戏开发规范

## 架构分层

```
MonoBehaviour (表现层)       → UI、动画、音效、场景交互
       ↕ 接口 / 事件
ScriptableObject / Service  → 数据、配置、核心逻辑、状态管理
```

- 核心逻辑不放 MonoBehaviour，放在独立的 Service / System 类
- ScriptableObject 做数据容器（配置、道具属性、技能参数等）
- MonoBehaviour 只负责场景中的具体行为（移动、动画触发、碰撞响应）

## 命名规范

| 类型 | 前缀 | 示例 |
|------|------|------|
| 成员变量 | `_camelCase` | `_health`, `_moveSpeed` |
| 静态变量 | `s_` | `s_instance` |
| 常量 | 全大写下划线 | `MAX_PLAYER_COUNT` |
| 方法 | PascalCase | `TakeDamage()` |
| 接口 | `I` 前缀 | `IDamageable` |
| 枚举 | 无前缀 | `PlayerState` |
| 事件 | `On` 前缀 | `OnHealthChanged` |
| 资源文件夹区分 | 按目录归类 | `ScriptableObjects/`, `Prefabs/`, `Scenes/` |

## 引用规则

```csharp
// ✅ 用 SerializeField + 拖拽赋值，避免 GetComponent/Find
[SerializeField] private HealthBar _healthBar;

// ✅ 用 TryGetComponent 替代 GetComponent（防止漏引用报错）
if (TryGetComponent<Rigidbody>(out var rb)) { ... }

// ✅ 组件缓存：Awake 时获取，存为成员变量
private Rigidbody _rb;
private void Awake() => _rb = GetComponent<Rigidbody>();

// ❌ 避免 GameObject.Find / FindObjectOfType（性能差、易断）
// ❌ 避免在 Update 中 GetComponent（每帧都查，性能灾难）
// ❌ 避免过多的 GetComponent 链式调用：GetComponent<A>().GetComponent<B>()
```

## 常用 API 约定

| 场景 | 方式 | 备注 |
|------|------|------|
| 加载资源 | `Addressables` 或 `Resources.Load<T>()` | Addressables 优先 |
| 对象池 | `ObjectPool<T>` / 自定义池 | 频繁创建/销毁的对象必须用池 |
| 事件系统 | C# `event Action` + `UnityEvent` | Action 用于 C# 内部，UnityEvent 用于 Inspector 连线 |
| 协程 | `StartCoroutine` / `StopCoroutine` | 注意 MonoBehaviour 销毁时协程自动停止 |
| 异步 | `async/await` + `UniTask` | 如果项目已引入 UniTask，优先用它替代协程 |
| 场景加载 | `SceneManager.LoadSceneAsync` | 异步加载，不阻塞主线程 |
| 输入 | `Input System` 新版 | 不推荐旧 Input Manager |

## Build / 编辑器

- 打包前先清理 `Library/` 和 `Temp/` 目录
- 修改 `.asmdef` 后必须重新生成项目文件
- 编译验证：Unity Editor → Console → Clear → Recompile
- 命令行构建：
  ```bash
  "Unity.exe" -quit -batchmode -projectPath . -executeMethod Builder.Build -logFile build.log
  ```

## 常见陷阱

| 陷阱 | 正确做法 |
|------|----------|
| `Destroy(gameObject)` 后继续访问 | 先判空 `if (gameObject != null)` |
| `OnDestroy` 中访问已销毁的引用 | 在 `OnDisable` 中清理引用 |
| 协程在对象销毁后继续执行 | 用 `CancellationToken` 或判空 |
| `Update` 中频繁 `GameObject.Find` | 在 `Awake`/`Start` 缓存引用 |
| `transform.position` 直接赋值 | 优先用 `Rigidbody.MovePosition` |