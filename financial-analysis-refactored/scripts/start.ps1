# 金融分析系统 - 一键启动脚本 (Windows PowerShell)
# 自动安装依赖并启动前后端服务

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  金融分析系统 - 重构版 v2.0.0" -ForegroundColor Cyan
Write-Host "  正在启动..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$projectRoot = $PSScriptRoot | Split-Path
$frontendPath = Join-Path $projectRoot "frontend"
$backendPath = Join-Path $projectRoot "backend"

# 检查 Node.js
Write-Host "[1/6] 检查 Node.js 环境..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ 未检测到 Node.js，请先安装 Node.js >= 18.0.0" -ForegroundColor Red
    exit 1
}

# 检查 Python
Write-Host "[2/6] 检查 Python 环境..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ 未检测到 Python，请先安装 Python >= 3.9" -ForegroundColor Red
    exit 1
}

# 安装前端依赖
Write-Host "[3/6] 安装前端依赖..." -ForegroundColor Yellow
Set-Location $frontendPath
if (-not (Test-Path "node_modules")) {
    Write-Host "正在安装前端依赖，这可能需要几分钟..." -ForegroundColor Gray
    pnpm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ 前端依赖安装完成" -ForegroundColor Green
    } else {
        Write-Host "✗ 前端依赖安装失败，尝试使用 npm..." -ForegroundColor Yellow
        npm install
    }
} else {
    Write-Host "✓ 前端依赖已存在" -ForegroundColor Green
}

# 安装后端依赖
Write-Host "[4/6] 安装后端依赖..." -ForegroundColor Yellow
Set-Location $backendPath
if (-not (Test-Path "venv")) {
    Write-Host "正在创建虚拟环境..." -ForegroundColor Gray
    python -m venv venv
}
& ".\venv\Scripts\Activate.ps1"
Write-Host "正在安装后端依赖..." -ForegroundColor Gray
pip install -r requirements.txt -q
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 后端依赖安装完成" -ForegroundColor Green
} else {
    Write-Host "✗ 后端依赖安装失败" -ForegroundColor Red
}

# 配置环境变量
Write-Host "[5/6] 配置环境变量..." -ForegroundColor Yellow
if (-not (Test-Path (Join-Path $frontendPath ".env"))) {
    Copy-Item (Join-Path $frontendPath ".env.example") (Join-Path $frontendPath ".env")
    Write-Host "✓ 前端环境配置已创建" -ForegroundColor Green
}
if (-not (Test-Path (Join-Path $backendPath ".env"))) {
    Copy-Item (Join-Path $backendPath ".env.example") (Join-Path $backendPath ".env")
    Write-Host "✓ 后端环境配置已创建" -ForegroundColor Green
    Write-Host "⚠ 请修改 backend/.env 文件中的数据库配置" -ForegroundColor Yellow
}

# 启动服务
Write-Host "[6/6] 启动服务..." -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  服务启动中..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  前端: http://localhost:5173" -ForegroundColor Green
Write-Host "  后端: http://localhost:8000" -ForegroundColor Green
Write-Host "  API文档: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

# 启动后端
Set-Location $backendPath
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '.\venv\Scripts\Activate.ps1'; python main.py"

# 等待后端启动
Start-Sleep -Seconds 3

# 启动前端
Set-Location $frontendPath
Start-Process powershell -ArgumentList "-NoExit", "-Command", "pnpm dev"

Write-Host "✓ 服务已启动！浏览器将自动打开..." -ForegroundColor Green
Start-Sleep -Seconds 2

# 打开浏览器
Start-Process "http://localhost:5173"

Set-Location $projectRoot
