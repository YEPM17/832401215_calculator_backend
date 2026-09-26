# 832401215 Calculator Backend

FastAPI + SQLAlchemy 后端，负责表达式解析、计算、历史持久化和删除。本地开发使用 SQLite，公网部署使用 PostgreSQL。

## 技术栈

- Python 3.12+
- FastAPI
- SQLAlchemy 2
- SQLite / PostgreSQL
- pytest

## 环境要求

- Python 3.12+
- Windows PowerShell 或 Linux/macOS Shell

## 安装与启动

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

访问 `http://127.0.0.1:8000/docs` 查看自动接口文档。

## 数据库初始化

应用首次启动会自动创建 `calculation.db` 和 `calculation_history` 表，无需手工执行 SQL。

## 环境变量

复制 `.env.example` 为 `.env`，按需修改：

- `DATABASE_URL`：数据库连接地址
- `CORS_ORIGINS`：允许访问 API 的前端地址，多个地址用逗号分隔
- `PORT`：服务端口

## 接口

- `POST /api/calculate`
- `GET /api/history`
- `DELETE /api/history/{id}`
- `DELETE /api/history`
- `GET /health`

请求示例：

```powershell
Invoke-RestMethod `
  -Method Post `
  -Uri 'http://127.0.0.1:8000/api/calculate' `
  -ContentType 'application/json' `
  -Body '{"expression":"(1+2)*3"}'
```

## 测试

```powershell
python -m pytest -v
```

## Docker

```powershell
docker build -t calculator-backend .
docker run --rm -p 8000:8000 -v calculator-data:/data calculator-backend
```

## 部署

当前公网部署使用 Railway：Docker Web Service 运行 FastAPI，Railway PostgreSQL 保存计算历史。部署后通过 `CORS_ORIGINS` 允许前端域名访问。

- 后端地址：https://832401215-calculator-backend-production.up.railway.app/
- 健康检查：https://832401215-calculator-backend-production.up.railway.app/health

仓库同时保留 `render.yaml` 作为 Render 平台的备选部署配置。
