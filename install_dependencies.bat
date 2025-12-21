@echo off
echo ========================================
echo 安装就业信息系统依赖
echo ========================================
echo.

echo [第一步] 安装后端依赖
echo ========================================
cd /d %~dp0backend

if not exist "venv\" (
    echo 创建虚拟环境...
    python -m venv venv
)

echo 激活虚拟环境...
call venv\Scripts\activate

echo 升级 pip...
python -m pip install --upgrade pip

echo 安装 Python 依赖包（使用清华镜像）...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo 后端依赖安装完成！
echo.

call deactivate

echo.
echo [第二步] 安装前端依赖
echo ========================================
cd /d %~dp0frontend

echo 安装 Node 依赖包（使用淘宝镜像）...
call npm install --registry=https://registry.npmmirror.com

echo.
echo ========================================
echo 所有依赖安装完成！
echo ========================================
echo.
echo 下一步：
echo   1. 双击运行 start_backend.bat 启动后端
echo   2. 双击运行 start_frontend.bat 启动前端
echo   3. 访问 http://localhost:3000
echo.

pause
