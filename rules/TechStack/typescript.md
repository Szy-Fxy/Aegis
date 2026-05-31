# TypeScript / Node.js 全栈开发规范

## 技术选型

- 新项目默认 TypeScript + Node.js
- 高性能场景考虑 Rust / Go
- 桌面工具：Electron（成熟）或 Tauri（轻量）
- 快速原型：先用 Python 脚本验证，再决定是否工程化

## 项目结构

```
project/
├── src/
│   ├── index.ts                # 入口
│   ├── config/                 # 配置（环境变量、常量）
│   ├── services/               # 业务服务层
│   ├── models/                 # 数据模型 / 类型定义
│   ├── middleware/              # Express/Fastify 中间件
│   ├── routes/                 # 路由（Web 项目）
│   └── utils/                  # 工具函数
├── tests/
│   ├── unit/
│   └── integration/
├── package.json
├── tsconfig.json
├── .eslintrc.cjs
├── .prettierrc
└── .env.example
```

## 命名

| 类型 | 约定 | 示例 |
|------|------|------|
| 文件名 | kebab-case | `user-service.ts` |
| 类 / 接口 | PascalCase | `UserService`, `IConfig` |
| 函数 / 变量 | camelCase | `getUserById`, `userName` |
| 常量 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| 私有成员 | `#` 前缀（ES2022+）或 `private` | `#cache`, `private logger` |
| 类型文件 | `*.types.ts` | `user.types.ts` |

## 类型

```typescript
// 优先用 interface，需要联合类型 / 交叉类型时才用 type
interface PlayerConfig {
  name: string;
  health: number;
  inventory: Item[];
}

// 不用 any，不确定用 unknown
function parse(raw: unknown): PlayerConfig {
  // 必须做类型守卫
  if (typeof raw !== "object" || raw === null) throw new Error("Invalid");
  return raw as PlayerConfig;
}

// 善用工具类型
type PlayerUpdate = Partial<PlayerConfig>;       // 全部可选
type PlayerSummary = Pick<PlayerConfig, "name">; // 只取部分字段
type ReadonlyPlayer = Readonly<PlayerConfig>;    // 全部只读
```

## 常用库

| 场景 | 使用 | 备注 |
|------|------|------|
| Web 框架 | `Fastify`（性能） / `Hono`（边缘） | Express 仅用于维护已有项目 |
| ORM | `Prisma` / `Drizzle` | Prisma 生态成熟，Drizzle 更轻量 |
| 数据校验 | `zod` | 类型推导 + 运行时校验一体 |
| 测试 | `vitest` | 替代 Jest，更快 |
| Lint | `eslint` + `prettier` | 或 `biome` 一站式 |
| 环境变量 | `dotenv` / `dotenv-cli` | 或 `process.loadEnvFile()` (Node 21+) |
| 日志 | `pino` | 高性能结构化日志 |
| HTTP 客户端 | `ky` / `undici` | Node 18+ 内置 fetch |
| 定时任务 | `node-cron` | 简单定时 |
| 数据库 | `postgres`（驱动） | 不用 pg 直接用，配合 Drizzle/Prisma |

## 命令

```bash
npm run dev         # 启动开发服务器
npm run build       # 构建生产版本
npm run test        # 运行测试
npm run lint        # 检查代码风格
npm run typecheck   # 类型检查（tsc --noEmit）
npm run format      # 格式化代码
```

## tsconfig.json 最小配置

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noEmit": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

## 常见陷阱

| 陷阱 | 正确做法 |
|------|----------|
| `any` 泛滥 | 用 `unknown` + 类型守卫 |
| 忘记处理 Promise rejection | 统一用 `try/catch` 或全局 `unhandledRejection` 处理 |
| 回调地狱 | 用 `async/await` |
| `console.log` 打敏感信息 | 用 `pino` 结构化日志，过滤敏感字段 |
| `import` 路径地狱 | 配置 `tsconfig.json` 的 `paths` 别名 |