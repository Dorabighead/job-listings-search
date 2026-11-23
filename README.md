# 招聘信息采集与查询系统

![React 18](https://img.shields.io/badge/React%2018-147A9D?style=flat-square&logo=react&logoColor=white)
![Ant Design](https://img.shields.io/badge/Ant%20Design-2563EB?style=flat-square&logo=antdesign&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-00897B?style=flat-square&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)

## 📌 项目简介

面向求职者的职位整理工具。将招聘信息保存到本地后，可以按关键词和地点筛选，查看职位详情和原始链接，为感兴趣的职位添加收藏备注，并将筛选结果导出为 Excel。

目前已实现 BOSS 直聘的数据来源适配。页面提供职位浏览、收藏管理和采集任务状态查询。

## 🏗️ 系统架构

- **Web 前端**使用 React、Ant Design 和 Vite，负责职位搜索、详情、收藏和任务状态展示。开发时由 Vite 将 `/api` 请求代理到 FastAPI。
- **API 后端**使用 FastAPI，提供职位、收藏和任务状态接口。Pandas 和 openpyxl 用于生成 Excel 文件。
- **数据层**通过 SQLAlchemy 读写 SQLite。服务首次启动时创建 `jobs` 和 `favorites` 两张表，分别保存职位和收藏备注。
- **数据采集**代码位于后端的 `scrapers/`，通过独立的数据来源适配器为职位列表提供数据。

## 📁 项目结构

| 路径 | 用途 |
| --- | --- |
| [backend/app/api](backend/app/api) | 职位、收藏和采集任务 API |
| [backend/app/models.py](backend/app/models.py) | 职位和收藏的 ORM 模型 |
| [backend/app/scrapers](backend/app/scrapers) | 数据来源适配器 |
| [frontend/src/components](frontend/src/components) | 职位列表、详情、收藏和任务界面 |
| [frontend/src/services](frontend/src/services) | 前端 API 请求 |
| [QUICK_START.md](QUICK_START.md) | Windows 快速启动指南 |

## 🚀 如何启动

建议使用 Python 3.11 和 Node.js 22。克隆仓库后，分别打开两个终端。

```sh
git clone https://github.com/wxk2378643343-cloud/job-listings-search.git
cd job-listings-search
```

### 1. 启动后端

在 `backend/` 创建虚拟环境并安装依赖。下面以 Windows PowerShell 为例。

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

在 macOS 或 Linux 上，可将上述两处 Python 路径改为 `.venv/bin/python`。默认数据库为 `backend/jobs.db`。如需更换数据库路径，可在 `backend/.env` 中设置 `DATABASE_URL`。

### 2. 启动前端

在另一个终端从仓库根目录运行。

```sh
cd frontend
npm ci
npm run dev
```

打开 [职位浏览页面](http://localhost:3000)。后端运行时，也可查看 [Swagger API 文档](http://127.0.0.1:8000/docs)。首次启动时数据库为空，可以通过 Swagger 的 `POST /api/jobs/` 使用自备的演示职位检查列表、收藏和导出流程。

| 功能 | API |
| --- | --- |
| 分页浏览职位 | `GET /api/jobs/` |
| 查看职位详情 | `GET /api/jobs/{job_id}` |
| 导出职位列表 | `GET /api/jobs/export/excel` |
| 查看或添加收藏 | `GET /api/favorites/`、`POST /api/favorites/` |
| 修改或删除收藏 | `PUT /api/favorites/{favorite_id}`、`DELETE /api/favorites/{favorite_id}` |
| 查看采集状态 | `GET /api/scraper/status` |

Windows 下也可以按 [快速启动指南](QUICK_START.md) 使用仓库自带的批处理脚本。前端请求失败时，先确认 API 文档可以打开，再检查 [Vite 代理配置](frontend/vite.config.js)中的后端端口。

## 使用说明

通过职位列表进行搜索、筛选、分页和导出。进入职位详情可以查看来源链接。在收藏页添加备注或取消收藏。使用外部招聘信息时请确保有权访问和使用相关数据。

## 贡献与反馈

欢迎提交 Issue 或 Pull Request，说明复现步骤和预期结果。

## 许可证

本项目基于 [MIT License](LICENSE) 开源，详见根目录 [LICENSE](LICENSE) 文件。
