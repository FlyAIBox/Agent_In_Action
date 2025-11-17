# 🎛️ 容器化部署操作手册

本手册帮助你快速理解并使用本项目的前后端 Dockerfile，完成本地或生产环境的容器化部署。

---

## 0. 快速开始（强烈推荐）

1) 在后端目录准备环境变量文件：

```bash
cd 03-agent-build-docker-deploy/backend
cp env.example .env
# 编辑 .env，填入 OPENAI_API_KEY 等必需配置
```

2) 返回项目目录并启动：

```bash
cd ..
docker compose -f docker-compose.yml up -d --build
```

3) 访问：前端 `http://localhost:8501`，后端健康检查 `http://localhost:8080/health`

> 注意：容器内访问另一容器的服务，不能使用 `localhost`，应使用 Compose 服务名（如 `http://backend:8080`）。

---

## 1. 环境准备

| 项目 | 说明 |
| ---- | ---- |
| Docker | 确保已安装最新版 Docker Engine |
| Docker Compose | 推荐使用内置的 Compose V2（`docker compose` 命令） |
| 项目源码 | 克隆仓库并切换到 `03-agent-build-docker-deploy/` 目录 |
| 环境变量 | 在项目根目录准备 `.env` 文件，至少包含 LLM、和风天气、高德等密钥 |

`.env` 示例：

```bash
OPENAI_API_KEY=your_openai_style_key
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat

QWEATHER_API_KEY=your_qweather_key
QWEATHER_API_BASE=https://api.qweather.com
QWEATHER_GEO_BASE=https://geoapi.qweather.com
```

> ⚠️ 生产环境请使用安全的秘钥管理方式（CI/CD Secret、KMS 等），避免直接在仓库中提交 `.env`。

---

## 2. 后端 Dockerfile（`backend/Dockerfile`）

```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p results

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "api_server.py"]
```

**要点说明**

- 基于 `python:3.10-slim`，仅安装必要系统依赖（`curl`）用于健康检查。
- 先复制 `requirements.txt` 并安装依赖，利用 Docker 层缓存提升重复构建速度。
- 将项目代码复制到 `/app`，提前创建 `results/` 目录，避免运行时缺失。
- 健康检查调用 `/health`，便于 Compose/容器平台监控服务状态。
- 默认通过 `python api_server.py` 启动 FastAPI，监听 8080 端口。

---

## 3. 前端 Dockerfile（`frontend/Dockerfile`）

```dockerfile
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**要点说明**

- 统一使用 `python:3.10-slim`，与后端保持一致。
- 将 Streamlit 应用监听地址设置为 `0.0.0.0`，方便容器外访问。
- 健康检查调用 `_stcore/health`，确保 Streamlit 服务可用。

---

## 4. Docker Compose（`docker-compose.yml`）

核心配置：

- **backend**：  
  - 构建目录 `./backend`，注入环境变量（LLM、和风天气、高德、汇率）。  
  - 将宿主机 `./results` 挂载到容器 `/app/results`，方便查看输出。  
  - 健康检查引用 `/health`，确保服务正常。  
  - 通过 `env_file: ./backend/.env` 注入密钥（推荐）。  
- **frontend**：  
  - 构建目录 `./frontend`，暴露 8501 端口。  
  - `API_BASE_URL` 指向 Compose 内部的 `backend` 服务（例如：`http://backend:8080`）。  
- **网络与卷**：  
  - 自定义桥接网络 `travel-network`，保证服务互联。  
  - 使用命名卷 `results` 或本地挂载存储规划结果。

完整文件已包含在仓库中，可根据部署环境调整端口与环境变量。

示例关键片段（已在仓库提供）：

```yaml
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    env_file:
      - ./backend/.env  # 从后端目录读取密钥与配置
    networks:
      - travel-network

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "8501:8501"
    environment:
      - API_BASE_URL=http://backend:8080  # 通过服务名访问后端
    depends_on:
      - backend
    networks:
      - travel-network

networks:
  travel-network:
    driver: bridge
```

---

## 5. 部署步骤

### 5.1 复制并填写 `.env`

```bash
cp env.example .env  # 若尚未创建
```

编辑 `.env`，填入实际密钥。部署时确保与 Compose 引用的变量一致。

### 5.2 （可选）单独构建与调试

> 重要：在容器内访问另一个容器的服务时，不能使用 `http://localhost:8080`。`localhost` 在容器内指向的是容器自身。应当通过 Docker 网络中的“容器名/服务名”访问，例如 `http://travel-backend:8080` 或在 Compose 中使用 `http://backend:8080`。

- **后端**
  ```bash
  cd backend
  docker build -t travel-backend .
  docker run --rm -p 8080:8080 \
    --env-file .env \
    -v $(pwd)/results:/app/results \
    travel-backend
  ```

- **前端**
  ```bash
  cd frontend
  docker build -t travel-frontend .
  # 创建用户定义网络（若尚未创建）
  docker network create travel-net || true

  # 先在同一网络中启动后端（如果未用 compose）
  docker run -d --name travel-backend --network travel-net -p 8080:8080 \
    --env-file ../backend/.env \
    -v $(pwd)/../backend/results:/app/results \
    travel-backend

  # 启动前端，并通过环境变量指向后端容器名
  docker run --rm --name travel-frontend --network travel-net -p 8501:8501 \
    -e API_BASE_URL=http://travel-backend:8080 \
    travel-frontend
  ```

### 5.3 使用 Compose 启动全栈

在项目根目录执行：

```bash
docker compose -f docker-compose.yml up --build
```

后台运行：

```bash
docker compose -f docker-compose.yml up -d --build
```

### 5.4 验证服务

| 项目 | 地址 |
| ---- | ---- |
| 前端界面 | http://localhost:8501 |
| 后端健康检查 | http://localhost:8080/health |
| OpenAPI 文档 | http://localhost:8080/docs |

查看日志：

```bash
docker compose -f docker-compose.yml logs -f
```

### 5.5 维护与关闭

- 更新代码后重建：

  ```bash
  docker compose -f docker-compose.yml build --no-cache
  docker compose -f docker-compose.yml up -d
  ```

- 停止并移除容器：

  ```bash
  docker compose -f docker-compose.yml down
  ```

---

## 6. 常见问题排查

| 问题 | 可能原因与解决建议 |
| ---- | ------------------ |
| `/health` 返回 warning | 检查 `OPENAI_API_KEY` 是否配置；确认 `.env` 已被 Compose 读取 |
| 构建失败 / 依赖安装慢 | 留意网络环境，可配置代理或使用镜像源；查看 `pip` 错误日志 |
| 端口冲突 | 调整 `docker-compose.yml` 中的 `ports` 映射 |
| API 调用失败 | 确认外部服务密钥有效，检查容器内是否能访问目标域名 |
| 前端无法调用后端 | 在容器内不要使用 `localhost`；使用 `http://backend:8080`（Compose 服务名）或 `http://<后端容器名>:8080`（自建网络） |
| 后端提示缺少 OPENAI_API_KEY | 在 `./backend/` 目录下复制并填写 `.env`：`cp env.example .env`，或在 Compose 中配置 `env_file: ./backend/.env` |
| Compose 没有读取 `.env` | 确认路径为 `./backend/.env`（相对 compose 文件所在目录），并重启：`docker compose down && docker compose up -d --build` |

---

## 7. 下一步建议

- 使用 CI/CD（如 GitHub Actions）自动构建并推送镜像到镜像仓库。  
- 在生产环境结合 Kubernetes、Swarm 等编排工具实现弹性扩缩。  
- 配置日志与监控（ELK、Prometheus）以便及时追踪 Agent 运行状态。  
- 针对业务需求扩展环境变量与容器参数（如代理设置、日志挂载等）。

---

## 8. 附录：Docker 基础知识速览

### 8.1 Docker 核心概念

- **镜像（Image）**：一个只读的模板，包含运行应用所需的代码、运行时和系统依赖。  
- **容器（Container）**：镜像的运行实例，生命周期可启动/停止/重启。  
- **Dockerfile**：定义镜像构建步骤的脚本文件，由一系列指令组成。  
- **Docker Compose**：基于 YAML 的多容器编排工具，可一次性启动/管理多个服务。  

### 8.2 常用命令速查

```bash
# 查看 Docker 版本与信息
docker version
docker info

# 镜像相关
docker images                    # 列出本地镜像
docker build -t name:tag .       # 从 Dockerfile 构建镜像
docker pull repo/name:tag        # 拉取远程镜像
docker push repo/name:tag        # 推送镜像到仓库
docker rmi image_id              # 删除镜像

# 容器相关
docker ps                        # 列出正在运行的容器
docker ps -a                     # 列出所有容器
docker run --name myapp image    # 启动容器
docker stop container_id         # 停止容器
docker logs -f container_id      # 查看实时日志
docker exec -it container_id sh  # 进入容器交互终端
docker rm container_id           # 删除容器

# Compose 相关（推荐使用 docker compose V2）
docker compose up -d             # 后台启动所有服务
docker compose down              # 停止并移除所有服务
docker compose logs -f service   # 查看指定服务日志
docker compose build             # 重新构建服务镜像
```

### 8.3 Dockerfile 编写基础

常见指令：

| 指令 | 作用 |
| ---- | ---- |
| `FROM` | 指定基础镜像 |
| `WORKDIR` | 设置工作目录 |
| `RUN` | 在镜像构建阶段执行命令 |
| `COPY` / `ADD` | 拷贝文件到镜像 |
| `ENV` | 设置环境变量 |
| `EXPOSE` | 声明容器要监听的端口（非强制） |
| `HEALTHCHECK` | 定义健康检查命令 |
| `CMD` / `ENTRYPOINT` | 定义容器启动时默认执行的命令 |

编写建议：

- 尽量使用精简基础镜像（如 `python:3.10-slim`）。  
- 先复制 `requirements.txt` 再安装依赖，利用缓存提高构建速度。  
- 使用 `--no-cache-dir`、清理包管理器缓存减少镜像体积。  
- `CMD` 与 `ENTRYPOINT` 可配合 `exec` 语法（数组形式）提升兼容性。  

### 8.4 Docker Compose 基础

常见字段：

| 字段 | 说明 |
| ---- | ---- |
| `version` | Compose 文件格式版本 |
| `services` | 定义一个或多个服务（容器） |
| `build` | 指定构建上下文与 Dockerfile |
| `image` | 引用已有镜像（与 `build` 二选一） |
| `ports` | 宿主机端口与容器端口映射 |
| `environment` / `env_file` | 注入环境变量 |
| `volumes` | 数据卷或目录挂载 |
| `depends_on` | 指定服务依赖关系 |
| `healthcheck` | 继承自 Docker，检查服务健康状态 |
| `networks` | 自定义网络，控制服务之间的通信 |

部署流程：

1. 编写并校验 Dockerfile、docker-compose.yml。  
2. 准备 `.env` 或 `env_file` 注入敏感配置。  
3. `docker compose up --build` 构建并启动服务。  
4. 使用 `docker compose logs -f`、`docker compose ps` 监控运行状态。  
5. 如需更新代码，重新构建并启动：`docker compose build --no-cache && docker compose up -d`。  

---

通过本手册，前后端服务的容器化部署流程即可快速落地，建议在教学中配合现场演示，让学员亲手完成一次完整部署。祝实战顺利！ 🚀
