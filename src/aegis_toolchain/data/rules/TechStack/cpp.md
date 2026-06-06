# 通用 C++ 开发规范

> 适用于非 UE 的通用 C++ 项目（桌面应用、服务端、工具、算法库等）。
> 如果项目是 Unreal Engine 游戏开发，请同时参考 [unreal.md](unreal.md)。

## 构建系统

- 新项目优先用 **CMake**（跨平台、生态最广）
- 包管理：**vcpkg**（微软维护，跨平台）或 **Conan**（更灵活）
- 编译器：GCC 13+ / Clang 17+ / MSVC 2022+，开启 C++20 或 C++23

## 项目结构

```
project/
├── src/
│   ├── main.cpp
│   ├── core/                 # 核心逻辑
│   ├── utils/                # 工具函数
│   └── models/               # 数据结构
├── include/                  # 公共头文件
│   └── project/
├── tests/
│   ├── CMakeLists.txt
│   └── test_core.cpp
├── CMakeLists.txt
├── vcpkg.json               # 或 conanfile.txt
└── README.md
```

## 命名规范

| 类型 | 约定 | 示例 |
|------|------|------|
| 类 / 结构体 | PascalCase | `PlayerController` |
| 函数 / 方法 | PascalCase | `CalculateDamage()` |
| 变量 | snake_case | `player_health` |
| 成员变量 | `_` 后缀 | `health_`, `name_` |
| 常量 | kPascalCase 或 UPPER_SNAKE | `kMaxPlayers`, `MAX_PLAYERS` |
| 命名空间 | snake_case | `project::core` |
| 宏 | UPPER_SNAKE_CASE | `PROJECT_VERSION` |
| 文件名 | snake_case | `player_controller.h`, `player_controller.cpp` |

## 现代 C++ 约定

```cpp
// ✅ 智能指针，不用裸 new/delete
auto player = std::make_unique<Player>();
auto shared = std::make_shared<Config>();

// ✅ 用 nullptr，不用 NULL 或 0
Player* p = nullptr;

// ✅ 用 auto 简化类型
auto it = players.find(id);

// ✅ 用 range-based for
for (const auto& player : players) { ... }

// ✅ 用 enum class，不用裸 enum
enum class State { Idle, Running, Dead };

// ✅ 用 std::optional 表示可能无值
std::optional<Player> find_player(int id);

// ✅ 用 std::expected (C++23) 或 std::variant 做错误处理
std::expected<Player, Error> load_player(std::string_view path);

// ✅ 用 constexpr 编译期计算
constexpr int factorial(int n) { return n <= 1 ? 1 : n * factorial(n - 1); }

// ❌ 不写裸 new / delete
// ❌ 不用 C 风格转换 (int)x，用 static_cast<int>(x)
// ❌ 不写 using namespace std; 在头文件中
```

## CMakeLists.txt 最小模板

```cmake
cmake_minimum_required(VERSION 3.21)
project(MyProject VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_executable(my_project
    src/main.cpp
    src/core/engine.cpp
)

target_include_directories(my_project PUBLIC include)
target_compile_options(my_project PRIVATE -Wall -Wextra -Wpedantic)

# 测试
enable_testing()
add_subdirectory(tests)
```

## 常用库

| 场景 | 使用 | 备注 |
|------|------|------|
| 测试 | `GoogleTest` / `Catch2` | 根据项目风格选择 |
| 日志 | `spdlog` | 异步、高性能 |
| JSON | `nlohmann/json` | 头文件 only，易集成 |
| HTTP 客户端 | `cpp-httplib` / `libcurl` | httplib 轻量，curl 功能全 |
| 数据库 | `sqlite_orm` (SQLite) / `mysql-connector-cpp` | 按需 |
| CLI 参数 | `CLI11` | 头文件 only |
| 序列化 | `protobuf` / `msgpack` | 跨语言通信用 |
| 数学计算 | `Eigen` | 线性代数 / 矩阵运算 |

## 编译与测试

```bash
# 配置
cmake -B build -DCMAKE_BUILD_TYPE=Debug

# 构建
cmake --build build -j$(nproc)

# 测试
cd build && ctest --output-on-failure

# 发布构建
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build -j$(nproc)
```

## 常见陷阱

| 陷阱 | 正确做法 |
|------|----------|
| 悬空引用（返回局部变量引用） | 返回值，不要返回引用 |
| 忘记虚析构函数 | 有虚函数的基类必须写 `virtual ~Base() = default;` |
| 头文件中 `using namespace` | 绝对禁止，污染所有包含者 |
| 循环引用（两个头文件互相 include） | 用前向声明 + 在 .cpp 中 include |
| 未初始化变量 | 永远给初始值 `int x = 0;` |
| 多线程数据竞争 | 用 `std::mutex` / `std::atomic`，不要裸写 |