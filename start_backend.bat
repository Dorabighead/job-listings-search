@echo off
echo ========================================
echo 启动就业信息系统 - 后端服务
echo ========================================
echo.

cd /d %~dp0backend

echo [1/3] 检查虚拟环境...
if not exist "venv\" (
    echo 虚拟环境不存在，正在创建...
    python -m venv venv
    echo 虚拟环境创建完成！
)

echo [2/3] 激活虚拟环境...
call venv\Scripts\activate

echo [3/3] 启动后端服务...
echo.
echo 后端服务地址: http://localhost:8000
echo API 文档地址: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

python -m app.main

pause
