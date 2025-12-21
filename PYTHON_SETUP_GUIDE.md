# Python 安装和虚拟环境使用指南

## 一、Python 安装步骤

### 1. 下载 Python

访问 Python 官网下载页面：
- 官网地址：https://www.python.org/downloads/
- 推荐版本：**Python 3.11.x** 或 **Python 3.10.x**
- 选择 **Windows installer (64-bit)** 下载

> 直接下载链接（Python 3.11.7）：
> https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe

### 2. 安装 Python 到指定目录

1. **运行下载的安装程序** (python-3.11.7-amd64.exe)

2. **重要**：在第一个安装界面：
   - ✅ **勾选** "Add Python to PATH"（将 Python 添加到环境变量）
   - ✅ **勾选** "Install launcher for all users"
   - 点击 **"Customize installation"**（自定义安装）

3. **Optional Features 界面**（可选功能）：
   - ✅ Documentation（文档）
   - ✅ pip（包管理器）- **必选**
   - ✅ tcl/tk and IDLE
   - ✅ Python test suite
   - ✅ py launcher
   - 点击 **"Next"**

4. **Advanced Options 界面**（高级选项）：
   - ✅ Install for all users（为所有用户安装）
   - ✅ Associate files with Python
   - ✅ Create shortcuts for installed applications
   - ✅ Add Python to environment variables（添加到环境变量）- **重要**
   - ✅ Precompile standard library

   - **自定义安装路径**：
     - 点击 "Browse" 按钮
     - 选择路径：`D:\Tool\python`
     - 或手动输入：`D:\Tool\python`

   - 点击 **"Install"**

5. **等待安装完成**
   - 看到 "Setup was successful" 表示安装成功
   - 点击 "Close" 关闭安装程序

### 3. 验证安装

打开**新的**命令提示符（CMD）或 PowerShell 窗口：

```bash
python --version
```

应该显示类似：
```
Python 3.11.7
```

检查 pip：
```bash
pip --version
```

应该显示类似：
```
pip 23.3.1 from D:\Tool\python\Lib\site-packages\pip (python 3.11)
```

> **注意**：如果命令不识别，请重启计算机后再试。

---

## 二、Python 虚拟环境详解

### 什么是虚拟环境？

虚拟环境是 Python 的独立工作空间，它可以：
- 为每个项目创建独立的依赖包环境
- 避免不同项目之间的包版本冲突
- 保持系统 Python 环境的干净

### 虚拟环境的工作原理

```
系统 Python (D:\Tool\python)
│
├── 项目A虚拟环境 (qiuzhi\backend\venv)
│   └── 独立的包: FastAPI, SQLAlchemy...
│
├── 项目B虚拟环境 (project_b\venv)
│   └── 独立的包: Django, Pandas...
│
└── 全局包（不推荐直接安装项目依赖）
```

---

## 三、虚拟环境基本操作

### 1. 创建虚拟环境

进入项目目录：
```bash
cd D:\project\qiuzhi\backend
```

创建虚拟环境（名为 venv）：
```bash
python -m venv venv
```

> 说明：
> - `python -m venv` 是创建虚拟环境的命令
> - 最后的 `venv` 是虚拟环境文件夹的名称（可以自定义）
> - 执行后会在当前目录创建 `venv` 文件夹

### 2. 激活虚拟环境

**Windows CMD：**
```bash
venv\Scripts\activate
```

**Windows PowerShell：**
```bash
venv\Scripts\Activate.ps1
```

> 如果 PowerShell 报错"无法加载脚本"，执行以下命令（以管理员身份运行 PowerShell）：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**激活成功的标志**：
命令提示符前面会出现 `(venv)`：
```
(venv) D:\project\qiuzhi\backend>
```

### 3. 在虚拟环境中安装包

激活虚拟环境后，使用 pip 安装包：

```bash
# 安装单个包
pip install fastapi

# 从 requirements.txt 安装所有依赖
pip install -r requirements.txt

# 升级 pip（推荐）
python -m pip install --upgrade pip
```

### 4. 查看已安装的包

```bash
pip list
```

或查看项目依赖：
```bash
pip freeze
```

### 5. 退出虚拟环境

```bash
deactivate
```

退出后，命令提示符前的 `(venv)` 会消失。

### 6. 删除虚拟环境

如果需要重新创建虚拟环境：

1. 先退出虚拟环境（如果已激活）
```bash
deactivate
```

2. 删除 venv 文件夹
```bash
rmdir /s venv
```

3. 重新创建
```bash
python -m venv venv
```

---

## 四、本项目虚拟环境完整流程

### 步骤 1：创建虚拟环境

```bash
# 进入后端目录
cd D:\project\qiuzhi\backend

# 创建虚拟环境
python -m venv venv
```

### 步骤 2：激活虚拟环境

**CMD：**
```bash
venv\Scripts\activate
```

**PowerShell：**
```bash
venv\Scripts\Activate.ps1
```

### 步骤 3：升级 pip（推荐）

```bash
python -m pip install --upgrade pip
```

### 步骤 4：安装项目依赖

```bash
pip install -r requirements.txt
```

安装过程可能需要几分钟，请耐心等待。

### 步骤 5：验证安装

```bash
pip list
```

应该看到已安装的包，包括：
- fastapi
- uvicorn
- sqlalchemy
- pydantic
- 等等...

### 步骤 6：运行后端服务

```bash
python -m app.main
```

成功启动会显示：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

访问 http://localhost:8000 查看 API
访问 http://localhost:8000/docs 查看 API 文档

### 步骤 7：停止服务

按 `Ctrl + C` 停止服务

### 步骤 8：退出虚拟环境

```bash
deactivate
```

---

## 五、常见问题解决

### Q1: 提示 "python 不是内部或外部命令"

**原因**：Python 未添加到环境变量

**解决方案**：
1. 手动添加环境变量：
   - 右键 "此电脑" → 属性 → 高级系统设置 → 环境变量
   - 在 "系统变量" 中找到 "Path"，点击编辑
   - 添加以下两个路径：
     ```
     D:\Tool\python
     D:\Tool\python\Scripts
     ```
   - 确定保存后重启命令提示符

2. 或者重新安装 Python，记得勾选 "Add Python to PATH"

### Q2: pip install 速度很慢

**原因**：访问国外服务器较慢

**解决方案**：使用国内镜像源

临时使用清华镜像：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

永久配置镜像（推荐）：
```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: PowerShell 无法激活虚拟环境

**错误信息**：
```
无法加载文件，因为在此系统上禁止运行脚本
```

**解决方案**：
以管理员身份运行 PowerShell，执行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q4: 虚拟环境激活后仍然使用全局 Python

**验证方法**：
```bash
where python
# 或
python -c "import sys; print(sys.prefix)"
```

应该显示虚拟环境路径：
```
D:\project\qiuzhi\backend\venv
```

**如果不对**：重新创建虚拟环境

### Q5: requirements.txt 安装失败

**常见原因**：
- 网络问题 → 使用国内镜像源
- pip 版本过低 → 升级 pip
- 缺少编译工具（某些包需要）

**解决步骤**：
```bash
# 1. 升级 pip
python -m pip install --upgrade pip

# 2. 使用镜像源安装
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 3. 如果某个包失败，单独安装
pip install <包名> -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 六、虚拟环境最佳实践

### ✅ 推荐做法

1. **每个项目使用独立虚拟环境**
   ```bash
   项目A/venv
   项目B/venv
   ```

2. **将虚拟环境添加到 .gitignore**
   ```
   venv/
   *.pyc
   __pycache__/
   ```

3. **使用 requirements.txt 管理依赖**
   ```bash
   # 导出当前环境依赖
   pip freeze > requirements.txt

   # 安装依赖
   pip install -r requirements.txt
   ```

4. **激活虚拟环境后再安装包**
   - ✅ 先激活 venv，再 pip install
   - ❌ 不要在全局环境安装项目依赖

### ❌ 避免的做法

1. ❌ 不使用虚拟环境，直接在全局安装
2. ❌ 多个项目共用一个虚拟环境
3. ❌ 将 venv 文件夹提交到 Git
4. ❌ 忘记激活虚拟环境就安装包

---

## 七、快速命令速查表

| 操作 | Windows CMD 命令 |
|------|-----------------|
| 创建虚拟环境 | `python -m venv venv` |
| 激活虚拟环境 | `venv\Scripts\activate` |
| 退出虚拟环境 | `deactivate` |
| 安装依赖 | `pip install -r requirements.txt` |
| 查看已安装包 | `pip list` |
| 升级 pip | `python -m pip install --upgrade pip` |
| 导出依赖 | `pip freeze > requirements.txt` |
| 删除虚拟环境 | `rmdir /s venv` |

---

## 八、下一步操作

完成 Python 安装和虚拟环境创建后：

1. ✅ 创建并激活虚拟环境
2. ✅ 安装后端依赖
3. ✅ 运行后端服务
4. 🔜 安装前端依赖（npm install）
5. 🔜 运行前端服务（npm run dev）

**祝你使用愉快！有问题随时问我。**
