# Unreal Engine / C++ 游戏开发规范

## 架构分层

```
Blueprint (表现层) → 事件绑定、动画、特效、UI
      ↕ UFUNCTION / UPROPERTY 接口
C++ (逻辑层)      → 核心逻辑、数据结构、状态管理、网络
```

- C++ 写核心逻辑，Blueprint 处理表现
- C++ 暴露 `BlueprintCallable` / `BlueprintAssignable` 接口给 BP
- 不在 Blueprint 中实现核心业务逻辑

## 命名规范

| 类型 | 前缀 | 示例 |
|------|------|------|
| Actor | A | `APetGuideActor` |
| Component | U | `UHealthComponent` |
| Interface | I | `IInteractable` |
| Enum | E | `EPetGuideState` |
| Struct | F | `FPetAnimParams` |
| Blueprint 资源 | BP_ | `BP_PetGuide` |
| Widget | WBP_ | `WBP_MainHUD` |
| DataAsset | DA_ | `DA_PlayerConfig` |

## UPROPERTY / UFUNCTION 修饰规范

```cpp
// 暴露给 BP 的属性
UPROPERTY(BlueprintReadOnly, Category = "Pet Guide")
float DialogueDistance = 150.0f;

// 暴露给 BP 的函数
UFUNCTION(BlueprintCallable, Category = "Pet Guide")
void SetWaypointActor(AActor* NewWaypoint);

// BP 可绑定的事件
UPROPERTY(BlueprintAssignable, Category = "Pet Guide")
FPetGuideEvent OnPreTeleport;

// BP 可实现的接口
UFUNCTION(BlueprintNativeEvent, Category = "Pet Guide")
void OnStateChanged(EPetGuideState NewState);
```

## 文件组织

```
Source/{ModuleName}/
├── Public/
│   ├── {ClassName}.h
│   └── {ModuleName}Module.h
├── Private/
│   ├── {ClassName}.cpp
│   └── {ModuleName}Module.cpp
└── {ModuleName}.Build.cs
```

## 修改流程

1. 先改 `.h` 声明，再改 `.cpp` 实现
2. 更新 `.Build.cs` 依赖（如需要）
3. 编译验证：
   - Windows: `GenerateProjectFiles.bat` → VS Build
   - Mac/Linux: `GenerateProjectFiles.sh` → Xcode / CLion Build
4. 删文件前确认无 C++ 引用 + 通知用户检查 BP 引用（`.uasset` 是二进制，AI 无法检查）

## 状态管理

- 有限状态机（FSM）+ 策略模式管理 Actor 复杂状态
- 删除/修改 API 先用 `DEPRECATED` 宏标记做过渡期
- 组件引用用 `UPROPERTY()` 保持，避免手动 `CastTo`

## 内存与指针

```cpp
// 组件引用 —— 用 UPROPERTY 防止 GC
UPROPERTY()
USkeletalMeshComponent* MeshComp;

// 弱引用 —— 防止悬空
TWeakObjectPtr<AActor> TargetActor;

// 智能指针 —— 非 UObject 对象
TUniquePtr<FPetIdleStrategy> IdleStrategy;
TSharedPtr<FGameData> GameData;

// 委托
DECLARE_DELEGATE(FOnComplete);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FPetGuideEvent, APetGuideActor*, Pet);
```

## 常见陷阱

| 陷阱 | 正确做法 |
|------|----------|
| UObject 裸指针被 GC 回收 | 用 `UPROPERTY()` 标记 |
| `CastTo` 失败未判空 | 判空并处理失败情况 |
| Tick 中做重计算 | 用 Timer 或移到其他线程 |
| 删 C++ 文件忘记 BP 引用 | 通知用户在编辑器 Reference Viewer 检查 |
| 跨模块引用未加依赖 | 在 `.Build.cs` 中 `PublicDependencyModuleNames.Add()` |