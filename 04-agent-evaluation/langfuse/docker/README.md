# Langfuse Docker 部署文档

> 大模型智能体评估平台 - 本地化部署完整方案

---

## 📚 文档导航

### 🚀 [快速开始.md](./快速开始.md)
**适合**: 初次使用、快速体验

**内容**:
- 5 分钟快速部署指南
- 一键生成安全配置
- SDK 集成示例（Python, OpenAI, LangChain）
- 常见问题快速解决

**开始使用**:
```bash
cd 04-agent-evaluation/langfuse/docker
# 按照"快速开始.md"操作
```

---

### 📖 [部署指南.md](./部署指南.md)
**适合**: 生产环境部署、高级配置

**内容**:
- 完整系统架构说明
- 详细环境变量配置
- 安全加固最佳实践
- 性能优化策略
- 数据备份与恢复方案
- 版本升级指南

**章节目录**:
1. 系统概述
2. 前置要求
3. 快速开始
4. 详细配置说明
5. 安全加固
6. 常见问题
7. 性能优化
8. 数据备份与恢复
9. 升级指南

---

### ⚙️ [docker-compose.yml](./docker-compose.yml)
**适合**: 理解系统架构、自定义配置

**特点**:
- ✅ 完整的中文注释
- ✅ 每个配置项详细说明
- ✅ 安全提示和最佳实践
- ✅ 面向高级学习者

**服务组件**:
- `langfuse-web`: Web 服务 (端口 3000)
- `langfuse-worker`: 后台任务处理 (端口 3030)
- `postgres`: 关系型数据库 (端口 5432)
- `clickhouse`: 列式数据库 (端口 8123, 9000)
- `redis`: 缓存和队列 (端口 6379)
- `minio`: 对象存储 (端口 9090, 9091)

---

## 🎯 使用场景选择

### 场景 1: 快速体验和学习
**推荐**: [快速开始.md](./快速开始.md)

```bash
# 1. 创建配置
cat > .env << EOF
POSTGRES_PASSWORD=testpass123
CLICKHOUSE_PASSWORD=testpass123
REDIS_AUTH=testpass123
MINIO_ROOT_PASSWORD=testpass123
ENCRYPTION_KEY=$(openssl rand -hex 32)
NEXTAUTH_SECRET=$(openssl rand -base64 32)
SALT=$(openssl rand -base64 32)
EOF

# 2. 启动服务
docker compose up -d

# 3. 访问 http://localhost:3000
```

---

### 场景 2: 开发环境部署
**推荐**: [快速开始.md](./快速开始.md) + 部分安全配置

```bash
# 1. 使用更安全的密码
# 参考"快速开始.md"的密钥生成命令

# 2. 启用自动初始化
# 在 .env 中配置 LANGFUSE_INIT_* 变量

# 3. 配置邮件服务（可选）
SMTP_CONNECTION_URL=smtp://user:pass@smtp.gmail.com:587
EMAIL_FROM_ADDRESS=noreply@yourcompany.com

# 4. 启动服务
docker compose up -d
```

---

### 场景 3: 生产环境部署
**推荐**: [部署指南.md](./部署指南.md) 完整阅读

**必须完成**:
- ✅ 修改所有默认密码和密钥
- ✅ 配置 HTTPS (Nginx/Caddy)
- ✅ 限制网络访问（防火墙）
- ✅ 启用 Redis TLS
- ✅ 配置数据备份任务
- ✅ 设置监控告警

**参考章节**:
- 安全加固
- 性能优化
- 数据备份与恢复

---

## 📋 快速参考

### 最小配置清单

```bash
# .env 文件必须配置项
POSTGRES_PASSWORD=          # PostgreSQL 密码
CLICKHOUSE_PASSWORD=        # ClickHouse 密码
ENCRYPTION_KEY=             # 64位十六进制密钥
NEXTAUTH_SECRET=            # JWT 签名密钥
SALT=                       # 加密盐值
REDIS_AUTH=                 # Redis 密码
MINIO_ROOT_PASSWORD=        # MinIO 密码 (≥8位)
```

### 密钥生成命令

```bash
# ENCRYPTION_KEY (64位十六进制)
openssl rand -hex 32

# NEXTAUTH_SECRET (Base64)
openssl rand -base64 32

# 随机密码
openssl rand -base64 24
```

### 常用命令

```bash
# 启动服务
docker compose up -d

# 查看日志
docker compose logs -f

# 停止服务
docker compose down

# 重启服务
docker compose restart

# 查看服务状态
docker compose ps

# 更新镜像
docker compose pull && docker compose up -d
```

### 访问地址

| 服务 | 地址 | 说明 |
|------|------|------|
| **Langfuse Web** | http://localhost:3000 | 主界面 |
| **MinIO Console** | http://localhost:9091 | 对象存储管理 |
| **Health Check** | http://localhost:3000/api/public/health | 健康检查 |

---

## 🎓 学习路径

### 初学者路径
1. ✅ 阅读 [快速开始.md](./快速开始.md)
2. ✅ 本地部署 Langfuse
3. ✅ 运行 SDK 集成示例
4. ✅ 探索 Web UI 功能
5. ✅ 查看 [docker-compose.yml](./docker-compose.yml) 注释理解架构

### 进阶路径
1. ✅ 阅读 [部署指南.md](./部署指南.md) 全文
2. ✅ 理解每个组件的作用和配置
3. ✅ 配置生产环境安全加固
4. ✅ 实施性能优化
5. ✅ 设置自动备份和监控

### 专家路径
1. ✅ 深入研究 [docker-compose.yml](./docker-compose.yml) 每个配置项
2. ✅ 自定义网络和资源限制
3. ✅ 集成 Kubernetes 部署
4. ✅ 实现高可用架构
5. ✅ 贡献社区最佳实践

---

## 🔗 相关资源

### 官方资源
- [Langfuse 官网](https://langfuse.com)
- [官方文档](https://langfuse.com/docs)
- [GitHub 仓库](https://github.com/langfuse/langfuse)
- [Docker 部署指南](https://langfuse.com/self-hosting/deployment/docker-compose)

### SDK 文档
- [Python SDK](https://langfuse.com/docs/sdk/python)
- [JavaScript/TypeScript SDK](https://langfuse.com/docs/sdk/typescript)
- [OpenAI SDK 集成](https://langfuse.com/docs/integrations/openai)
- [LangChain 集成](https://langfuse.com/docs/integrations/langchain)
- [LlamaIndex 集成](https://langfuse.com/docs/integrations/llama-index)

### 社区支持
- [Discord 社区](https://discord.gg/7NXusRtqYU)
- [GitHub Discussions](https://github.com/langfuse/langfuse/discussions)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/langfuse)

---

## 📊 系统要求

### 最小配置
- **CPU**: 4 核
- **内存**: 8GB
- **磁盘**: 100GB
- **网络**: 10Mbps

### 推荐配置
- **CPU**: 8 核
- **内存**: 16GB
- **磁盘**: 200GB SSD
- **网络**: 100Mbps

### 高负载配置
- **CPU**: 16 核
- **内存**: 32GB
- **磁盘**: 500GB NVMe SSD
- **网络**: 1Gbps

---

## ⚠️ 重要提示

### 安全警告

> ⚠️ **生产环境部署前必读**
> 
> 本配置的默认密码仅供测试使用！
> 
> 生产环境部署时**必须**修改以下配置:
> - `POSTGRES_PASSWORD`
> - `CLICKHOUSE_PASSWORD`
> - `REDIS_AUTH`
> - `MINIO_ROOT_PASSWORD`
> - `ENCRYPTION_KEY`
> - `NEXTAUTH_SECRET`
> - `SALT`
> 
> 参考 [部署指南.md](./部署指南.md) 的"安全加固"章节。

### 数据持久化

> 💾 **数据保护**
> 
> 默认配置使用 Docker Volumes 存储数据。
> 
> **停止服务时不要使用 `-v` 参数**:
> ```bash
> docker compose down     # ✅ 正确 - 保留数据
> docker compose down -v  # ❌ 错误 - 删除所有数据！
> ```
> 
> 定期备份数据，参考"数据备份与恢复"章节。

---

## 🤝 贡献

欢迎改进本文档！

### 如何贡献
1. 发现错误或改进点
2. 提交 Issue 或 Pull Request
3. 分享您的部署经验

### 反馈渠道
- GitHub Issues
- 项目讨论区
- 邮件联系

---

## 📝 版本信息

| 项目 | 版本 | 更新日期 |
|------|------|---------|
| Langfuse | v3 | 2025-01 |
| Docker Compose | 2.0+ | - |
| PostgreSQL | 17 | - |
| ClickHouse | Latest | - |
| Redis | 7 | - |
| MinIO | Latest | - |

---

## 📄 许可证

本文档采用 MIT 许可证。Langfuse 项目采用 MIT 许可证。

---

## 🎉 开始使用

选择适合您的文档开始：

- 🚀 **快速体验**: [快速开始.md](./快速开始.md)
- 📖 **完整部署**: [部署指南.md](./部署指南.md)
- ⚙️ **深入理解**: [docker-compose.yml](./docker-compose.yml)

**祝您使用愉快！**

