# ⚡ 5分钟快速启动指南

## 🎯 目标
在5分钟内启动并运行重构后的金融分析系统

---

## 📋 前置检查（1分钟）

### 必需环境
```powershell
# 检查 Node.js（需要 >= 18.0.0）
node --version

# 检查 Python（需要 >= 3.9）
python --version

# 检查 MySQL（需要 >= 8.0）
mysql --version

# 安装 pnpm（如果没有）
npm install -g pnpm
```

✅ 如果以上命令都能正常输出版本号，继续下一步

---

## 🚀 启动步骤

### 方式一：一键启动（推荐） ⭐

```powershell
# 1. 进入项目目录
cd d:\比赛\金融分析项目\financial_analysis\financial-analysis-refactored

# 2. 运行启动脚本
.\scripts\start.ps1

# 完成！脚本会自动：
# ✅ 安装所有依赖
# ✅ 配置环境变量
# ✅ 启动前后端服务
# ✅ 打开浏览器
```

**时间**: 3-5分钟（首次运行，需下载依赖）

---

### 方式二：手动启动

如果脚本执行失败，使用手动方式：

#### 步骤1：启动后端（2分钟）

```powershell
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 安装依赖
pip install -r requirements.txt

# 复制环境配置
Copy-Item .env.example .env

# 启动后端
python main.py
```

✅ 后端启动成功：http://localhost:8000

#### 步骤2：启动前端（2分钟）

**打开新的 PowerShell 窗口**

```powershell
# 进入前端目录
cd frontend

# 安装依赖
pnpm install

# 复制环境配置
Copy-Item .env.example .env

# 启动前端
pnpm dev
```

✅ 前端启动成功：http://localhost:5173

---

## 🌐 访问应用

### 1. 前端界面
```
http://localhost:5173
```
应该看到：
- 🎨 精美的渐变首页
- 🧭 导航按钮（公司查询、市场概况、用户中心）
- ✨ 功能特性展示

### 2. 后端API
```
http://localhost:8000
```
应该看到：
```json
{
  "message": "金融分析系统API - 重构版",
  "version": "2.0.0",
  "docs": "/docs"
}
```

### 3. API文档
```
http://localhost:8000/docs
```
应该看到：
- 📚 Swagger UI 界面
- 📡 所有API接口列表
- 🧪 可直接测试的接口

---

## ✅ 验证清单

### 前端检查
- [ ] 首页正常显示
- [ ] 可以点击导航按钮
- [ ] 浏览器控制台无错误

### 后端检查
- [ ] 访问 http://localhost:8000 返回欢迎信息
- [ ] 访问 http://localhost:8000/docs 显示API文档
- [ ] 访问 http://localhost:8000/health 返回 `{"status": "ok"}`

### 前后端连接
- [ ] 前端能正常调用后端API
- [ ] 浏览器Network标签显示API请求成功

---

## 🔧 常见问题快速修复

### Q1: 端口被占用

**前端端口冲突（5173）：**
```powershell
# 结束占用进程
Get-Process -Id (Get-NetTCPConnection -LocalPort 5173).OwningProcess | Stop-Process

# 或修改配置
# 编辑 frontend/vite.config.ts 中的 server.port
```

**后端端口冲突（8000）：**
```powershell
# 结束占用进程
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process

# 或修改配置
# 编辑 backend/.env 中的 PORT=8001
```

### Q2: pnpm 未找到

```powershell
npm install -g pnpm
```

### Q3: Python 依赖安装慢

```powershell
# 使用清华镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q4: 虚拟环境激活失败

```powershell
# 如果提示权限错误，以管理员身份运行：
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# 然后重新激活
.\venv\Scripts\Activate.ps1
```

---

## 🎉 成功启动！

如果所有验证都通过，恭喜您！系统已成功启动。

### 接下来可以：

1. 📖 **浏览功能**
   - 访问公司查询页面
   - 体验搜索功能
   - 查看组件展示

2. 🔍 **查看代码**
   - 研究组件结构（`frontend/src/components/`）
   - 学习Composables（`frontend/src/composables/`）
   - 理解API设计（`backend/apps/`）

3. 📚 **阅读文档**
   - [完整安装指南](./docs/SETUP.md)
   - [开发规范](./docs/DEVELOPMENT.md)
   - [架构设计](./docs/ARCHITECTURE.md)

4. 💻 **开始开发**
   - 创建新组件
   - 添加新功能
   - 编写测试

---

## 📞 获取帮助

如果遇到问题：

1. 查看详细文档：[docs/SETUP.md](./docs/SETUP.md)
2. 查看总结文档：[REFACTORED_PROJECT_SUMMARY.md](./REFACTORED_PROJECT_SUMMARY.md)
3. 提交Issue：https://github.com/LiQiCheng457/financial-analysis/issues

---

**祝您使用愉快！** 🚀✨

---

**提示**: 首次启动需要下载依赖，可能需要3-5分钟。后续启动只需30秒！
