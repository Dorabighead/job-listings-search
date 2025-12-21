# 快速启动指南

> 按照以下步骤，一步步启动就业信息爬取系统

---

## 📋 前置准备

### 1. 安装 Python（如果还没安装）

**详细安装步骤请查看：[PYTHON_SETUP_GUIDE.md](./PYTHON_SETUP_GUIDE.md)**

快速步骤：
1. 下载 Python 3.11：https://www.python.org/downloads/
2. 安装到 `D:\Tool\python`
3. **必须勾选** "Add Python to PATH"
4. 验证安装：打开 CMD 运行 `python --version`

### 2. 确认 Node.js 已安装

打开 CMD 运行：
```bash
node --version
```

应该显示 `v20.x.x` 或更高版本（你已经安装了 ✓）

---

## 🚀 启动步骤

### 第一步：安装后端依赖

打开 **命令提示符（CMD）** 或 **PowerShell**：

```bash
# 1. 进入后端目录
cd D:\project\qiuzhi\backend

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# CMD 使用：
venv\Scripts\activate

# PowerShell 使用：
# venv\Scripts\Activate.ps1

# 4. 升级 pip（推荐）
python -m pip install --upgrade pip

# 5. 安装依赖（使用清华镜像加速）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

等待安装完成（约 2-3 分钟）

---

### 第二步：启动后端服务

在**同一个**命令窗口（确保虚拟环境已激活，提示符前有 `(venv)`）：

```bash
# 启动后端服务
python -m app.main
```

看到以下信息表示成功：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

**不要关闭这个窗口！** 保持后端运行。

**测试后端：** 打开浏览器访问
- API 根路径：http://localhost:8000
- API 文档：http://localhost:8000/docs

---

### 第三步：安装前端依赖

打开**新的** CMD 或 PowerShell 窗口：

```bash
# 1. 进入前端目录
cd D:\project\qiuzhi\frontend

# 2. 安装依赖（使用淘宝镜像加速）
npm install --registry=https://registry.npmmirror.com
```

等待安装完成（约 3-5 分钟）

---

### 第四步：启动前端服务

在同一个前端窗口：

```bash
# 启动前端开发服务器
npm run dev
```

看到以下信息表示成功：
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

---

### 第五步：访问系统

打开浏览器访问：**http://localhost:3000**

你会看到就业信息查询系统的界面！

---

## 📱 使用系统

### 1. 爬取职位数据

1. 点击顶部菜单 **"爬虫管理"**
2. 填写表单：
   - 数据来源：选择 "Boss直聘"
   - 搜索关键词：输入 "Python" 或 "前端开发"
   - 工作地点：选择 "北京" 或其他城市（可选）
   - 爬取页数：输入 `1` 或 `2`（建议先少量测试）
3. 点击 **"启动爬虫"** 按钮
4. 等待爬取完成（页面会显示进度）

### 2. 浏览职位

1. 点击顶部菜单 **"职位列表"**
2. 查看爬取到的职位
3. 使用搜索框和筛选条件查找职位
4. 点击职位卡片查看详情

### 3. 收藏职位

1. 在职位列表或详情页，点击 ❤️ 图标收藏职位
2. 点击顶部菜单 **"我的收藏"** 查看收藏
3. 可以为收藏添加备注

### 4. 导出数据

在职位列表页面，点击 **"导出Excel"** 按钮下载数据

---

## 🔧 常用操作

### 停止服务

**停止后端：**
- 在后端窗口按 `Ctrl + C`
- 输入 `deactivate` 退出虚拟环境

**停止前端：**
- 在前端窗口按 `Ctrl + C`

### 下次启动

**后端：**
```bash
cd D:\project\qiuzhi\backend
venv\Scripts\activate
python -m app.main
```

**前端：**
```bash
cd D:\project\qiuzhi\frontend
npm run dev
```

### 查看日志

**后端日志：** 直接在运行后端的 CMD 窗口查看

**前端日志：**
- 开发服务器日志：前端 CMD 窗口
- 浏览器日志：按 F12 打开开发者工具

---

## ❓ 常见问题

### Q1: 后端启动失败，提示 "ModuleNotFoundError"

**原因：** 没有激活虚拟环境或依赖未安装

**解决：**
```bash
cd D:\project\qiuzhi\backend
venv\Scripts\activate
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: 前端启动失败，提示端口被占用

**错误信息：** `Port 3000 is already in use`

**解决：**
1. 修改端口：编辑 `frontend/vite.config.js`，将 `port: 3000` 改为 `port: 3001`
2. 或者关闭占用 3000 端口的程序

### Q3: 爬虫没有数据

**可能原因：**
1. 网络连接问题
2. 目标网站结构变化
3. 需要登录或验证码

**解决：**
- 检查后端日志查看错误信息
- 尝试访问 Boss直聘网站确认可访问
- 减少爬取页数测试

### Q4: 前端无法连接后端

**错误：** API 请求失败

**检查：**
1. 后端是否正在运行（http://localhost:8000 可访问）
2. 查看浏览器控制台（F12）的网络请求错误
3. 确认 `frontend/.env` 中的 API 地址正确

### Q5: pip install 很慢

**解决：** 使用国内镜像源
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

或永久配置：
```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 📚 更多文档

- **Python 安装和虚拟环境详解**：[PYTHON_SETUP_GUIDE.md](./PYTHON_SETUP_GUIDE.md)
- **项目完整说明**：[README.md](./README.md)
- **API 接口文档**：启动后端后访问 http://localhost:8000/docs

---

## 🎯 完整启动命令总结

**方式一：两个窗口**

窗口 1 - 后端：
```bash
cd D:\project\qiuzhi\backend
venv\Scripts\activate
python -m app.main
```

窗口 2 - 前端：
```bash
cd D:\project\qiuzhi\frontend
npm run dev
```

**方式二：使用启动脚本（下面会创建）**

运行 `start.bat` 即可一键启动

---

## ✨ 下一步

- 尝试爬取不同关键词的职位
- 收藏感兴趣的职位并添加备注
- 导出数据分析
- 查看 API 文档了解更多功能

**祝你使用愉快！**
