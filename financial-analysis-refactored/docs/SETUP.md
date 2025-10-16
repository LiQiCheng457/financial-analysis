# 📦 安装指南

## 环境要求

在开始之前，请确保您的系统已安装以下软件：

### 必需软件

| 软件 | 最低版本 | 推荐版本 | 下载地址 |
|------|---------|---------|---------|
| **Node.js** | 18.0.0 | 20.11.0 | https://nodejs.org/ |
| **Python** | 3.9 | 3.11 | https://www.python.org/ |
| **MySQL** | 8.0 | 8.0.35 | https://dev.mysql.com/downloads/ |
| **pnpm** | 8.0.0 | 8.15.0 | `npm install -g pnpm` |

### 可选软件

- **Git**: 版本控制
- **VS Code**: 推荐的代码编辑器
- **Postman**: API测试工具

## 快速安装

### 方式一：一键启动（推荐）

#### Windows

```powershell
# 1. 克隆项目
git clone https://github.com/LiQiCheng457/financial-analysis.git
cd financial-analysis/financial-analysis-refactored

# 2. 运行启动脚本
.\scripts\start.ps1
```

脚本会自动完成：
- ✅ 环境检查
- ✅ 依赖安装
- ✅ 环境配置
- ✅ 服务启动

#### Linux/Mac

```bash
# 1. 克隆项目
git clone https://github.com/LiQiCheng457/financial-analysis.git
cd financial-analysis/financial-analysis-refactored

# 2. 运行启动脚本
chmod +x scripts/start.sh
./scripts/start.sh
```

### 方式二：手动安装

如果您需要更多控制，可以手动安装：

#### 1. 数据库配置

```sql
-- 创建数据库
CREATE DATABASE financial_analysis CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户（可选）
CREATE USER 'fin_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON financial_analysis.* TO 'fin_user'@'localhost';
FLUSH PRIVILEGES;
```

#### 2. 后端安装

```bash
cd backend

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# Windows CMD
.\venv\Scripts\activate.bat
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入数据库配置

# 运行数据库迁移（如果有）
# alembic upgrade head

# 启动后端
python main.py
```

后端将在 `http://localhost:8000` 启动

#### 3. 前端安装

```bash
cd frontend

# 安装依赖（推荐使用 pnpm）
pnpm install
# 或使用 npm
# npm install

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件（通常默认配置即可）

# 启动前端
pnpm dev
# 或
# npm run dev
```

前端将在 `http://localhost:5173` 启动

## 验证安装

### 1. 检查后端

访问 http://localhost:8000
- 应该看到欢迎信息

访问 http://localhost:8000/docs
- 应该看到 Swagger API 文档

访问 http://localhost:8000/health
- 应该返回 `{"status": "ok"}`

### 2. 检查前端

访问 http://localhost:5173
- 应该看到金融分析系统首页
- 可以正常导航到各个页面

### 3. 检查前后端连接

在浏览器控制台中，检查是否有API请求错误。

## 常见问题

### Q1: pnpm 未找到

```bash
# 全局安装 pnpm
npm install -g pnpm
```

### Q2: Python 依赖安装失败

```bash
# 升级 pip
python -m pip install --upgrade pip

# 使用清华镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 数据库连接失败

检查 `backend/.env` 文件中的数据库配置：
- 数据库是否已创建
- 用户名和密码是否正确
- MySQL 服务是否运行

### Q4: 端口已被占用

**前端端口（5173）冲突：**
```bash
# 修改 frontend/vite.config.ts 中的 server.port
```

**后端端口（8000）冲突：**
```bash
# 修改 backend/.env 中的 PORT
```

### Q5: AKShare 数据获取失败

AKShare 依赖网络连接，请确保：
- 网络连接正常
- 没有被防火墙拦截
- 可以尝试使用代理

## 开发工具配置

### VS Code 推荐扩展

#### 前端
- Vue Language Features (Volar)
- TypeScript Vue Plugin (Volar)
- ESLint
- Prettier

#### 后端
- Python
- Pylance
- Python Debugger

### VS Code 配置

在项目根目录创建 `.vscode/settings.json`:

```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black"
}
```

## 下一步

安装完成后，您可以：

1. 📖 阅读 [开发指南](./DEVELOPMENT.md) 了解开发规范
2. 📡 查看 [API文档](./API.md) 了解接口使用
3. 🏛️ 学习 [架构文档](./ARCHITECTURE.md) 理解系统设计

## 获取帮助

如果遇到问题：

1. 查看本文档的"常见问题"部分
2. 查看 [GitHub Issues](https://github.com/LiQiCheng457/financial-analysis/issues)
3. 创建新的 Issue 描述您的问题

---

**祝您使用愉快！** 🎉
