# 金融分析系统 - 大规模重构优化方案

**制定日期：** 2025-01-16  
**目标：** 提升代码质量、可维护性、可扩展性

---

## 📋 目录

1. [前端重构方案](#1-前端重构方案)
2. [后端重构方案](#2-后端重构方案)
3. [命名规范标准化](#3-命名规范标准化)
4. [项目结构优化](#4-项目结构优化)
5. [执行计划](#5-执行计划)

---

## 1. 前端重构方案

### 1.1 组件拆分策略

#### 当前问题
- ❌ 大型组件超过 1000 行（如 Snapshot.vue, Profile.vue）
- ❌ 业务逻辑与 UI 耦合严重
- ❌ 重复代码（搜索框、表格、表单等）
- ❌ 缺少原子组件库

#### 优化方案

##### A. 原子组件层 (Atomic Components)
**位置：** `src/components/atomic/`

```
components/
  atomic/
    ├── BaseButton.vue          # 基础按钮（继承 el-button）
    ├── BaseInput.vue           # 基础输入框
    ├── BaseCard.vue            # 基础卡片
    ├── BaseTag.vue             # 基础标签
    ├── BaseBadge.vue           # 基础徽章
    ├── BaseEmpty.vue           # 空状态
    ├── BaseLoading.vue         # 加载状态
    └── BaseDialog.vue          # 基础对话框
```

##### B. 业务组件层 (Business Components)
**位置：** `src/components/business/`

```
components/
  business/
    ├── stock/
    │   ├── StockSearchBar.vue      # 股票搜索栏
    │   ├── StockInfoCard.vue       # 股票信息卡片
    │   ├── StockTable.vue          # 股票列表表格
    │   ├── StockDetailPanel.vue    # 股票详情面板
    │   └── StockPriceChart.vue     # 股价图表
    │
    ├── company/
    │   ├── CompanySearchPanel.vue     # 公司搜索面板
    │   ├── CompanyIndustryTags.vue    # 行业标签组
    │   ├── CompanyInfoTable.vue       # 公司信息表格
    │   ├── CompanyDetailCard.vue      # 公司详情卡片
    │   └── CompanyProfileLayout.vue   # 公司概况布局
    │
    ├── chart/
    │   ├── KLineChart.vue          # K线图
    │   ├── LineChart.vue           # 折线图
    │   ├── CandlestickChart.vue    # 蜡烛图
    │   └── VolumeChart.vue         # 成交量图
    │
    ├── user/
    │   ├── UserProfileForm.vue     # 用户资料表单
    │   ├── UserPasswordForm.vue    # 密码修改表单
    │   ├── UserPreferences.vue     # 偏好设置
    │   └── UserStatistics.vue      # 用户统计
    │
    └── common/
        ├── SearchBar.vue           # 通用搜索栏
        ├── FilterPanel.vue         # 筛选面板
        ├── DataTable.vue           # 数据表格
        ├── Pagination.vue          # 分页器
        └── ActionBar.vue           # 操作栏
```

##### C. 布局组件层 (Layout Components)
**位置：** `src/components/layout/`

```
components/
  layout/
    ├── AppHeader.vue           # 应用头部
    ├── AppSidebar.vue          # 侧边栏
    ├── AppFooter.vue           # 页脚
    ├── PageContainer.vue       # 页面容器
    ├── ContentSection.vue      # 内容区块
    └── SplitPane.vue           # 分割面板
```

##### D. 功能组件层 (Feature Components)
**位置：** `src/components/features/`

```
components/
  features/
    ├── watchlist/
    │   ├── WatchlistPanel.vue      # 自选股面板
    │   ├── WatchlistGroup.vue      # 自选股分组
    │   └── WatchlistItem.vue       # 自选股项
    │
    ├── realtime/
    │   ├── RealtimeQuote.vue       # 实时行情
    │   ├── RealtimeTicker.vue      # 实时滚动
    │   └── RealtimeAlert.vue       # 实时提醒
    │
    └── news/
        ├── NewsCard.vue            # 新闻卡片
        ├── NewsList.vue            # 新闻列表
        └── NewsDetail.vue          # 新闻详情
```

---

### 1.2 Composables 抽取（组合式 API）

**位置：** `src/composables/`

```
composables/
  ├── useStock.ts              # 股票相关
  ├── useCompany.ts            # 公司相关
  ├── useChart.ts              # 图表相关
  ├── useSearch.ts             # 搜索相关
  ├── usePagination.ts         # 分页相关
  ├── useForm.ts               # 表单相关
  ├── useTable.ts              # 表格相关
  ├── useAuth.ts               # 认证相关
  ├── useUser.ts               # 用户相关
  ├── useWebSocket.ts          # WebSocket
  └── useDebounce.ts           # 防抖节流
```

#### 示例：`useSearch.ts`
```typescript
export function useSearch(options: SearchOptions) {
  const query = ref('')
  const results = ref([])
  const loading = ref(false)
  const error = ref<Error | null>(null)

  const search = useDebounceFn(async () => {
    // 搜索逻辑
  }, 300)

  return {
    query,
    results,
    loading,
    error,
    search
  }
}
```

---

### 1.3 视图层重构

#### 页面拆分原则
- 每个页面不超过 300 行
- 业务逻辑抽离到 composables
- UI 逻辑拆分到子组件
- 使用 `<script setup>` 语法

#### 新的视图结构
```
views/
  ├── home/
  │   ├── index.vue                    # 首页（入口）
  │   └── components/                  # 首页专用组件
  │       ├── HeroSection.vue
  │       ├── QuickAccessGrid.vue
  │       └── ChartSection.vue
  │
  ├── market/
  │   ├── summary/
  │   │   ├── index.vue                # 市场概况
  │   │   └── components/
  │   │       ├── SummaryCards.vue
  │   │       └── TradingCalendar.vue
  │   │
  │   ├── snapshot/
  │   │   ├── index.vue                # 公司快照（重构后）
  │   │   └── components/
  │   │       ├── SearchPanel.vue
  │   │       ├── ResultTable.vue
  │   │       └── DetailModal.vue
  │   │
  │   ├── kline/
  │   │   ├── index.vue                # K线图
  │   │   └── components/
  │   │       ├── ChartToolbar.vue
  │   │       └── IndicatorPanel.vue
  │   │
  │   └── timeseries/
  │       └── index.vue                # 分时图
  │
  ├── stock/
  │   ├── history/
  │   │   ├── index.vue                # 历史行情
  │   │   └── components/
  │   │       ├── DateRangePicker.vue
  │   │       └── HistoryChart.vue
  │   │
  │   └── realtime/
  │       └── index.vue                # 实时行情
  │
  ├── finance/
  │   ├── reports/
  │   │   └── index.vue                # 财务报表
  │   ├── metrics/
  │   │   └── index.vue                # 财务指标
  │   └── peer/
  │       └── index.vue                # 同业对比
  │
  ├── picker/
  │   ├── filter/
  │   │   └── index.vue                # 条件选股
  │   ├── hot/
  │   │   └── index.vue                # 热门股票
  │   └── backtest/
  │       └── index.vue                # 策略回测
  │
  ├── watchlist/
  │   ├── crud/
  │   │   └── index.vue                # 自选股管理
  │   ├── groups/
  │   │   └── index.vue                # 分组管理
  │   └── alerts/
  │       └── index.vue                # 价格提醒
  │
  ├── news/
  │   ├── realtime/
  │   │   └── index.vue                # 实时资讯
  │   └── announcements/
  │       └── index.vue                # 公司公告
  │
  ├── user/
  │   ├── profile/
  │   │   ├── index.vue                # 个人中心（重构后）
  │   │   └── components/
  │   │       ├── ProfileTab.vue
  │   │       ├── SecurityTab.vue
  │   │       ├── PreferencesTab.vue
  │   │       └── StatisticsTab.vue
  │   │
  │   └── permissions/
  │       └── index.vue                # 权限管理
  │
  └── login/
      └── index.vue                    # 登录页
```

---

### 1.4 样式规范化

#### SCSS 变量管理
**位置：** `src/styles/`

```
styles/
  ├── variables.scss           # SCSS 变量
  ├── mixins.scss             # SCSS 混合
  ├── functions.scss          # SCSS 函数
  ├── animations.scss         # 动画定义
  ├── utilities.scss          # 工具类
  ├── reset.scss              # 样式重置
  ├── global.scss             # 全局样式
  └── themes/
      ├── default.scss        # 默认主题
      └── dark.scss           # 暗色主题（预留）
```

#### CSS 模块化
- 使用 `<style scoped>` 避免样式污染
- 使用 CSS Modules 命名
- BEM 命名规范（Block-Element-Modifier）

---

### 1.5 TypeScript 类型定义

**位置：** `src/types/`

```
types/
  ├── api/
  │   ├── stock.d.ts          # 股票接口类型
  │   ├── company.d.ts        # 公司接口类型
  │   ├── user.d.ts           # 用户接口类型
  │   └── common.d.ts         # 通用接口类型
  │
  ├── models/
  │   ├── Stock.ts            # 股票模型
  │   ├── Company.ts          # 公司模型
  │   ├── User.ts             # 用户模型
  │   └── Chart.ts            # 图表模型
  │
  ├── store/
  │   ├── auth.d.ts           # Auth Store 类型
  │   ├── user.d.ts           # User Store 类型
  │   └── watchlist.d.ts      # Watchlist Store 类型
  │
  └── global.d.ts             # 全局类型声明
```

---

## 2. 后端重构方案

### 2.1 API 路由分层

#### 当前问题
- ❌ 单个文件包含多个领域接口
- ❌ 缺少版本控制
- ❌ 缺少接口分组

#### 优化方案

**位置：** `app/apis/`

```
apis/
  ├── __init__.py
  ├── v1/                          # API 版本 1
  │   ├── __init__.py
  │   ├── auth.py                  # 认证接口
  │   ├── user.py                  # 用户接口
  │   │
  │   ├── stock/                   # 股票模块
  │   │   ├── __init__.py
  │   │   ├── realtime.py         # 实时行情
  │   │   ├── history.py          # 历史数据
  │   │   ├── search.py           # 股票搜索
  │   │   └── trade_dates.py      # 交易日历
  │   │
  │   ├── company/                 # 公司模块
  │   │   ├── __init__.py
  │   │   ├── profile.py          # 公司概况
  │   │   ├── search.py           # 公司搜索
  │   │   └── industry.py         # 行业分类
  │   │
  │   ├── market/                  # 市场模块
  │   │   ├── __init__.py
  │   │   ├── summary.py          # 市场概况
  │   │   └── indices.py          # 指数数据
  │   │
  │   ├── finance/                 # 财务模块
  │   │   ├── __init__.py
  │   │   ├── reports.py          # 财务报表
  │   │   ├── metrics.py          # 财务指标
  │   │   └── peer.py             # 同业对比
  │   │
  │   ├── watchlist/               # 自选股模块
  │   │   ├── __init__.py
  │   │   ├── crud.py             # 增删改查
  │   │   ├── groups.py           # 分组管理
  │   │   └── alerts.py           # 提醒管理
  │   │
  │   └── news/                    # 资讯模块
  │       ├── __init__.py
  │       ├── realtime.py         # 实时资讯
  │       └── announcements.py    # 公司公告
  │
  └── v2/                          # API 版本 2（预留）
      └── __init__.py
```

---

### 2.2 Service 层重构

**位置：** `app/services/`

```
services/
  ├── __init__.py
  ├── base_service.py              # 基础服务类
  │
  ├── stock/
  │   ├── __init__.py
  │   ├── realtime_service.py      # 实时行情服务
  │   ├── history_service.py       # 历史数据服务
  │   ├── search_service.py        # 搜索服务
  │   └── trade_date_service.py    # 交易日服务
  │
  ├── company/
  │   ├── __init__.py
  │   ├── profile_service.py       # 公司概况服务
  │   ├── search_service.py        # 搜索服务
  │   └── industry_service.py      # 行业服务
  │
  ├── market/
  │   ├── __init__.py
  │   ├── summary_service.py       # 市场概况服务
  │   └── indices_service.py       # 指数服务
  │
  ├── finance/
  │   ├── __init__.py
  │   ├── reports_service.py       # 财务报表服务
  │   ├── metrics_service.py       # 财务指标服务
  │   └── peer_service.py          # 同业对比服务
  │
  ├── user/
  │   ├── __init__.py
  │   ├── profile_service.py       # 用户资料服务
  │   └── preferences_service.py   # 偏好设置服务
  │
  ├── watchlist/
  │   ├── __init__.py
  │   ├── crud_service.py          # CRUD服务
  │   ├── group_service.py         # 分组服务
  │   └── alert_service.py         # 提醒服务
  │
  ├── news/
  │   ├── __init__.py
  │   ├── realtime_service.py      # 实时资讯服务
  │   └── announcement_service.py  # 公告服务
  │
  ├── cache/
  │   ├── __init__.py
  │   ├── redis_service.py         # Redis缓存
  │   └── memory_service.py        # 内存缓存
  │
  └── external/
      ├── __init__.py
      ├── akshare_client.py        # AKShare客户端封装
      └── tushare_client.py        # TuShare客户端（预留）
```

---

### 2.3 数据模型重构

**位置：** `app/models/`

```
models/
  ├── __init__.py
  ├── base.py                      # 基础模型类
  │
  ├── user/
  │   ├── __init__.py
  │   ├── user.py                  # 用户模型
  │   ├── role.py                  # 角色模型
  │   └── permission.py            # 权限模型
  │
  ├── stock/
  │   ├── __init__.py
  │   ├── stock_info.py            # 股票信息
  │   ├── stock_quote.py           # 股票行情
  │   └── trade_date.py            # 交易日
  │
  ├── company/
  │   ├── __init__.py
  │   ├── company_info.py          # 公司信息
  │   └── company_finance.py       # 公司财务
  │
  ├── watchlist/
  │   ├── __init__.py
  │   ├── watchlist.py             # 自选股
  │   ├── watchlist_group.py       # 自选股分组
  │   └── price_alert.py           # 价格提醒
  │
  └── news/
      ├── __init__.py
      ├── news.py                  # 新闻
      └── announcement.py          # 公告
```

---

### 2.4 Schema 重构

**位置：** `app/schemas/`

```
schemas/
  ├── __init__.py
  ├── base.py                      # 基础Schema
  │
  ├── common/
  │   ├── __init__.py
  │   ├── response.py              # 统一响应格式
  │   ├── pagination.py            # 分页Schema
  │   └── query.py                 # 查询参数Schema
  │
  ├── user/
  │   ├── __init__.py
  │   ├── user_schema.py           # 用户Schema
  │   ├── auth_schema.py           # 认证Schema
  │   └── profile_schema.py        # 资料Schema
  │
  ├── stock/
  │   ├── __init__.py
  │   ├── stock_schema.py          # 股票Schema
  │   ├── quote_schema.py          # 行情Schema
  │   └── search_schema.py         # 搜索Schema
  │
  ├── company/
  │   ├── __init__.py
  │   ├── company_schema.py        # 公司Schema
  │   └── industry_schema.py       # 行业Schema
  │
  └── watchlist/
      ├── __init__.py
      ├── watchlist_schema.py      # 自选股Schema
      └── alert_schema.py          # 提醒Schema
```

---

### 2.5 工具类重构

**位置：** `app/utils/`

```
utils/
  ├── __init__.py
  ├── datetime_utils.py            # 日期时间工具
  ├── string_utils.py              # 字符串工具
  ├── number_utils.py              # 数字工具
  ├── validation_utils.py          # 验证工具
  ├── encryption_utils.py          # 加密工具
  ├── cache_utils.py               # 缓存工具
  ├── logger.py                    # 日志工具
  └── response_utils.py            # 响应工具
```

---

## 3. 命名规范标准化

### 3.1 前端命名规范

#### 文件命名
- **组件文件：** PascalCase（大驼峰）
  - ✅ `CompanySearchPanel.vue`
  - ❌ `companySearchPanel.vue`
  - ❌ `company-search-panel.vue`

- **视图文件：** index.vue（统一入口）
  - ✅ `views/market/snapshot/index.vue`
  - ❌ `views/market/Snapshot.vue`

- **工具文件：** camelCase（小驼峰）
  - ✅ `formatDate.ts`
  - ✅ `requestUtils.ts`
  - ❌ `FormatDate.ts`

- **常量文件：** UPPER_SNAKE_CASE
  - ✅ `API_CONSTANTS.ts`
  - ✅ `APP_CONFIG.ts`

#### 变量命名
```typescript
// 组件
const UserProfile = defineComponent({...})

// 变量（camelCase）
const userName = ref('')
const isLoading = ref(false)
const hasPermission = computed(() => ...)

// 常量（UPPER_SNAKE_CASE）
const API_BASE_URL = 'http://localhost:8000'
const MAX_RETRY_COUNT = 3

// 类型/接口（PascalCase）
interface UserInfo { ... }
type StockData = { ... }

// 枚举（PascalCase）
enum UserRole {
  Admin = 'admin',
  User = 'user'
}

// 函数（camelCase）
function getUserInfo() { ... }
const handleClick = () => { ... }

// 事件处理（handle + 动词）
const handleSubmit = () => { ... }
const handleSearch = () => { ... }
```

---

### 3.2 后端命名规范

#### 文件命名
- **模块文件：** snake_case（下划线）
  - ✅ `user_service.py`
  - ✅ `stock_realtime.py`
  - ❌ `UserService.py`
  - ❌ `stockRealtime.py`

- **类文件：** PascalCase（如果文件只包含一个类）
  - ✅ `User.py`（模型类）
  - ✅ `UserService.py`（服务类）

#### 变量命名
```python
# 类名（PascalCase）
class UserService:
    pass

class StockQuote:
    pass

# 函数名（snake_case）
def get_user_info():
    pass

def search_companies_by_industry():
    pass

# 变量（snake_case）
user_name = "admin"
is_active = True
stock_code = "000001"

# 常量（UPPER_SNAKE_CASE）
API_VERSION = "v1"
MAX_PAGE_SIZE = 100
DEFAULT_TIMEOUT = 30

# 私有变量（下划线前缀）
_internal_cache = {}
_db_connection = None

# 数据库字段（snake_case）
created_at = Column(DateTime)
updated_at = Column(DateTime)
```

#### API 路由命名
```python
# RESTful 风格
GET    /api/v1/stocks                  # 获取列表
GET    /api/v1/stocks/{id}             # 获取详情
POST   /api/v1/stocks                  # 创建
PUT    /api/v1/stocks/{id}             # 更新
DELETE /api/v1/stocks/{id}             # 删除

# 资源嵌套
GET    /api/v1/companies/{id}/stocks   # 获取公司的股票
GET    /api/v1/users/{id}/watchlists   # 获取用户自选股

# 操作动词（非RESTful场景）
POST   /api/v1/stocks/search           # 搜索
POST   /api/v1/auth/login              # 登录
POST   /api/v1/auth/logout             # 登出
```

---

### 3.3 数据库命名规范

```sql
-- 表名：snake_case（复数）
CREATE TABLE users (...);
CREATE TABLE stock_quotes (...);
CREATE TABLE company_profiles (...);

-- 字段名：snake_case
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    user_name VARCHAR(50),
    created_at DATETIME,
    updated_at DATETIME,
    is_active BOOLEAN DEFAULT TRUE
);

-- 索引名：idx_{table}_{column}
CREATE INDEX idx_users_user_name ON users(user_name);
CREATE INDEX idx_stocks_code ON stocks(stock_code);

-- 外键名：fk_{table}_{ref_table}
ALTER TABLE watchlists 
ADD CONSTRAINT fk_watchlists_users 
FOREIGN KEY (user_id) REFERENCES users(id);
```

---

## 4. 项目结构优化

### 4.1 前端最终结构

```
financial-analysis-admin/
├── public/
│   ├── favicon.ico
│   └── index.html
│
├── src/
│   ├── api/                         # API 接口
│   │   ├── modules/
│   │   │   ├── auth.ts
│   │   │   ├── user.ts
│   │   │   ├── stock.ts
│   │   │   ├── company.ts
│   │   │   ├── market.ts
│   │   │   ├── finance.ts
│   │   │   ├── watchlist.ts
│   │   │   └── news.ts
│   │   ├── interceptors.ts          # 拦截器
│   │   └── index.ts
│   │
│   ├── assets/                      # 静态资源
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   │
│   ├── components/                  # 组件
│   │   ├── atomic/                  # 原子组件
│   │   ├── business/                # 业务组件
│   │   ├── layout/                  # 布局组件
│   │   └── features/                # 功能组件
│   │
│   ├── composables/                 # 组合式API
│   │   ├── useStock.ts
│   │   ├── useCompany.ts
│   │   ├── useChart.ts
│   │   └── ...
│   │
│   ├── config/                      # 配置
│   │   ├── menu.ts                  # 菜单配置
│   │   ├── routes.ts                # 路由配置
│   │   └── app.ts                   # 应用配置
│   │
│   ├── directives/                  # 自定义指令
│   │   ├── permission.ts
│   │   └── loading.ts
│   │
│   ├── layout/                      # 布局
│   │   └── AppLayout.vue
│   │
│   ├── plugins/                     # 插件
│   │   ├── element-plus.ts
│   │   └── echarts.ts
│   │
│   ├── router/                      # 路由
│   │   ├── modules/
│   │   │   ├── market.ts
│   │   │   ├── stock.ts
│   │   │   └── ...
│   │   ├── guards.ts                # 路由守卫
│   │   └── index.ts
│   │
│   ├── store/                       # 状态管理
│   │   ├── modules/
│   │   │   ├── auth.ts
│   │   │   ├── user.ts
│   │   │   ├── watchlist.ts
│   │   │   └── ...
│   │   └── index.ts
│   │
│   ├── styles/                      # 样式
│   │   ├── variables.scss
│   │   ├── mixins.scss
│   │   ├── animations.scss
│   │   ├── global.scss
│   │   └── themes/
│   │
│   ├── types/                       # 类型定义
│   │   ├── api/
│   │   ├── models/
│   │   ├── store/
│   │   └── global.d.ts
│   │
│   ├── utils/                       # 工具函数
│   │   ├── format.ts                # 格式化
│   │   ├── validate.ts              # 验证
│   │   ├── request.ts               # 请求
│   │   └── storage.ts               # 存储
│   │
│   ├── views/                       # 视图
│   │   ├── home/
│   │   ├── market/
│   │   ├── stock/
│   │   ├── finance/
│   │   ├── picker/
│   │   ├── watchlist/
│   │   ├── news/
│   │   ├── user/
│   │   └── login/
│   │
│   ├── App.vue
│   └── main.ts
│
├── .env.development                 # 开发环境变量
├── .env.production                  # 生产环境变量
├── .eslintrc.js                     # ESLint 配置
├── .prettierrc.js                   # Prettier 配置
├── tsconfig.json                    # TypeScript 配置
├── vite.config.ts                   # Vite 配置
└── package.json
```

---

### 4.2 后端最终结构

```
financial-analysis-api/
├── app/
│   ├── apis/                        # API 路由
│   │   ├── v1/
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── stock/
│   │   │   ├── company/
│   │   │   ├── market/
│   │   │   ├── finance/
│   │   │   ├── watchlist/
│   │   │   └── news/
│   │   └── v2/
│   │
│   ├── core/                        # 核心模块
│   │   ├── config.py                # 配置
│   │   ├── database.py              # 数据库
│   │   ├── security.py              # 安全
│   │   ├── middleware.py            # 中间件
│   │   ├── exceptions.py            # 异常
│   │   └── dependencies.py          # 依赖
│   │
│   ├── models/                      # 数据模型
│   │   ├── base.py
│   │   ├── user/
│   │   ├── stock/
│   │   ├── company/
│   │   ├── watchlist/
│   │   └── news/
│   │
│   ├── schemas/                     # Pydantic Schema
│   │   ├── base.py
│   │   ├── common/
│   │   ├── user/
│   │   ├── stock/
│   │   ├── company/
│   │   ├── watchlist/
│   │   └── news/
│   │
│   ├── services/                    # 业务逻辑
│   │   ├── base_service.py
│   │   ├── stock/
│   │   ├── company/
│   │   ├── market/
│   │   ├── finance/
│   │   ├── user/
│   │   ├── watchlist/
│   │   ├── news/
│   │   ├── cache/
│   │   └── external/
│   │
│   ├── utils/                       # 工具函数
│   │   ├── datetime_utils.py
│   │   ├── string_utils.py
│   │   ├── number_utils.py
│   │   ├── validation_utils.py
│   │   ├── encryption_utils.py
│   │   ├── cache_utils.py
│   │   ├── logger.py
│   │   └── response_utils.py
│   │
│   └── main.py                      # 应用入口
│
├── migrations/                      # 数据库迁移
│   ├── versions/
│   └── env.py
│
├── scripts/                         # 脚本
│   ├── init_db.py
│   └── seed_data.py
│
├── tests/                           # 测试
│   ├── unit/
│   ├── integration/
│   └── conftest.py
│
├── .env                             # 环境变量
├── .env.example                     # 环境变量示例
├── alembic.ini                      # Alembic 配置
├── pytest.ini                       # Pytest 配置
├── requirements.txt                 # 依赖
└── main.py                          # 启动文件
```

---

## 5. 执行计划

### 阶段 1：前端组件拆分（Week 1-2）
- [ ] 创建 atomic 组件库
- [ ] 创建 business 组件库
- [ ] 抽取 composables
- [ ] 重构 Snapshot.vue（最大组件）
- [ ] 重构 Profile.vue
- [ ] 重构 KLine.vue

### 阶段 2：前端视图重构（Week 2-3）
- [ ] 重构视图目录结构
- [ ] 拆分大型视图文件
- [ ] 统一使用 index.vue 入口
- [ ] 移除重复代码

### 阶段 3：前端类型系统（Week 3）
- [ ] 定义 API 接口类型
- [ ] 定义模型类型
- [ ] 定义 Store 类型
- [ ] 完善全局类型声明

### 阶段 4：后端 API 重构（Week 4）
- [ ] 按模块拆分 API 路由
- [ ] 实现 v1 版本 API
- [ ] 添加 API 版本控制
- [ ] 统一响应格式

### 阶段 5：后端 Service 重构（Week 5）
- [ ] 拆分 stock_service.py
- [ ] 创建模块化服务
- [ ] 抽取公共基类
- [ ] 实现缓存层

### 阶段 6：后端模型重构（Week 6）
- [ ] 按模块组织模型
- [ ] 拆分大型模型文件
- [ ] 定义模型关系
- [ ] 添加模型验证

### 阶段 7：测试与优化（Week 7-8）
- [ ] 前端单元测试
- [ ] 后端单元测试
- [ ] 集成测试
- [ ] 性能测试
- [ ] 代码审查
- [ ] 文档更新

---

## 📊 预期效果

### 代码质量
- ✅ 单文件代码量 < 300 行
- ✅ 组件复用率 > 60%
- ✅ 测试覆盖率 > 80%
- ✅ TypeScript 类型覆盖 100%

### 性能提升
- ✅ 首屏加载时间 < 2s
- ✅ 接口响应时间 < 500ms
- ✅ 组件懒加载率 > 80%

### 开发效率
- ✅ 新功能开发周期 -30%
- ✅ Bug 修复时间 -50%
- ✅ 代码审查时间 -40%

---

## 📝 注意事项

1. **渐进式重构**：不要一次性重构所有代码，按模块逐步进行
2. **保持向后兼容**：重构过程中保持API兼容性
3. **充分测试**：每个阶段完成后进行充分测试
4. **文档同步**：及时更新技术文档
5. **团队协作**：定期代码审查，保持代码风格统一

---

**文档版本：** 1.0  
**最后更新：** 2025-01-16  
**维护者：** 开发团队
