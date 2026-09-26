# 832401215 Calculator Backend

FastAPI + SQLAlchemy + SQLite 后端，负责表达式解析、计算、历史持久化和删除。

## 技术栈

- Python 3.12+
- FastAPI
- SQLAlchemy 2
- SQLite
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

Render 可直接识别 `render.yaml`。部署后把服务公网地址填入前端 `js/config.js`，并把前端公网地址加入 `CORS_ORIGINS`。
