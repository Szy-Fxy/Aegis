# Java 技术栈规范

## 环境管理

- JDK 17+（LTS），新项目优先用 JDK 21
- 构建工具：Gradle（Kotlin DSL）或 Maven，项目推荐 Gradle
- 依赖管理用 `build.gradle.kts` 或 `pom.xml`

```groovy
// build.gradle.kts
plugins {
    java
    id("org.springframework.boot") version "3.3.0"
    id("io.spring.dependency-management") version "1.1.5"
}

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
```

## 项目结构

```
project/
├── src/
│   ├── main/
│   │   ├── java/{package}/
│   │   │   ├── controller/     # REST Controller
│   │   │   ├── service/        # 业务逻辑
│   │   │   ├── repository/     # 数据访问
│   │   │   ├── model/          # 实体/ DTO
│   │   │   ├── config/         # 配置类
│   │   │   └── exception/      # 自定义异常
│   │   └── resources/
│   │       ├── application.yml
│   │       └── db/migration/   # Flyway 迁移
│   └── test/
│       └── java/{package}/
├── build.gradle.kts
├── settings.gradle.kts
├── .env.example
└── Makefile
```

## 代码风格

- 使用 Google Java Style Guide 或 Spring Java Format
- 用 Lombok 减少样板代码（`@Data`, `@Builder`, `@Slf4j`），但避免滥用 `@AllArgsConstructor`
- 用 `var`（Java 10+）简化局部变量，但类型不明显时写全称
- 常量用 `static final`，命名 SCREAMING_SNAKE_CASE
- 包名全小写，无下划线

```java
// ✅ 使用 Lombok 简化
@Data
@Builder
public class User {
    private final String id;
    private final String name;
    @Email
    private final String email;
}

// ✅ 统一异常处理
@RestControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(NotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(NotFoundException ex) {
        return ResponseEntity.status(404).body(new ErrorResponse(ex.getMessage()));
    }
}
```

## 常用库速查

| 场景 | 优先使用 | 备注 |
|------|----------|------|
| Web 框架 | Spring Boot 3.x | 生态最全 |
| ORM | Spring Data JPA / MyBatis-Plus | JPA 简单 CRUD，MyBatis 复杂查询 |
| 数据库迁移 | Flyway | 版本化迁移 |
| 序列化 | Jackson | Spring Boot 默认 |
| 数据校验 | Jakarta Validation | `@NotNull`, `@Valid` |
| 测试 | JUnit 5 + Mockito + AssertJ | Spring Boot Test |
| HTTP 客户端 | RestClient / WebClient | Spring 6 内置 |
| 缓存 | Spring Cache + Caffeine / Redis | 本地用 Caffeine，分布式用 Redis |
| 日志 | SLF4J + Logback | Spring Boot 默认 |
| API 文档 | SpringDoc OpenAPI | 替代 Swagger |
| 配置管理 | `application.yml` + `@ConfigurationProperties` | 类型安全配置 |
| 安全 | Spring Security | 认证 + 授权 |

## 测试

```bash
./gradlew test                   # Gradle
mvn test                         # Maven
```

- 单元测试：Service 层，Mock 依赖
- 集成测试：`@SpringBootTest`，Controller 用 `@WebMvcTest`
- 数据库测试：`@DataJpaTest` 或 Testcontainers

## 最佳实践

- 构造函数注入优于字段注入（`@RequiredArgsConstructor`）
- 接口不是必须的：只有一个实现时不要抽接口
- 异常不用于控制流，用于真正的异常情况
- 谨慎使用 `@Transactional`：理解其传播行为和失效场景
- Optional 只用做返回值，不用做参数或字段