# Rust 技术栈规范

## 环境管理

```bash
# 使用 rustup 管理工具链
rustup update stable
rustup component add clippy rustfmt

# 项目初始化
cargo new {project}             # 新项目
cargo init                      # 在当前目录初始化

# 依赖管理
cargo add {crate}               # 添加依赖
cargo add -D {crate}            # 添加开发依赖
cargo update                    # 更新依赖
```

## 项目结构

```
project/
├── src/
│   ├── main.rs                 # 入口
│   ├── lib.rs                  # 库根
│   ├── config.rs               # 配置
│   ├── error.rs                # 错误类型定义
│   ├── models/                 # 数据模型
│   ├── services/               # 业务逻辑
│   └── handlers/               # HTTP/gRPC handler
├── tests/
│   └── integration_test.rs     # 集成测试
├── migrations/                 # 数据库迁移
├── Cargo.toml
├── Cargo.lock
├── .env.example
├── rust-toolchain.toml         # 固定工具链版本
└── Makefile
```

## 代码风格

- 使用 `rustfmt` 自动格式化，`cargo fmt`
- 使用 `clippy` 检查代码质量，`cargo clippy -- -D warnings`
- 遵循 Rust API Guidelines
- 类型命名：PascalCase（`UserService`）
- 变量/函数命名：snake_case（`user_id`, `get_user`）
- 常量：SCREAMING_SNAKE_CASE（`MAX_RETRIES`）
- 全面使用 `Result<T, E>` 和 `Option<T>`，避免 `unwrap()` 和 `expect()`（除非能证明不会 panic）

```rust
// ✅ 定义专用错误类型
#[derive(Debug, thiserror::Error)]
pub enum AppError {
    #[error("not found: {0}")]
    NotFound(String),
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
}

// ✅ 使用 ? 传播错误
pub async fn get_user(id: Uuid, pool: &PgPool) -> Result<User, AppError> {
    sqlx::query_as::<_, User>("SELECT * FROM users WHERE id = $1")
        .bind(id)
        .fetch_optional(pool)
        .await?
        .ok_or(AppError::NotFound(id.to_string()))
}
```

## 常用库速查

| 场景 | 优先使用 | 备注 |
|------|----------|------|
| 异步运行时 | `tokio` | 生态最全 |
| HTTP 框架 | `axum` | 基于 tokio + tower |
| HTTP 客户端 | `reqwest` | 同步 + 异步 |
| 数据库 ORM | `sqlx` | 编译时 SQL 检查 |
| 序列化 | `serde` + `serde_json` | 事实标准 |
| 错误处理 | `thiserror` + `anyhow` | 库用 thiserror，应用用 anyhow |
| 日志 | `tracing` | 结构化日志 |
| 配置管理 | `config` | 支持多种格式 |
| 测试 | 内置 `#[test]` + `tokio::test` | 标准库已够用 |
| CLI | `clap` | 参数解析 |
| JWT | `jsonwebtoken` | 主流选择 |
| 数据校验 | `validator` | 派生宏校验 |
| 时间处理 | `chrono` / `time` | chrono 常用，time 更现代 |

## 测试

```bash
cargo test                      # 运行全部测试
cargo test -- --nocapture       # 显示测试输出
cargo tarpaulin                 # 覆盖率（需安装 cargo-tarpaulin）
```

## 所有权与借用

- 函数参数优先使用引用（`&T`），除非需要所有权
- 避免过早引入 `Arc<Mutex<T>>`，先尝试重构为更清晰的所有权模型
- `Clone` 不是免费的，留意大数据的隐式 clone
- 生命周期标注：编译器能推导就不要手写，只有必要时才加

```rust
// ✅ 优先借用
fn process(data: &[u8]) -> Result<(), Error> { ... }

// ✅ 需要所有权时明确
fn store(data: Vec<u8>) -> Result<(), Error> { ... }
```