# 📈 智能证券分析系统# 🎯 智能证券分析系统



[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.0-009688.svg)](https://fastapi.tiangolo.com/)

[![Vue](https://img.shields.io/badge/Vue-3.x-green.svg)](https://vuejs.org/)![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)

[![Element Plus](https://img.shields.io/badge/Element%20Plus-2.x-409eff.svg)](https://element-plus.org/)![Python](https://img.shields.io/badge/python-3.9+-green.svg)

[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)![Vue](https://img.shields.io/badge/vue-3.3+-brightgreen.svg)

![License](https://img.shields.io/badge/license-MIT-orange.svg)

一个基于 **Vue 3** + **FastAPI** 的现代化金融数据分析平台，提供实时行情、技术分析、公司信息查询等功能。

**基于 Vue 3 + FastAPI 的智能证券分析系统**

## 🌟 项目特色

[快速开始](#-快速开始) • [功能特性](#-功能特性) • [技术栈](#-技术栈) • [文档](#-完整文档)

- 🚀 **实时行情**：集成 AKShare 金融数据接口，提供实时股票行情

- 📊 **数据可视化**：ECharts 图表展示，支持K线图、折线图等多种图表</div>

- 🏢 **公司信息**：完整的上市公司基本资料查询，支持行业筛选

- 📅 **历史数据**：历史行情数据查询与分析，支持日期范围筛选---

- 🎨 **现代化UI**：基于 Element Plus 的美观界面设计

- 🔐 **用户系统**：完整的用户注册、登录、权限管理## 📖 项目简介



## 📸 系统预览这是一个功能完善的金融数据分析平台，提供实时行情查询、技术分析、公司信息查询等功能。



### 主页 - 实时行情展示### ✨ 核心功能

- 折线图展示股票价格走势（开盘、收盘、最高、最低）

- 支持自定义股票代码查询| 模块 | 功能说明 |

- 实时数据更新|------|----------|

| 🔐 **用户认证** | JWT Token认证、密码加密存储、权限控制 |

### 市场概况| 📊 **实时行情** | 股票价格走势、分时图、数据可视化 |

- 上交所每日交易概况| 📈 **K线图表** | 专业K线图、成交量、MA均线、技术指标 |

- 成交金额、市值、挂牌数等关键指标| 🏢 **公司信息** | 行业搜索、上市公司资料、分页展示 |

| 📅 **市场概况** | 上交所每日交易统计、市场趋势 |

### 公司概况查询| 👤 **个人中心** | 资料管理、头像上传、安全设置 |

- 13个行业分类标签筛选

- 支持公司名称、股票代码模糊搜索### 🎯 特色亮点

- 详细的公司基本资料展示（32个字段）

- 紫色渐变标签设计，色彩编码信息分类- ✅ **数据实时** - 基于AKShare的实时股票数据源

- ✅ **交互流畅** - 现代化的用户界面和交互体验

### K线图分析- ✅ **响应式设计** - 完美适配PC/平板/手机

- 专业的K线图技术分析- ✅ **安全可靠** - 完善的认证和权限控制机制

- 支持前复权、后复权

- 多种技术指标---



## 🏗️ 技术架构## 🚀 快速开始



### 前端技术栈### 📋 环境要求

- **框架**: Vue 3.x (Composition API)

- **UI库**: Element Plus 2.x| 软件 | 版本 | 说明 |

- **构建工具**: Vite 4.x|------|------|------|

- **图表**: ECharts 5.x| Python | 3.9+ | 后端运行环境 |

- **语言**: TypeScript| Node.js | 16+ | 前端构建工具 |

- **包管理**: pnpm| MySQL | 8.0+ | 数据库 |

| **Conda** | - | **Python环境管理（非必需，但推荐）** |

### 后端技术栈

- **框架**: FastAPI 0.110.0### ⚡ 三步启动

- **ORM**: SQLAlchemy 2.0

- **数据库**: MySQL 8.0```powershell

- **数据源**: AKShare (金融数据接口)# 1️⃣ 启动后端

- **认证**: JWTcd financial-analysis-api

- **服务器**: Uvicornconda activate financial-analysis

python main.py

### 数据源

- **AKShare**: 主要数据来源，提供实时行情、历史数据等# 2️⃣ 启动前端（新开终端）

- **本地数据库**: 存储公司基本信息、用户数据等cd financial-analysis-admin

pnpm install  # 首次运行需要

## 📦 项目结构pnpm run dev



```# 3️⃣ 访问应用

financial-analysis/# 浏览器打开: http://localhost:5173

├── financial-analysis-admin/          # 前端项目```

│   ├── src/

│   │   ├── api/                      # API 接口封装

│   │   ├── components/               # 公共组件## 📦 技术栈

│   │   ├── views/                    # 页面视图

│   │   │   ├── home/                 # 主页<table>

│   │   │   ├── market/               # 市场相关<tr>

│   │   │   │   ├── Summary.vue       # 市场概况<td width="50%" valign="top">

│   │   │   │   ├── Snapshot.vue      # 公司概况

│   │   │   │   └── KLine.vue         # K线图### 后端技术

│   │   │   ├── stock/                # 股票相关

│   │   │   └── user/                 # 用户相关| 技术 | 版本 | 用途 |

│   │   ├── router/                   # 路由配置|------|------|------|

│   │   ├── store/                    # 状态管理| FastAPI | 0.104+ | Web框架 |

│   │   └── utils/                    # 工具函数| SQLAlchemy | 2.0+ | ORM |

│   ├── package.json| Pydantic | 2.5+ | 数据验证 |

│   └── vite.config.ts| JWT | - | 身份认证 |

│| **AKShare** | 1.13+ | **股票数据源** |

├── financial-analysis-api/           # 后端项目| MySQL | 8.0+ | 数据库 |

│   ├── app/

│   │   ├── apis/                     # API 路由</td>

│   │   │   └── stock.py              # 股票相关API<td width="50%" valign="top">

│   │   ├── services/                 # 业务逻辑

│   │   │   └── stock_service.py      # 股票数据服务### 前端技术

│   │   ├── models/                   # 数据模型

│   │   └── core/                     # 核心模块| 技术 | 版本 | 用途 |

│   ├── main.py                       # 应用入口|------|------|------|

│   ├── requirements.txt              # Python 依赖| Vue 3 | 3.3+ | 前端框架 |

│   └── .env                          # 环境变量配置| TypeScript | 5.0+ | 类型系统 |

│| Vite | 4.5+ | 构建工具 |

├── 启动服务.ps1                       # 快速启动脚本| Element Plus | 2.4+ | UI组件库 |

├── 服务启动指南.md                    # 详细启动文档| ECharts | 5.4+ | 数据可视化 |

├── 问题修复报告.md                    # 技术问题记录| Pinia | 2.1+ | 状态管理 |

├── 基本资料优化文档.md                # UI优化记录

└── README.md                         # 本文档</td>

```</tr>

</table>

## 🚀 快速开始

---

### 环境要求

## 📁 项目结构

#### 开发环境

- **Node.js**: 16.x 或更高版本```

- **Python**: 3.8 或更高版本financial_analysis/

- **MySQL**: 8.0 或更高版本├── 📚 README.md                     # 👈 你在这里

- **pnpm**: 最新版本（推荐）或 npm├── 📄 PROJECT_SUMMARY.md            # 完整技术文档

- **Conda**: Anaconda 或 Miniconda（推荐）├── 📋 HANDOVER_GUIDE.md             # 项目交接指南

│

#### 系统要求├── 📂 financial-analysis-api/       # 后端服务

- **操作系统**: Windows 10/11, macOS, Linux│   ├── main.py                      # 应用入口

- **内存**: 建议 8GB 及以上│   ├── requirements.txt             # Python依赖

- **硬盘**: 至少 2GB 可用空间│   ├── .env                         # 环境变量

│   └── app/

### 📥 从 GitHub 克隆项目│       ├── apis/                    # API路由

│       │   ├── auth.py              # 认证API

```bash│       │   ├── stock.py             # 股票API

# 克隆仓库│       │   └── user.py              # 用户API

git clone https://github.com/LiQiCheng457/financial-analysis.git│       ├── models/                  # 数据模型

│       │   └── user.py              # User模型

# 进入项目目录│       ├── services/                # 业务逻辑

cd financial-analysis│       │   ├── auth_service.py      # 认证服务

```│       │   └── stock_service.py     # 股票服务

│       └── schemas/                 # 数据验证

### 🔧 后端配置与启动│           └── user_schema.py       # User Schema

│

#### 1. 创建 Python 虚拟环境（重要！）└── 📂 financial-analysis-admin/     # 前端应用

    ├── vite.config.ts               # Vite配置

```bash    ├── package.json                 # 前端依赖

# 创建名为 financial-analysis 的虚拟环境    └── src/

conda create -n financial-analysis python=3.8 -y        ├── api/                     # API封装

        │   ├── auth.ts              # 认证API

# 激活虚拟环境        │   ├── stock.ts             # 股票API

conda activate financial-analysis        │   └── user.ts              # 用户API

```        ├── views/                   # 页面组件

        │   ├── Home.vue             # 首页

#### 2. 安装 Python 依赖        │   ├── market/              # 市场分析

        │   │   ├── KLine.vue        # K线图

```bash        │   │   ├── Snapshot.vue     # 公司概况

cd financial-analysis-api        │   │   └── DailySummary.vue # 每日概况

        │   └── user/

# 安装依赖（必须在虚拟环境中）        │       └── Profile.vue      # 个人中心

pip install -r requirements.txt        ├── router/                  # 路由配置

        └── store/                   # 状态管理

# 安装 AKShare（关键依赖）```

pip install akshare pandas

```---



#### 3. 配置数据库## 🎨 功能展示



**创建数据库：**### 1. 首页 - 实时行情

```sql- 渐变色Hero区域

CREATE DATABASE financial_analysis_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;- 快速入口导航

```- 股票走势图表



**修改 `.env` 文件：**### 2. 市场分析 - K线图

```env- 专业K线图（蜡烛图）

DATABASE_USER=root- 成交量柱状图

DATABASE_PASSWORD=your_password- MA均线指标

DATABASE_HOST=localhost- 数据源切换

DATABASE_PORT=3306

DATABASE_NAME=financial_analysis_db### 3. 公司概况

SECRET_KEY=your-super-secret-key-for-jwt- 按行业搜索

ALGORITHM=HS256- 公司列表分页（50条/页）

ACCESS_TOKEN_EXPIRE_MINUTES=30- 公司详情查看

```

### 4. 个人中心

#### 4. 初始化数据库（可选）- 头像上传（Base64）

- 资料编辑（昵称/手机/邮箱/签名）

如果需要导入公司基本信息数据：- 密码修改（旧密码验证）

```bash- 安全设置

# 运行初始化脚本

python scripts/initialize/initialize.py---

```

## 📚 完整文档

#### 5. 启动后端服务

| 文档 | 内容 | 适用场景 |

**⚠️ 重要：必须在虚拟环境中启动！**|------|------|----------|

| **[项目总结](PROJECT_SUMMARY.md)** | 完整技术文档、API说明、数据库设计 | 技术归档、深入学习 |

```bash| **[交接指南](HANDOVER_GUIDE.md)** | 详细交接文档、常见问题、调试技巧 | 项目交接、新人上手 |

# 确保已激活虚拟环境| **[API文档](http://127.0.0.1:8000/docs)** | Swagger自动生成的API文档 | 接口调试、联调 |

conda activate financial-analysis

---

# 启动服务

python main.py## ⚙️ 配置说明

```

### 后端配置

**验证启动成功：**

- 访问: http://localhost:8000**环境变量** (`financial-analysis-api/.env`):

- API 文档: http://localhost:8000/docs```ini

- 看到输出: `INFO: Uvicorn running on http://0.0.0.0:8000`# 数据库配置

DATABASE_USER=root

### 💻 前端配置与启动DATABASE_PASSWORD=your_password

DATABASE_HOST=localhost

#### 1. 安装 Node.js 依赖DATABASE_PORT=3306

DATABASE_NAME=financial_analysis_db

```bash

cd financial-analysis-admin# JWT配置

SECRET_KEY=your-secret-key-change-in-production

# 使用 pnpm 安装（推荐）ALGORITHM=HS256

pnpm installACCESS_TOKEN_EXPIRE_MINUTES=30

```

# 或使用 npm

npm install### 前端配置

```

**代理设置** (`vite.config.ts`):

#### 2. 启动开发服务器```typescript

server: {

```bash  proxy: {

pnpm run dev    '/api': {

# 或      target: 'http://127.0.0.1:8000',  // 后端地址

npm run dev      changeOrigin: true

```    }

  }

**验证启动成功：**}

- 访问: http://localhost:5173```

- 看到输出: `Local: http://localhost:5173/`

---

### 🎯 一键启动（Windows PowerShell）

## 🐛 常见问题

我们提供了快速启动脚本：

### ❌ Q1: 数据不显示或返回空数组？

```powershell

# 在项目根目录执行**✅ 解决方案**: 确保后端使用了包含AKShare的conda环境：

.\启动服务.ps1

``````powershell

# 1. 激活conda环境（必需！）

脚本会自动：conda activate financial-analysis

1. 停止旧的服务进程

2. 在虚拟环境中启动后端# 2. 验证AKShare已安装

3. 测试后端 API 连接python -c "import akshare as ak; print(ak.__version__)"

4. 启动前端开发服务器

# 3. 启动后端

## 📚 开发进度python main.py

```

### ✅ 已完成功能

> ⚠️ **关键提示**: AKShare必须安装在conda环境中，否则所有数据API会返回空！

#### 核心功能

- [x] 用户注册、登录、JWT 认证### ❌ Q2: 前端API请求404错误？

- [x] 实时行情数据获取与展示

- [x] 历史行情数据查询（支持日期范围）**✅ 检查清单**:

- [x] K线图技术分析（前复权、后复权）1. ✓ 后端是否启动？访问 http://127.0.0.1:8000/docs

- [x] 上交所每日概况数据展示2. ✓ Vite代理配置是否指向正确端口（8000）？

- [x] 交易日历查询3. ✓ API路径是否包含重复的`/api`？（应使用相对路径）



#### 公司信息模块### ❌ Q3: 登录后页面空白？

- [x] 公司基本资料查询（32个字段）

- [x] 行业分类标签筛选（13个分组）**✅ 解决方案**:

- [x] 公司搜索（支持代码、名称模糊匹配）1. 打开浏览器控制台（F12）查看错误

- [x] OR 逻辑行业筛选（支持多个行业）2. 检查Token是否正确存储：

- [x] 分页功能（前端 + 后端）   ```javascript

- [x] 详情页面优化（紫色渐变标签）   localStorage.getItem('token')

   ```

#### UI/UX 优化3. 确认后端返回的Token格式正确

- [x] 响应式布局设计

- [x] 现代化 UI 界面### ❌ Q4: 数据库连接失败？

- [x] 色彩编码系统（信息分类可视化）

- [x] 交互动画效果**✅ 解决方案**:

- [x] 信息密集型布局优化（空间节省28%）1. 确认MySQL服务已启动

2. 检查`.env`配置是否正确

#### 数据可视化3. 验证数据库是否存在：

- [x] ECharts 折线图（实时行情）   ```sql

- [x] K线图（技术分析）   SHOW DATABASES LIKE 'financial_analysis_db';

- [x] 数据表格展示   ```

- [x] 图表交互功能

更多问题请查看 **[交接指南 - 常见问题](HANDOVER_GUIDE.md#-常见问题及解决方案)**

### 🚧 开发中功能

---

- [ ] 自选股管理

- [ ] 技术指标计算（MACD, KDJ, RSI等）## 🔧 开发指南

- [ ] 财务数据分析

- [ ] 新闻资讯聚合### 后端开发

- [ ] 智能预警系统

```powershell

### 📅 计划功能# 安装依赖

pip install -r requirements.txt

- [ ] 量化策略回测

- [ ] AI 智能推荐# 运行开发服务器

- [ ] 移动端适配python main.py

- [ ] 数据导出功能（Excel, PDF）

- [ ] 多语言支持# 数据库迁移

- [ ] 暗色主题python migrations/migrate_user_fields.py



## 🔐 默认账号# 查看API文档

# http://127.0.0.1:8000/docs

系统提供测试账号（如已初始化数据）：```



```### 前端开发

用户名: admin

密码: admin123```powershell

```# 安装依赖

pnpm install

**⚠️ 生产环境请务必修改默认密码！**

# 运行开发服务器

## 📖 API 文档pnpm run dev



后端启动后，访问以下地址查看完整 API 文档：# 构建生产版本

pnpm run build

- **Swagger UI**: http://localhost:8000/docs

- **ReDoc**: http://localhost:8000/redoc# 预览生产构建

pnpm run preview

### 主要 API 端点```



#### 股票数据---

```

GET  /api/stocks/trade_dates          # 获取交易日历## 📊 数据库设计

GET  /api/stocks/history               # 获取历史行情

GET  /api/stocks/realtime              # 获取实时行情### users 表

GET  /api/stocks/sse_daily_summary     # 上交所每日概况```sql

GET  /api/stocks/company_profile       # 公司基本资料CREATE TABLE users (

GET  /api/stocks/search_companies      # 搜索公司列表  id INT PRIMARY KEY AUTO_INCREMENT,

```  username VARCHAR(50) UNIQUE NOT NULL,

  hashed_password VARCHAR(255) NOT NULL,

#### 用户认证  avatar TEXT,

```  nickname VARCHAR(100),

POST /api/auth/register                # 用户注册  phone VARCHAR(20),

POST /api/auth/login                   # 用户登录  email VARCHAR(100),

GET  /api/auth/me                      # 获取当前用户信息  signature VARCHAR(200),

```  created_at DATETIME DEFAULT CURRENT_TIMESTAMP

);

## 🛠️ 常见问题```



### Q1: 后端启动报错 "akshare 未安装"### stock_basic_info 表

```sql

**原因**: 后端没有在虚拟环境中运行CREATE TABLE stock_basic_info (

  id INT PRIMARY KEY AUTO_INCREMENT,

**解决方案**:  stock_code VARCHAR(20) UNIQUE NOT NULL,

```bash  company_name VARCHAR(200),

# 停止所有 Python 进程  eastmoney_industry VARCHAR(100),

Get-Process python | Stop-Process -Force  regulatory_industry VARCHAR(100),

  -- 更多字段请参考 PROJECT_SUMMARY.md

# 在虚拟环境中重新启动);

conda activate financial-analysis```

cd financial-analysis-api

python main.py详细设计请参考 **[项目总结 - 数据库设计](PROJECT_SUMMARY.md#5-数据库设计)**

```

---

### Q2: 前端连接后端失败

## 🔐 安全性

**检查项**:

1. 后端是否正常启动（访问 http://localhost:8000）| 措施 | 说明 | 状态 |

2. 前端 API 配置是否正确（检查 `src/utils/request.ts`）|------|------|------|

3. 防火墙是否阻止连接| JWT Token | 身份认证 | ✅ 已实现 |

| Bcrypt | 密码加密 | ✅ 已实现 |

### Q3: 数据库连接失败| ORM | SQL注入防护 | ✅ 已实现 |

| CORS | 跨域控制 | ✅ 已配置 |

**检查项**:| SECRET_KEY | 生产环境更换 | ⚠️ 待更新 |

1. MySQL 服务是否启动

2. `.env` 文件中的数据库配置是否正确---

3. 数据库用户权限是否足够

## 📝 更新日志

### Q4: 图表不显示数据

### v1.0.0 (2024-10-16)

**原因**: 后端 API 返回数据异常

**✨ 新增功能**:

**解决方案**:- ✅ 用户注册登录系统

1. 检查浏览器控制台错误- ✅ 个人中心完整功能（5个标签页）

2. 验证后端 API 返回数据格式- ✅ 股票数据查询和可视化

3. 确保 akshare 正常工作- ✅ K线图技术分析

- ✅ 公司信息查询（行业搜索、分页）

### Q5: 端口被占用- ✅ 市场概况展示



**解决方案**:**🔧 技术改进**:

```bash- ✅ 前后端分离架构

# 查看端口占用- ✅ RESTful API设计

netstat -ano | findstr :8000- ✅ 响应式界面

netstat -ano | findstr :5173- ✅ 代码规范化

- ✅ 完整项目文档

# 停止占用进程

taskkill /PID <进程ID> /F---

```

## 🤝 贡献

## 📊 性能优化

欢迎提交Issue和Pull Request！

### 已实现的优化

- ✅ API 响应数据缓存### 贡献指南

- ✅ 前端组件懒加载

- ✅ 图表数据分页加载1. Fork本仓库

- ✅ SQL 查询优化（索引、DISTINCT）2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)

- ✅ 紧凑布局（空间节省28%）3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)

4. 推送到分支 (`git push origin feature/AmazingFeature`)

### 性能指标5. 开启Pull Request

- **首屏加载**: < 2s

- **API 响应**: < 500ms（本地数据）---

- **图表渲染**: < 100ms

- **搜索响应**: < 300ms## 📄 许可证



## 🤝 贡献指南本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件



欢迎贡献代码！请遵循以下步骤：---



1. Fork 本仓库## 🙏 致谢

2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)

3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)感谢以下开源项目：

4. 推送到分支 (`git push origin feature/AmazingFeature`)

5. 开启 Pull Request- [Vue.js](https://vuejs.org/) - 渐进式JavaScript框架

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化Python Web框架

### 代码规范- [Element Plus](https://element-plus.org/) - Vue 3组件库

- **前端**: ESLint + Prettier- [ECharts](https://echarts.apache.org/) - 数据可视化库

- **后端**: PEP 8 规范- [AKShare](https://akshare.akfamily.xyz/) - 金融数据接口库

- **提交信息**: 遵循 [Conventional Commits](https://www.conventionalcommits.org/)

---

## 📄 开源协议

## 📞 支持

本项目采用 [MIT License](LICENSE) 开源协议。

- **Issue**: [GitHub Issues](https://github.com/your-repo/financial-analysis/issues)

## 🙏 致谢- **文档**: [完整文档](PROJECT_SUMMARY.md) | [交接指南](HANDOVER_GUIDE.md)

- **API文档**: http://127.0.0.1:8000/docs (启动后端后访问)

### 技术栈

- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架---

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Python Web 框架

- [Element Plus](https://element-plus.org/) - Vue 3 组件库<div align="center">

- [ECharts](https://echarts.apache.org/) - 强大的图表库

- [AKShare](https://akshare.akfamily.xyz/) - 金融数据接口**⭐ 如果这个项目对你有帮助，请给我们一个Star！**



### 数据来源Made with ❤️ by Financial Analysis Team

- **AKShare**: 提供免费的金融数据接口

- **东方财富**: 部分行业分类数据</div>

- **上交所**: 每日交易概况数据


## 📞 联系方式

- **项目地址**: https://github.com/LiQiCheng457/financial-analysis
- **问题反馈**: [Issues](https://github.com/LiQiCheng457/financial-analysis/issues)
- **作者**: LiQiCheng457

## 🌟 Star History

如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！

---

**最后更新时间**: 2025-10-16  
**当前版本**: v1.0.0  
**开发状态**: 持续开发中 🚧

