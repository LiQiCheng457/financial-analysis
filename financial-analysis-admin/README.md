# 金融分析系统 - 前端管理平台

基于 Vue 3 + TypeScript + Element Plus 的现代化金融数据分析与量化策略平台。

## 📊 项目简介

面向A股市场的综合性金融分析系统前端项目，集成行情查询、技术指标分析、财务指标展示、AI量化策略等功能模块。

**核心特性**：
- 🎯 技术分析：MA、MACD、KDJ、RSI、BOLL等20+技术指标
- 🔍 智能选股：股票搜索、行业筛选、搜索历史
- 📈 信号检测：买卖信号识别、综合评分、交易建议
- 💼 财务分析：估值指标、盈利能力、财务健康度
- 🤖 AI策略：行业轮动策略、量化回测报告
- 📊 数据可视化：ECharts金融图表、K线、热力图

## 🛠️ 技术栈

- **Vue 3.4+** + **TypeScript 5.0+** + **Vite 4.5+**
- **Element Plus** + **ECharts 5.x**
- **Pinia** + **Vue Router 4** + **Axios**

## 📦 项目结构

```
financial-analysis-admin/
├── src/
│   ├── api/              # API接口定义
│   ├── components/       # 公共组件
│   ├── views/            # 页面视图
│   ├── router/           # 路由配置
│   ├── store/            # 状态管理
│   └── utils/            # 工具函数
├── public/               # 静态资源
└── ...
```

## � 快速开始

### 环境要求

- Node.js >= 16.x
- pnpm >= 8.x
- Git

### 配置与启动

#### 1. 克隆项目

```bash
# 克隆仓库
git clone https://github.com/LiQiCheng457/financial-analysis.git

# 进入前端目录
cd financial-analysis/financial-analysis-admin
```

#### 2. 安装依赖

```bash
# 使用 pnpm 安装（推荐）
pnpm install

# 或使用 npm
npm install
```

#### 3. 配置环境变量

创建 `.env.local` 文件：

```bash
# API 基础地址（后端服务地址）
VITE_API_BASE_URL=http://localhost:8000

# WebSocket 地址（实时推送）
VITE_WS_URL=ws://localhost:8000/ws
```

#### 4. 启动开发服务器

```bash
# 启动开发服务
pnpm run dev

# 服务将运行在 http://localhost:5173
```

#### 5. 构建生产版本

```bash
# 构建生产版本
pnpm run build

# 预览构建结果
pnpm run preview
```

## 🔧 可用脚本

```bash
# 开发服务
pnpm run dev

# 构建生产版本
pnpm run build

# 预览构建结果
pnpm run preview

# 代码检查
pnpm run lint            # ESLint 检查并修复
pnpm run lint:check      # ESLint 仅检查
pnpm run format          # Prettier 格式化
pnpm run format:check    # Prettier 检查格式
pnpm run type-check      # TypeScript 类型检查
```

## 🐛 常见问题

### 1. 安装依赖失败

```bash
# 清除缓存并重新安装
pnpm store prune
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### 2. 接口请求跨域

后端需要配置 CORS，或在开发环境使用 Vite 代理：

```typescript
// vite.config.ts
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})
```

### 3. Sass 编译错误

```bash
pnpm add -D sass
```

## 📝 开发规范

- 代码风格：遵循 ESLint + Prettier 配置
- 组件命名：PascalCase
- 文件命名：kebab-case
- Git提交：参考 [GIT_COMMIT_CONVENTION.md](./GIT_COMMIT_CONVENTION.md)

详细规范请查看 [CODE_STYLE.md](./CODE_STYLE.md)

---

## ✅ 已完成功能详细列表

### 1. 市场分析模块

#### 1.1 公司概况查询 (`/market/snapshot`)
- ✅ 公司搜索（代码/名称/行业）
- ✅ 行业标签筛选（8大类50+标签）
- ✅ 公司详情展示
  - 基本信息表格
  - 股票走势K线图
  - **💰 财务指标页**（新增）
  - 经营范围
  - 公司简介
- ✅ 搜索历史记录
- ✅ 分页查询

#### 1.2 技术指标分析 (`/market/technical`)
- ✅ 统一股票搜索组件
  - 70+常用股票预加载
  - 搜索历史记录（最多50条）
  - 收藏功能集成
- ✅ 20+技术指标计算与展示
  - MA (5/10/20/60日均线)
  - MACD (快线/慢线/柱状图)
  - KDJ (随机指标)
  - RSI (相对强弱指标)
  - BOLL (布林带)
  - VOL (成交量)
- ✅ 多周期切换（日线/周线/月线）
- ✅ K线图表展示（ECharts）
- ✅ 指标说明文档
- ✅ **🎯 技术信号检测**（新增）
  - MACD 金叉/死叉
  - KDJ 超买/超卖
  - RSI 超买/超卖
  - MA 金叉/死叉
  - BOLL 突破信号
  - 成交量异常
- ✅ **📊 综合交易建议**（新增）
  - 0-100 分综合评分
  - 买入/卖出/中性评级
  - 止损价/目标价计算
  - 信号强度评估（1-5星）

#### 1.3 每日概况 (`/market/summary`)
- ✅ 市场指数概览
- ⏳ 涨跌幅排行榜（待优化）

### 2. 财务分析模块

#### 2.1 财务指标组件 (`FinancialMetrics.vue`)
- ✅ **估值指标**
  - PE（市盈率）- 智能评价
  - PB（市净率）- 智能评价
  - PS（市销率）
  - 股息率 - 智能评价
- ✅ **盈利能力**
  - ROE（净资产收益率）- 智能评价
  - ROA（总资产收益率）
  - 毛利率
  - 净利率 - 智能评价
- ✅ **财务健康度**
  - 资产负债率 - 智能评价
  - 流动比率 - 智能评价
  - 速动比率
  - 现金流健康度
- ✅ **可视化图表**
  - 营收与利润趋势（近4年）
  - ROE趋势图（近4年）
- ✅ **综合评分**
  - 0-100分财务评分
  - 优秀/良好/一般/较差评级

**📝 注意**：当前使用模拟数据，待接入真实财务API

### 3. AI量化策略模块 🤖

#### 3.1 行业轮动策略 (`/strategy/industry-rotation`)
- ✅ **核心绩效指标**
  - 总收益率：27.05%
  - 年化收益：13.13%
  - 夏普比率：1.53
  - 最大回撤：-22.71%
  - 交易次数：285次
  - 回测天数：95天
- ✅ **策略亮点展示**
  - 收益对比分析
  - 夏普比率评估
  - AI准确率统计
- ✅ **累计收益曲线**
  - 策略收益 vs 沪深300基准
  - 交互式 ECharts 图表
  - 支持日收益/累计收益切换
- ✅ **回撤分析图**
  - 实时回撤曲线
  - 最大回撤标注
- ✅ **当前推荐行业配置**
  - 8大行业置信度评分
  - 强烈推荐/推荐/持有/规避评级
  - 可视化进度条
- ✅ **行业配置分析**
  - 行业持仓占比饼图
  - 月度收益柱状图
- ✅ **行业轮动热力图**
  - 24个月 × 8个行业
  - 收益率颜色映射
- ✅ **模型信息展示**
  - 架构：双向LSTM + 注意力机制
  - 方向准确率：67.87%
  - Top 20%准确率：79.98%
  - 参数量：3,992,706
  - 训练数据：865,477样本
  - 特征维度：50个技术指标

**📝 注意**：当前使用模拟数据，展示UI框架

### 4. 自选股模块
- ⏳ 增删改查（待完善）
- ⏳ 分组管理（待完善）
- ⏳ 涨跌提醒（待完善）

### 5. 选股器模块
- ⏳ 条件筛选（待开发）
- ⏳ 策略回测（待开发）
- ⏳ 热门策略（待开发）

### 6. 新闻资讯模块
- ⏳ 实时新闻（待开发）
- ⏳ 公司公告（待开发）

### 7. 用户系统
- ✅ 登录/登出
- ✅ 用户信息展示
- ⏳ 权限管理（待开发）

---

## 🚧 待接入的后端API列表

### 高优先级 API

#### 1. 财务指标API
```python
GET /api/company/{stock_code}/financial_metrics
```
**返回数据**：
- 估值指标：PE, PB, PS, 股息率
- 盈利能力：ROE, ROA, 毛利率, 净利率
- 财务健康：资产负债率, 流动比率, 速动比率
- 历史趋势：近4年营收、利润、ROE数据

**当前状态**：前端UI已完成，使用模拟数据

---

#### 2. AI策略预测API
```python
GET /api/strategy/industry-rotation/prediction
```
**返回数据**：
- 8大行业涨跌预测
- 预测置信度
- 推荐操作（买入/持有/卖出）
- 预测周期（1天/5天/20天）

**当前状态**：前端UI已完成，使用模拟数据

---

#### 3. AI策略回测API
```python
GET /api/strategy/industry-rotation/backtest
```
**返回数据**：
- 累计收益曲线数据
- 回撤曲线数据
- 月度收益数据
- 行业配置历史
- 行业轮动热力图数据

**当前状态**：前端UI已完成，使用模拟数据

---

### 中优先级 API

#### 4. 技术信号历史API
```python
GET /api/stocks/{stock_code}/signal_history
```
**返回数据**：
- 历史信号记录
- 信号准确率统计
- 信号成功率分析

**当前状态**：信号检测功能已完成，历史追踪待实现

---

#### 5. 实时信号推送API
```python
WebSocket /ws/signals
```
**推送数据**：
- 实时信号触发通知
- 关注股票价格变动
- 行业推荐更新

**当前状态**：待开发

---

### 低优先级 API

#### 6. 选股器API
```python
POST /api/picker/filter
GET /api/picker/backtest
GET /api/picker/hot_strategies
```

#### 7. 新闻资讯API
```python
GET /api/news/realtime
GET /api/news/announcements
```

---

## 🎯 待优化功能清单

### 1. 技术分析优化

- [ ] **图表信号标注**
  - 在K线图上直接标注买卖信号点
  - 信号点点击查看详情
  - 历史信号回顾

- [ ] **多股对比**
  - 同时查看多只股票技术指标
  - 相关性分析
  - 强弱对比

- [ ] **指标自定义**
  - 用户自定义指标参数
  - 保存常用指标组合
  - 指标预设模板

### 2. 财务分析优化

- [ ] **同行业对比**
  - 选择对比公司
  - 财务指标横向对比
  - 行业排名展示

- [ ] **财务趋势预测**
  - 基于历史数据的趋势预测
  - 增长率分析
  - 风险预警

- [ ] **财务报表详情**
  - 资产负债表
  - 利润表
  - 现金流量表

### 3. AI策略优化

- [ ] **参数化回测**
  - 自定义回测参数
  - 调仓周期设置
  - 持仓数量配置
  - 交易成本设置

- [ ] **策略对比**
  - 多策略并行展示
  - 绩效对比分析
  - 策略组合优化

- [ ] **实时信号订阅**
  - 用户关注行业设置
  - 信号推送通知
  - 邮件/短信提醒

- [ ] **行业详情页**
  - 点击行业查看详情
  - 行业内股票排行
  - 行业资金流向
  - 行业新闻资讯

### 4. 用户体验优化

- [ ] **搜索增强**
  - 搜索结果高亮
  - 智能推荐
  - 拼音搜索支持

- [ ] **数据缓存**
  - 本地缓存策略
  - 离线数据支持
  - 智能预加载

- [ ] **主题切换**
  - 暗色模式
  - 自定义配色
  - 护眼模式

- [ ] **移动端适配**
  - 响应式布局优化
  - 触摸手势支持
  - PWA支持

### 5. 性能优化

- [ ] **图表性能**
  - 大数据量渲染优化
  - 图表懒加载
  - 虚拟滚动

- [ ] **代码分割**
  - 路由懒加载
  - 组件异步加载
  - 按需加载优化

---

## 🔧 详细开发流程说明

### 新增功能开发流程

#### 1. 添加新页面

```bash
# 1. 创建页面组件
src/views/module-name/PageName.vue

# 2. 添加路由配置
src/router/index.ts

# 3. 添加菜单配置
src/config/menu.ts
```

**示例**：添加"资金流向"页面

```typescript
// 1. src/views/market/MoneyFlow.vue
<template>
  <PageShell title="资金流向">
    <!-- 页面内容 -->
  </PageShell>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getMoneyFlow } from '@/api/stock'
// 组件逻辑
</script>

// 2. src/router/index.ts
{
  path: '/market/money-flow',
  name: 'MoneyFlow',
  component: () => import('@/views/market/MoneyFlow.vue'),
  meta: { title: '资金流向', requiresAuth: true }
}

// 3. src/config/menu.ts
{
  path: '/market/money-flow',
  title: '资金流向',
  icon: 'TrendCharts'
}
```

#### 2. 添加API接口

```typescript
// src/api/stock.ts

/**
 * 获取资金流向数据
 * @param stockCode 股票代码
 * @param days 天数
 */
export const getMoneyFlow = async (
  stockCode: string, 
  days: number = 5
): Promise<MoneyFlowData> => {
  const response = await axios.get(
    `${API_BASE_URL}/api/stocks/${stockCode}/money-flow`,
    { params: { days } }
  )
  return response.data
}
```

**API规范**：
- 使用 TypeScript 类型定义
- 添加 JSDoc 注释
- 统一错误处理
- 使用 async/await

#### 3. 创建业务组件

```bash
src/components/business/MoneyFlowChart.vue
```

**组件规范**：
- 组件名使用 PascalCase
- Props 使用 TypeScript 定义
- 发出事件使用 defineEmits
- 使用 Composition API

```vue
<template>
  <div class="money-flow-chart">
    <div ref="chartRef" style="width: 100%; height: 400px"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * echarts from 'echarts'
import type { MoneyFlowData } from '@/types/stock'

interface Props {
  data: MoneyFlowData[]
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const emit = defineEmits<{
  refresh: []
}>()

const chartRef = ref<HTMLDivElement>()
let chartInstance: echarts.ECharts | null = null

// 组件逻辑...
</script>
```

#### 4. 类型定义

```typescript
// src/types/stock.ts

export interface MoneyFlowData {
  date: string
  mainInflow: number      // 主力流入
  mainOutflow: number     // 主力流出
  retailInflow: number    // 散户流入
  retailOutflow: number   // 散户流出
}

export interface MoneyFlowResponse {
  code: string
  name: string
  data: MoneyFlowData[]
}
```

#### 5. 状态管理（如需要）

```typescript
// src/store/market.ts
import { defineStore } from 'pinia'

export const useMarketStore = defineStore('market', {
  state: () => ({
    moneyFlowData: [] as MoneyFlowData[],
    loading: false
  }),
  
  actions: {
    async fetchMoneyFlow(stockCode: string) {
      this.loading = true
      try {
        const data = await getMoneyFlow(stockCode)
        this.moneyFlowData = data
      } finally {
        this.loading = false
      }
    }
  }
})
```

### 开发工作流

```bash
# 1. 创建功能分支
git checkout -b feature/money-flow

# 2. 开发功能
# - 编写代码
# - 运行开发服务器测试
pnpm run dev

# 3. 代码检查
pnpm run lint
pnpm run type-check
pnpm run format

# 4. 提交代码
git add .
git commit -m "feat(market): 添加资金流向功能

- 实现资金流向API接口
- 创建资金流向图表组件
- 添加资金流向页面
"

# 5. 推送并创建PR
git push origin feature/money-flow
```

---

## 📊 数据说明

### 模拟数据 vs 真实数据

当前系统部分模块使用模拟数据：

| 模块 | 数据来源 | 状态 |
|------|---------|------|
| 历史行情 | 真实API (AKShare) | ✅ 已接入 |
| 技术指标 | 真实计算 | ✅ 已完成 |
| 技术信号 | 真实检测 | ✅ 已完成 |
| 公司概况 | 真实API | ✅ 已接入 |
| **财务指标** | **模拟数据** | ⏳ 待接入 |
| **AI策略回测** | **模拟数据** | ⏳ 待接入 |
| **行业预测** | **模拟数据** | ⏳ 待接入 |

### 数据更新频率

| 数据类型 | 更新频率 | 延迟 |
|---------|---------|------|
| 日线数据 | 每日20:00后 | T+0 |
| 分钟数据 | 实时 | <1秒 |
| 财务数据 | 季度更新 | 财报发布后 |
| 公司信息 | 不定期 | - |

### 数据缓存策略

```typescript
// 前端缓存策略
const CACHE_CONFIG = {
  // 股票基本信息：缓存1天
  stockBasic: 24 * 60 * 60 * 1000,
  
  // 日线数据：缓存到当天20:00
  dailyData: 'until_20:00',
  
  // 技术指标：不缓存（实时计算）
  technicalIndicators: 0,
  
  // 财务数据：缓存7天
  financialData: 7 * 24 * 60 * 60 * 1000,
  
  // 搜索历史：永久存储
  searchHistory: Infinity
}
```

---

## 🎨 设计系统

### 颜色规范

```scss
// 主题色
--primary-color: #667eea;      // 主色调
--success-color: #67c23a;      // 成功/涨
--warning-color: #e6a23c;      // 警告
--danger-color: #f56c6c;       // 危险/跌
--info-color: #909399;         // 信息

// 文字色
--text-primary: #303133;       // 主要文字
--text-regular: #606266;       // 常规文字
--text-secondary: #909399;     // 次要文字
--text-placeholder: #c0c4cc;   // 占位文字

// 边框色
--border-base: #dcdfe6;
--border-light: #e4e7ed;
--border-lighter: #ebeef5;
--border-extra-light: #f2f6fc;

// 背景色
--bg-color: #f5f7fa;
--bg-white: #ffffff;

// 金融专用色
--color-up: #f5222d;          // 涨（红色）
--color-down: #52c41a;        // 跌（绿色）
--color-volume: rgba(102, 126, 234, 0.3);  // 成交量
```

### 图表配色方案

#### 技术指标颜色
```javascript
const INDICATOR_COLORS = {
  // 均线系列
  MA5: '#409eff',    // 蓝色
  MA10: '#e6a23c',   // 橙色
  MA20: '#67c23a',   // 绿色
  MA60: '#f56c6c',   // 红色
  
  // MACD
  DIF: '#409eff',    // 蓝色
  DEA: '#e6a23c',    // 橙色
  MACD: (val) => val >= 0 ? '#f5222d' : '#52c41a',
  
  // KDJ
  K: '#409eff',      // 蓝色
  D: '#e6a23c',      // 橙色
  J: '#67c23a',      // 绿色
  
  // BOLL
  UPPER: '#f56c6c',  // 红色
  MIDDLE: '#409eff', // 蓝色
  LOWER: '#67c23a',  // 绿色
}
```

#### K线图配色
```javascript
const KLINE_COLORS = {
  up: {
    stroke: '#f5222d',
    fill: '#f5222d'
  },
  down: {
    stroke: '#52c41a',
    fill: '#52c41a'
  }
}
```

### 字体规范

```scss
// 字体家族
--font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
--font-family-code: 'Consolas', 'Monaco', monospace;

// 字体大小
--font-size-extra-large: 20px;
--font-size-large: 18px;
--font-size-medium: 16px;
--font-size-base: 14px;
--font-size-small: 13px;
--font-size-extra-small: 12px;

// 字重
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-bold: 700;
```

### 间距规范

```scss
// 间距系统（4px基准）
--spacing-xs: 4px;
--spacing-sm: 8px;
--spacing-md: 16px;
--spacing-lg: 24px;
--spacing-xl: 32px;
--spacing-xxl: 48px;
```

### 圆角规范

```scss
--border-radius-small: 2px;
--border-radius-base: 4px;
--border-radius-large: 8px;
--border-radius-round: 20px;
--border-radius-circle: 50%;
```

### 阴影规范

```scss
--box-shadow-light: 0 2px 4px rgba(0, 0, 0, 0.12);
--box-shadow-base: 0 2px 12px rgba(0, 0, 0, 0.1);
--box-shadow-dark: 0 4px 16px rgba(0, 0, 0, 0.12);
```

### 组件尺寸规范

```scss
// 按钮
--button-height-large: 40px;
--button-height-default: 32px;
--button-height-small: 28px;

// 输入框
--input-height-large: 40px;
--input-height-default: 32px;
--input-height-small: 24px;

// 表格
--table-header-height: 48px;
--table-row-height: 48px;
```

### 响应式断点

```scss
// 断点定义
$breakpoints: (
  'xs': 0,        // 手机
  'sm': 768px,    // 平板
  'md': 992px,    // 小屏电脑
  'lg': 1200px,   // 桌面
  'xl': 1920px    // 大屏
);
```

### 图标使用规范

```vue
<!-- Element Plus 图标 -->
<el-icon :size="20" color="#409eff">
  <TrendCharts />
</el-icon>

<!-- 自定义尺寸 -->
<el-icon :size="16">  <!-- 小 -->
<el-icon :size="20">  <!-- 默认 -->
<el-icon :size="24">  <!-- 中 -->
<el-icon :size="32">  <!-- 大 -->
```

---

## 📖 相关文档

- [后端API文档](../financial-analysis-api/README.md)
- [代码规范](./CODE_STYLE.md)
- [Git提交规范](./GIT_COMMIT_CONVENTION.md)

## 📞 联系方式

- **GitHub**: https://github.com/LiQiCheng457/financial-analysis
- **Issues**: https://github.com/LiQiCheng457/financial-analysis/issues

## 📄 许可证

MIT License

---

**Version**: 1.0.0  
**Last Updated**: 2025-11-01
