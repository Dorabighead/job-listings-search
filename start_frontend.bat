@echo off
echo ========================================
echo 启动就业信息系统 - 前端服务
echo ========================================
echo.

cd /d %~dp0frontend

echo [1/2] 检查依赖...
if not exist "node_modules\" (
    echo node_modules 不存在，正在安装依赖...
    echo 使用淘宝镜像加速安装...
    call npm install --registry=https://registry.npmmirror.com
    echo 依赖安装完成！
)

echo [2/2] 启动前端服务...
echo.
echo 前端服务地址: http://localhost:3000
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

call npm run dev

pause
