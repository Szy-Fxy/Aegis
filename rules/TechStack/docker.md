# Docker 技术栈规范

## 镜像构建原则

- 使用多阶段构建（multi-stage build）减小镜像体积
- 基础镜像优先使用 `alpine` 或 `distroless` 变体
- 固定基础镜像版本，不使用 `latest` 标签
- 合理利用 Docker 层缓存：先复制依赖文件，再复制源码

```dockerfile
# ✅ 多阶段构建示例（Go）
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /app/server ./cmd/server

FROM alpine:3.20
RUN apk add --no-cache ca-certificates tzdata
COPY --from=builder /app/server /usr/local/bin/server
USER 1000:1000
ENTRYPOINT ["/usr/local/bin/server"]
```

## Dockerfile 最佳实践

- COPY 优于 ADD（除非需要自动解压 tar）
- 合并 RUN 指令减少层数（用 `&&` 连接）
- 清理包管理器缓存（`apt-get clean` / `apk cache clean`）
- 使用非 root 用户运行容器（`USER 1000`）
- 使用 `.dockerignore` 排除不必要文件

```dockerfile
# ✅ 合并 RUN + 清理
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

## Docker Compose

```yaml
# docker-compose.yml 示例
version: "3.9"
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - DATABASE_URL=postgres://user:pass@db:5432/app
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: app
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 5s
      timeout: 3s
      retries: 5

volumes:
  pgdata:
```

## 安全

- 绝不将 `.env` 文件复制到镜像中
- 不在 Dockerfile 中写 `ENV SECRET_KEY=xxx`
- 使用 Docker Secrets 或环境变量注入敏感信息
- 定期扫描镜像漏洞：`docker scan` / `trivy`
- 限制容器资源：`deploy.resources.limits` 中设置 CPU 和内存上限

## 常用命令

```bash
docker build -t {name}:{tag} .                    # 构建镜像
docker compose up -d                               # 启动服务
docker compose down                                # 停止服务
docker compose logs -f {service}                   # 查看日志
docker compose exec {service} sh                   # 进入容器
docker system prune -a                             # 清理未使用资源
docker scan {image}                                # 安全扫描
```

## 生产环境 Checklist

```
□ 使用固定版本标签（非 latest）
□ 以非 root 用户运行
□ 健康检查已配置
□ 资源限制已设置（CPU/内存）
□ 日志输出到 stdout/stderr（不写文件）
□ 敏感信息通过环境变量注入（不硬编码）
□ 镜像已通过安全扫描
□ .dockerignore 已配置
```