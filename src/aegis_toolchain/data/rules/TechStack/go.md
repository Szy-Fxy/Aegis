# Go 技术栈规范

## 环境管理

```bash
# Go 模块初始化
go mod init github.com/{org}/{project}

# 依赖管理
go get {package}              # 添加依赖
go get -u {package}           # 更新依赖
go mod tidy                    # 清理未使用依赖
go mod vendor                  # 将依赖复制到 vendor 目录
```

## 项目结构

```
project/
├── cmd/
│   └── {app_name}/
│       └── main.go            # 入口文件
├── internal/                   # 私有包（不可被外部引用）
│   ├── handler/               # HTTP/gRPC handler
│   ├── service/               # 业务逻辑层
│   ├── repository/            # 数据访问层
│   └── model/                 # 数据模型
├── pkg/                        # 可被外部引用的公共库
├── api/                        # API 定义（proto / OpenAPI）
├── configs/                    # 配置文件
├── scripts/                    # 构建/部署脚本
├── go.mod
├── go.sum
├── .env.example
└── Makefile
```

## 代码风格

- 使用 `gofmt` 或 `goimports` 自动格式化
- 遵循 Effective Go 和 Go Code Review Comments
- 变量命名：驼峰式，缩写全大写（`userID` 不是 `userId`）
- 错误处理：永远不忽略 error，用 `errors.Wrap` 添加上下文
- 包名：小写、单数、简短、无下划线

```go
// ✅ 正确的错误处理
func GetUser(id string) (*User, error) {
    user, err := repo.FindByID(id)
    if err != nil {
        return nil, fmt.Errorf("GetUser: %w", err)
    }
    return user, nil
}

// ✅ 接口定义在使用方，不是实现方
type UserRepository interface {
    FindByID(id string) (*User, error)
    Save(user *User) error
}
```

## 常用库速查

| 场景 | 优先使用 | 备注 |
|------|----------|------|
| HTTP 路由 | `chi` / 标准库 `net/http` | chi 轻量且兼容标准库 |
| HTTP 客户端 | 标准库 `net/http` | 大多数场景够用 |
| gRPC | `google.golang.org/grpc` | 官方实现 |
| 数据库 ORM | `sqlx` / `sqlc` | sqlc 编译时生成代码 |
| 数据库迁移 | `golang-migrate` | 主流选择 |
| 配置管理 | `viper` | 支持多种格式 |
| 日志 | `zerolog` / `slog`（Go 1.21+） | 结构化日志 |
| 测试 | 标准库 `testing` + `testify` | testify 提供 assert/mock |
| 数据校验 | `go-playground/validator` | 结构体 tag 校验 |
| 任务队列 | `asynq`（Redis 后端） | 分布式任务队列 |
| WebSocket | `gorilla/websocket` | 主流选择 |
| CLI | `cobra` | 命令行工具框架 |

## 测试

```bash
go test ./...                    # 运行全部测试
go test -v -race ./...           # 竞态检测
go test -coverprofile=coverage.out ./...  # 覆盖率
```

## 并发

- Goroutine 生命周期必须管理：每次 `go func()` 前确认它如何退出
- 用 `context.Context` 传递取消信号和超时
- Channel 首选单向声明（`<-chan` / `chan<-`）
- `sync.WaitGroup` 等待 goroutine 结束
- 避免共享内存，用 channel 通信（「Do not communicate by sharing memory」）

```go
func worker(ctx context.Context, wg *sync.WaitGroup, jobs <-chan Job) {
    defer wg.Done()
    for {
        select {
        case <-ctx.Done():
            return
        case job, ok := <-jobs:
            if !ok {
                return
            }
            process(job)
        }
    }
}
```