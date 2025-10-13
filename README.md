# 金融分析项目 (FastAPI + Vue3)

这是一个前后端分离的金融数据分析示例项目。后端使用 FastAPI (Python)，前端使用 Vue 3 + Vite。数据源使用 akshare 获取上海证券交易所每日概况与个股历史行情；前端使用 ECharts 做可视化。

目录结构（简要）

- `financial-analysis-api/` - 后端服务 (FastAPI)
  - `main.py` - 程序入口
  - `requirements.txt` - Python 依赖
  - `app/` - 后端应用代码
    - `apis/` - 路由定义（包括 `stock.py`）
    - `services/` - 服务层（包括 `stock_service.py`，包含 akshare 调用）
    - `core/`, `models/`, `schemas/` 等
  - `.env` - 项目运行时环境变量（不会被提交）

- `financial-analysis-admin/` - 前端 (Vue 3 + Vite)
  - `package.json`, `pnpm-lock.yaml`
  - `src/` - 源代码
    - `api/stock.ts` - 前端请求封装
    - `components/StockChart.vue` - 可视化组件（基于 ECharts）
    - `views/` - 页面（包含 `HomeView.vue`、`StockHistory.vue`）

- `scripts/` - 辅助脚本与 mock 数据（例如 `fetch_stock_history.py`）

------

先决条件

- 操作系统：Windows / macOS / Linux（示例以 Windows PowerShell 为主）
- Python 3.10（项目在 README 中建议 3.10）
- Node.js + pnpm（或 npm/yarn），用于启动前端
- Conda（可选，但本仓库使用 conda 环境名 `financial-analysis` 的示例）

推荐环境（示例）

- Conda 环境名：`financial-analysis`（已在开发机使用）
- 前端包管理：pnpm（你也可以用 npm/yarn）

------

后端（financial-analysis-api）启动步骤

1. 切换到后端目录：

```powershell
cd 'D:\比赛\金融分析项目\financial_analysis\financial-analysis-api'
```

2. 激活已有 conda 环境（示例环境名 `financial-analysis`）或创建一个：

```powershell
# 激活已有环境
conda activate financial-analysis

# 或者创建并激活新环境（只需运行一次）
conda create -n financial-analysis python=3.10 -y
conda activate financial-analysis
```

3. 安装 Python 依赖：

```powershell
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

4. 配置环境变量（可选）：

- 项目有一个示例 `.env`（或 `financial-analysis-api/.env`），用于存放数据库连接、密钥等敏感配置，请按需创建或修改该文件。示例条目：

```
# 示例 .env
DATABASE_URL=mysql+pymysql://user:password@127.0.0.1:3306/your_db_name
SECRET_KEY=your_secret
DEBUG=True
```

5. MySQL 连接与位置说明：

- 项目中读取/配置 MySQL 的位置：
  - 主配置通常在 `financial-analysis-api/app/core/database.py` 或 `financial-analysis-api/application/settings.py`（如果不存在，项目会在 `app/core/database.py` 或 `app/config` 中查找 DATABASE_URL）。
  - 具体的数据库 URL 常通过环境变量 `DATABASE_URL` 或项目配置文件注入。请检查 `app/core/database.py` 或 `application/settings.py` 中 `sqlalchemy` 的配置语句以确定实际使用的变量名与优先级。

（示例：在 `app/core/database.py` 中会有类似 `create_engine(DATABASE_URL, ...)` 的代码，或在 application/settings 中解析环境变量。）

6. 启动后端服务：

```powershell
# 项目使用 main.py 提供命令入口
python main.py run

# 或者使用 uvicorn（如果你更习惯）：
# python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

7. 验证：打开浏览器访问后端文档（如果项目配置了 docs）：

```
http://127.0.0.1:9000/docs
```

（端口/路径根据 `main.py` 的配置可能不同；`main.py run` 在本项目中会读取 settings 配置并启动相应端口，默认示例文档中提到 9000。）

------

前端（financial-analysis-admin）启动步骤

1. 进入前端目录：

```powershell
cd 'D:\比赛\金融分析项目\financial_analysis\financial-analysis-admin'
```

2. 安装依赖（首次）

```powershell
pnpm install
# 或者使用 npm
# npm install
```

3. 启动开发服务器（默认代理 `/api` 到后端）

```powershell
pnpm run dev
```

4. 打开浏览器访问开发地址（Vite 控制台会显示，例如 http://localhost:5173）。

注意：前端 `src/utils/request.ts` 使用 baseURL `/api`，开发时 Vite 配置会把 `/api` 代理到后端地址（参见 `vite.config.ts`）。确保后端在代理目标上运行（例如 127.0.0.1:8000 或 main.py 指定端口）。

------

当前项目完成状态（截至当前工作区文件）

- 后端
  - 基本框架与路由已实现（`app/apis/stock.py` 包含 `/trade_dates`, `/sse_daily_summary`, `/history` 路由）。
  - 服务层实现了 `app/services/stock_service.py`：对 akshare 的调用、数据清洗、JSON-safe 转换与历史行情获取逻辑已实现（含多源支持）。
  - 若要进行端到端测试，需要在本地安装 `uvicorn`（或通过 `python main.py run`）并确保 `akshare`、`pandas` 等依赖存在，且能联网或使用脚本中的 mock 数据。

- 前端
  - Vue 3 页面与组件已实现：包含 `StockHistory.vue`（表格）、`StockChart.vue`（ECharts 可视化）与 API 封装 `src/api/stock.ts`。
  - ECharts 已被加入依赖，组件支持对后端返回不同字段名的兼容性（中英列名自动识别）。
  - 前端 dev server 需后端可用以取得真实数据；否则组件可使用脚本目录下的 mock 数据进行本地开发。

- 开发/调试说明
  - 若后端因 akshare 或网络问题无法获取真实数据，可使用 `financial-analysis-api/scripts/mock_stock_history_000001.json` 或 `scripts/fetch_stock_history.py` 来本地验证前端显示。
  - 若出现 `No module named uvicorn`，请在激活的 Python 环境中安装 `uvicorn[standard] fastapi` 或使用 `python main.py run`（项目封装的启动命令通常不依赖全局 uvicorn）。

