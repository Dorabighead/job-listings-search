# 就业信息爬取和查询系统

一个完整的就业信息爬取、存储和查询系统，支持从多个招聘网站自动爬取职位信息，并提供友好的 Web 界面进行搜索、筛选、收藏和导出。

## 技术栈

### 后端
- **Python 3.8+**
- **FastAPI** - 现代化的 Web 框架
- **SQLAlchemy** - ORM 数据库操作
- **SQLite** - 轻量级数据库
- **BeautifulSoup4** - HTML 解析
- **Selenium** - 动态网页爬取
- **Pandas** - 数据导出

### 前端
- **React 18** - UI 框架
- **Ant Design 5** - UI 组件库
- **Vite** - 构建工具
- **Axios** - HTTP 客户端
- **React Router** - 路由管理

## 功能特性

### 核心功能
- ✅ 自动爬取招聘网站职位信息
- ✅ 支持关键词和地点筛选
- ✅ 职位列表展示和分页
- ✅ 职位详情查看
- ✅ 收藏感兴趣的职位
- ✅ 添加收藏备注
- ✅ 导出职位数据为 Excel
- ✅ 爬虫状态实时监控

### 支持的招聘网站
- ✅ **Boss直聘** (已实现)
- ⏳ 智联招聘 (待实现)
- ⏳ 前程无忧 (待实现)
- ⏳ 拉勾网 (待实现)

## 项目结构

```
qiuzhi/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── main.py            # FastAPI 应用入口
│   │   ├── database.py        # 数据库配置
│   │   ├── models.py          # 数据模型
│   │   ├── schemas.py         # Pydantic schemas
│   │   ├── crud.py            # CRUD 操作
│   │   ├── api/               # API 路由
│   │   │   ├── jobs.py
│   │   │   ├── favorites.py
│   │   │   └── scraper.py
│   │   └── scrapers/          # 爬虫模块
│   │       ├── base.py
│   │       └── boss_scraper.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/                  # 前端应用
│   ├── src/
│   │   ├── components/        # React 组件
│   │   ├── services/          # API 服务
│   │   ├── App.jsx
│   │   └── index.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 快速开始

### 环境要求
- Python 3.8 或更高版本
- Node.js 16 或更高版本
- npm 或 yarn

### 后端设置

1. **进入后端目录**
```bash
cd backend
```

2. **创建虚拟环境**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **配置环境变量** (可选，使用默认配置即可)

编辑 `.env` 文件：
```env
DATABASE_URL=sqlite:///./jobs.db
API_HOST=0.0.0.0
API_PORT=8000
```

5. **启动后端服务**
```bash
python -m app.main
```

后端服务将在 `http://localhost:8000` 运行

API 文档可访问: `http://localhost:8000/docs`

### 前端设置

1. **进入前端目录**
```bash
cd frontend
```

2. **安装依赖**
```bash
npm install
```

3. **启动开发服务器**
```bash
npm run dev
```

前端应用将在 `http://localhost:3000` 运行

## 使用指南

### 1. 启动爬虫任务

访问 **爬虫管理** 页面：
1. 选择数据来源 (目前支持 Boss直聘)
2. 输入搜索关键词 (如：Python、前端开发)
3. 选择工作地点 (可选)
4. 设置爬取页数 (建议1-3页)
5. 点击 "启动爬虫" 按钮

爬虫将自动爬取职位信息并保存到数据库，页面会显示爬取进度。

### 2. 浏览职位列表

在 **职位列表** 页面：
- 使用搜索框搜索职位或公司
- 通过下拉框筛选地点和数据来源
- 点击职位卡片查看详情
- 点击爱心图标收藏职位
- 点击 "导出Excel" 按钮下载当前筛选结果

### 3. 查看职位详情

点击任意职位卡片进入详情页：
- 查看完整的职位信息
- 收藏该职位
- 点击 "查看原始链接" 访问原网站

### 4. 管理收藏

在 **我的收藏** 页面：
- 查看所有收藏的职位
- 为职位添加备注
- 取消收藏
- 快速跳转到职位详情

### 5. 导出数据

在职位列表页面：
1. 设置搜索和筛选条件
2. 点击 "导出Excel" 按钮
3. 系统将下载包含当前筛选结果的 Excel 文件

## API 接口

### 职位相关
- `GET /api/jobs` - 获取职位列表
- `GET /api/jobs/{id}` - 获取职位详情
- `DELETE /api/jobs/{id}` - 删除职位
- `GET /api/jobs/export/excel` - 导出 Excel

### 收藏相关
- `GET /api/favorites` - 获取收藏列表
- `POST /api/favorites` - 添加收藏
- `PUT /api/favorites/{id}` - 更新收藏备注
- `DELETE /api/favorites/{id}` - 取消收藏

### 爬虫相关
- `POST /api/scraper/run` - 启动爬虫任务
- `GET /api/scraper/status` - 获取爬虫状态

完整 API 文档请访问: `http://localhost:8000/docs`

## 数据库表结构

### jobs 表
存储职位信息：
- id, job_id, title, company
- salary_min, salary_max
- location, experience, education
- job_type, description, requirements
- welfare, source, url
- created_at, updated_at

### favorites 表
存储收藏信息：
- id, job_id (外键)
- note (备注)
- created_at

## 注意事项

### 爬虫使用建议

1. **合理控制频率**: 建议每次爬取间隔 5 分钟以上
2. **遵守 robots.txt**: 尊重网站的爬虫协议
3. **避免大量爬取**: 每次爬取 1-3 页即可
4. **反爬虫限制**:
   - 已实现随机 User-Agent
   - 已实现请求延迟 (2-5秒)
   - 遇到验证码时需要手动处理

### 网站结构变化

招聘网站可能会更新页面结构，导致爬虫失效。如遇此问题：
1. 检查目标网站的 HTML 结构
2. 更新 `scrapers/` 目录下对应爬虫的解析逻辑
3. 重点关注 CSS 选择器部分

### 法律声明

本项目仅用于学习和研究目的。使用爬虫功能时：
- 请遵守目标网站的服务条款
- 不要用于商业用途
- 合理控制爬取频率
- 尊重网站版权和隐私

## 开发计划

- [ ] 实现智联招聘爬虫
- [ ] 实现前程无忧爬虫
- [ ] 实现拉勾网爬虫
- [ ] 添加薪资趋势分析
- [ ] 添加职位去重功能
- [ ] 支持邮件提醒
- [ ] 添加用户认证系统

## 故障排除

### 后端启动失败

**问题**: `ModuleNotFoundError`
**解决**: 确保已激活虚拟环境并安装所有依赖

```bash
pip install -r requirements.txt
```

### 前端无法连接后端

**问题**: API 请求失败
**解决**: 检查后端是否在 8000 端口运行，查看 `frontend/.env` 配置

### 爬虫无法获取数据

**问题**: 爬虫返回空数据
**解决**:
1. 检查网络连接
2. 确认目标网站未更新结构
3. 查看后端日志获取详细错误信息

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎通过 Issue 反馈。
