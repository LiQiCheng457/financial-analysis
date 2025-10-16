# 🚀 金融分析系统 - 重构版本

> **完整重构的金融分析平台** - 基于 Vue 3 + FastAPI + AKShare  
> 代码质量优化、模块化设计、开箱即用

## 📋 项目概述

这是原金融分析系统的**完整重构版本**，采用现代化的架构设计和最佳实践，提供：

- 🎯 **清晰的项目结构** - 前后端分离，模块化组织
- 🧩 **组件化开发** - 原子设计系统，高度复用
- 📦 **类型安全** - TypeScript 100% 覆盖
- 🎨 **统一的代码风格** - ESLint + Prettier + Stylelint
- 📚 **完整的文档** - API文档、开发指南、部署说明
- ⚡ **开箱即用** - 一键启动脚本，快速上手

## 🏗️ 项目结构

```
financial-analysis-refactored/
├── frontend/                 # 前端项目（Vue 3 + TypeScript）
│   ├── src/
│   │   ├── views/           # 页面视图
│   │   ├── components/      # 组件库
│   │   │   ├── atomic/      # 原子组件
│   │   │   ├── molecular/   # 分子组件
│   │   │   └── business/    # 业务组件
│   │   ├── composables/     # 组合式API
│   │   ├── api/             # API接口层
│   │   ├── router/          # 路由配置
│   │   ├── stores/          # 状态管理（Pinia）
│   │   ├── utils/           # 工具函数
│   │   ├── types/           # TypeScript类型
│   │   ├── styles/          # 全局样式
│   │   └── assets/          # 静态资源
│   ├── public/              # 公共资源
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── .env.example
│
├── backend/                  # 后端项目（FastAPI + Python）
│   ├── apps/                # 应用模块
│   │   ├── company/         # 公司信息模块
│   │   ├── market/          # 市场数据模块
│   │   ├── user/            # 用户管理模块
│   │   └── analysis/        # 数据分析模块
│   ├── core/                # 核心功能
│   │   ├── config.py        # 配置管理
│   │   ├── database.py      # 数据库连接
│   │   ├── security.py      # 安全认证
│   │   └── exceptions.py    # 异常处理
│   ├── utils/               # 工具函数
│   ├── models/              # 数据模型
│   ├── schemas/             # Pydantic模式
│   ├── tests/               # 单元测试
│   ├── main.py              # 应用入口
│   ├── requirements.txt
│   └── .env.example
│
├── docs/                     # 项目文档
│   ├── SETUP.md             # 安装指南
│   ├── DEVELOPMENT.md       # 开发指南
│   ├── API.md               # API文档
│   ├── ARCHITECTURE.md      # 架构说明
│   └── CHANGELOG.md         # 更新日志
│
├── scripts/                  # 工具脚本
│   ├── start.ps1            # Windows启动脚本
│   ├── start.sh             # Linux/Mac启动脚本
│   ├── setup.ps1            # 环境配置脚本
│   └── deploy.sh            # 部署脚本
│
├── .gitignore
└── README.md                 # 本文件
```

## 🚀 快速开始

### 前置要求

- **Node.js** >= 18.0.0
- **Python** >= 3.9
- **MySQL** >= 8.0
- **pnpm** >= 8.0.0（推荐）

### 一键启动

#### Windows
```powershell
# 进入项目目录
cd financial-analysis-refactored

# 运行启动脚本（自动安装依赖并启动前后端）
.\scripts\start.ps1
```

#### Linux/Mac
```bash
# 进入项目目录
cd financial-analysis-refactored

# 运行启动脚本
chmod +x scripts/start.sh
./scripts/start.sh
```

### 手动启动

#### 1. 配置环境变量

```bash
# 复制环境配置模板
cp frontend/.env.example frontend/.env
cp backend/.env.example backend/.env

# 编辑配置文件，填入数据库等信息
```

#### 2. 启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 数据库迁移
alembic upgrade head

# 启动服务
python main.py
```

后端服务将运行在：http://localhost:8000

#### 3. 启动前端

```bash
cd frontend

# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

前端服务将运行在：http://localhost:5173

## 📦 核心功能

### ✅ 已实现功能

- **公司信息查询**
  - 多行业标签筛选（13个行业）
  - OR逻辑组合搜索
  - 公司详情展示（32个字段）

- **实时行情**
  - 股票实时价格
  - 涨跌幅统计
  - K线图表展示

- **市场概况**
  - 市场总览
  - 行业分析
  - 热门榜单

- **用户中心**
  - 用户认证
  - 个人信息管理
  - 收藏功能

### 🚧 正在开发

- **技术分析工具**
  - 技术指标计算
  - 图表分析
  - 策略回测

- **智能推荐**
  - 个性化推荐
  - 风险评估
  - 投资建议

## 🛠️ 技术栈

### 前端

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue 3 | ^3.4.0 | 渐进式框架 |
| TypeScript | ^5.3.0 | 类型系统 |
| Vite | ^5.0.0 | 构建工具 |
| Element Plus | ^2.5.0 | UI组件库 |
| Pinia | ^2.1.0 | 状态管理 |
| Vue Router | ^4.2.0 | 路由管理 |
| Axios | ^1.6.0 | HTTP客户端 |
| ECharts | ^5.4.0 | 图表库 |

### 后端

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | ^3.9 | 编程语言 |
| FastAPI | ^0.109.0 | Web框架 |
| SQLAlchemy | ^2.0.0 | ORM |
| MySQL | ^8.0 | 数据库 |
| AKShare | ^1.13.0 | 金融数据 |
| Pydantic | ^2.5.0 | 数据验证 |
| Uvicorn | ^0.27.0 | ASGI服务器 |

## 📚 文档导航

- [📖 安装指南](./docs/SETUP.md) - 详细的环境配置和安装步骤
- [👨‍💻 开发指南](./docs/DEVELOPMENT.md) - 开发规范和最佳实践
- [📡 API文档](./docs/API.md) - 完整的API接口说明
- [🏛️ 架构文档](./docs/ARCHITECTURE.md) - 系统架构和设计思路
- [📝 更新日志](./docs/CHANGELOG.md) - 版本更新记录

## 🎯 开发规范

### 代码风格

- **前端**: ESLint + Prettier (Airbnb风格)
- **后端**: Black + Flake8 (PEP 8)
- **提交**: Conventional Commits

### 命名规范

#### 前端
- 组件文件: PascalCase (`BaseCard.vue`)
- 函数/变量: camelCase (`getUserInfo`)
- 常量: UPPER_SNAKE_CASE (`API_BASE_URL`)
- CSS类: kebab-case (`user-profile`)

#### 后端
- 文件/函数: snake_case (`get_user_info.py`)
- 类: PascalCase (`UserModel`)
- 常量: UPPER_SNAKE_CASE (`API_VERSION`)

### Git工作流

```bash
# 创建功能分支
git checkout -b feature/new-feature

# 提交代码
git commit -m "feat: 添加新功能"

# 推送分支
git push origin feature/new-feature

# 创建 Pull Request
```

## 🧪 测试

### 前端测试

```bash
cd frontend

# 运行单元测试
pnpm test

# 运行E2E测试
pnpm test:e2e

# 测试覆盖率
pnpm test:coverage
```

### 后端测试

```bash
cd backend

# 运行单元测试
pytest

# 测试覆盖率
pytest --cov=apps --cov-report=html
```

## 📦 构建部署

### 前端构建

```bash
cd frontend

# 生产构建
pnpm build

# 预览构建结果
pnpm preview
```

### 后端部署

```bash
cd backend

# 使用 Gunicorn + Uvicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# 或使用 Docker
docker build -t financial-analysis-backend .
docker run -p 8000:8000 financial-analysis-backend
```

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👥 团队

- **项目负责人**: LiQiCheng457
- **技术架构**: [架构文档](./docs/ARCHITECTURE.md)
- **问题反馈**: [GitHub Issues](https://github.com/LiQiCheng457/financial-analysis/issues)

## 📞 联系方式

- **GitHub**: https://github.com/LiQiCheng457/financial-analysis
- **Email**: your-email@example.com

## 🙏 致谢

- [Vue.js](https://vuejs.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [AKShare](https://akshare.akfamily.xyz/)
- [Element Plus](https://element-plus.org/)

---

**最后更新**: 2025-10-16  
**版本**: v2.0.0-refactored  
**状态**: 🚧 重构进行中
