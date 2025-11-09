<template>
  <div class="home-dashboard">
    <!-- 顶部：标题 + 时间范围切换 + 用户欢迎/版本 -->
    <div class="top-bar">
      <div class="title-block">
        <h1>智能证券分析系统</h1>
        <div class="sub">实时行情 · 数据分析 · 智能决策</div>
      </div>

      <div class="controls">
        <el-radio-group v-model="range" size="small">
          <el-radio-button label="today">Today</el-radio-button>
          <el-radio-button label="7d">7D</el-radio-button>
          <el-radio-button label="30d">30D</el-radio-button>
        </el-radio-group>
        <div class="meta">欢迎, {{ user }} · 版本 {{ version }}</div>
      </div>
    </div>

    <!-- 第一行：KPI 卡片 -->
    <div class="kpi-row">
      <div class="kpi" v-for="(k, idx) in kpis" :key="idx">
        <div class="kpi-title">{{ k.label }}</div>
        <div class="kpi-value">{{ k.value }}</div>
        <div class="kpi-sub">{{ k.sub }}</div>
      </div>
    </div>

    <!-- 第二行：折线图 + Top Movers -->
    <div class="row">
      <div class="col left">
        <div class="card">
          <div class="card-head">总资产趋势</div>
          <stock-chart :mock-series="chart.series" />
        </div>
      </div>
      <div class="col right">
        <div class="card">
          <div class="card-head">今日涨跌榜</div>
          <el-table :data="topMovers" stripe size="small" style="width:100%">
            <el-table-column prop="symbol" label="代码" width="100"/>
            <el-table-column prop="name" label="名称"/>
            <el-table-column prop="price" label="最新价" width="90"/>
            <el-table-column prop="change_pct" label="涨跌%" width="90">
              <template #default="{ row }">
                <span :class="{'pos': row.change_pct>0,'neg': row.change_pct<0}">{{ row.change_pct }}%</span>
              </template>
            </el-table-column>
            <el-table-column prop="volume" label="成交量" width="120"/>
          </el-table>
        </div>

        <div class="card" style="margin-top:12px">
          <div class="card-head">成交量榜</div>
          <el-table :data="topVolume" stripe size="small" style="width:100%">
            <el-table-column prop="symbol" label="代码" width="100"/>
            <el-table-column prop="name" label="名称"/>
            <el-table-column prop="volume" label="成交量" width="120"/>
            <el-table-column prop="price" label="最新价" width="90"/>
          </el-table>
        </div>
      </div>
    </div>

    <!-- 第三行：持仓/时间线/快速操作 -->
    <div class="row third">
      <div class="col third-left">
        <div class="card">
          <div class="card-head">持仓概览</div>
          <div class="portfolio">
            <div class="pv">组合市值：<strong>{{ currency(portfolio.total_value) }}</strong></div>
            <div class="pv small">浮动盈亏：{{ currency(portfolio.profit_today) }}</div>
            <el-table :data="portfolio.holdings" size="small" style="width:100%">
              <el-table-column prop="symbol" label="代码" width="100"/>
              <el-table-column prop="amount" label="持仓" width="90"/>
              <el-table-column prop="market_value" label="市值" width="120"/>
            </el-table>
          </div>
        </div>
      </div>

      <div class="col third-mid">
        <div class="card">
          <div class="card-head">最近活动</div>
          <ul class="activity-list">
            <li v-for="(a, i) in activities" :key="i">
              <div class="time">{{ a.time }}</div>
              <div class="msg">{{ a.msg }}</div>
            </li>
          </ul>
        </div>
      </div>

      <!-- 快速操作已移除 -->
    </div>

    <!-- 底部：系统日志 / 帮助 -->
    <div class="bottom">
      <div class="links">
        <a href="/docs" target="_blank">后端 API 文档</a> ·
        <a href="#" @click.prevent="openHelp">系统帮助</a>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import StockChart from '@/components/StockChart.vue'

// mock 数据（可替换为真实接口）
const user = 'admin'
const version = '1.0.0'
const range = ref('7d')

const kpis = ref([
  { label: '总用户数', value: 124, sub: '' },
  { label: '今日活跃', value: 18, sub: '' },
  { label: '跟踪股票数', value: 342, sub: '' },
  { label: '今日净变动', value: '1.86%', sub: '' }
])

const chart = ref({ series: [
  { date: '2025-10-28', value: 1000000 },
  { date: '2025-10-29', value: 1008500 },
  { date: '2025-10-30', value: 1012000 },
  { date: '2025-10-31', value: 1018000 },
  { date: '2025-11-01', value: 1023500 }
] })

const topMovers = ref([
  { symbol: '000858', name: '五粮液', price: 280.3, change_pct: 5.2, volume: 25000 },
  { symbol: '300750', name: '宁德时代', price: 410.1, change_pct: -2.1, volume: 18000 },
  { symbol: '600519', name: '贵州茅台', price: 1850.0, change_pct: 1.3, volume: 50000 },
  { symbol: '000001', name: '平安银行', price: 15.2, change_pct: 3.5, volume: 1200000 },
  { symbol: '002594', name: '比亚迪', price: 245.6, change_pct: 2.8, volume: 90000 }
])

const portfolio = ref({ total_value: 1200000, profit_today: 5200, holdings: [
  { symbol: '000001', amount: 1000, market_value: 15200 },
  { symbol: '600519', amount: 10, market_value: 18500 }
] })


const activities = ref([
  { time: '09:12', msg: 'admin 登录成功' },
  { time: '08:55', msg: '系统: 定时更新完成 300 条' },
  { time: '07:20', msg: '用户 liqi 导入持仓: 12 条' }
])

// 成交量榜（用于新增的榜单）
const topVolume = ref([
  { symbol: '000001', name: '平安银行', volume: 1200000, price: 15.2 },
  { symbol: '002594', name: '比亚迪', volume: 90000, price: 245.6 },
  { symbol: '600519', name: '贵州茅台', volume: 50000, price: 1850.0 },
  { symbol: '000858', name: '五粮液', volume: 25000, price: 280.3 },
  { symbol: '300750', name: '宁德时代', volume: 18000, price: 410.1 }
])

function openHelp() {
  alert('打开系统帮助（mock）')
}

// 简单过滤/格式化
function currency(val: number) {
  return (val || 0).toLocaleString('zh-CN', { style: 'currency', currency: 'CNY' })
}

// expose to template
defineExpose({})
</script>

<style scoped>
/* 基础布局 */
.home-dashboard { 
  padding: 16px;
  max-width: 100%;
  overflow-x: hidden;
}

.top-bar { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  margin-bottom: 16px;
  flex-wrap: wrap;
  gap: 12px;
}

.title-block h1 { 
  margin: 0; 
  font-size: 1.5rem;
  line-height: 1.2;
}

.title-block .sub { 
  color: #666; 
  font-size: 0.9rem;
  margin-top: 4px;
}

.controls { 
  display: flex; 
  align-items: center; 
  gap: 12px;
  flex-wrap: wrap;
}

.controls .meta { 
  color: #999; 
  font-size: 0.9rem;
  white-space: nowrap;
}

/* KPI 卡片 */
.kpi-row { 
  display: grid; 
  grid-template-columns: repeat(4, 1fr); 
  gap: 12px; 
  margin-bottom: 16px;
}

.kpi { 
  background: #fff; 
  padding: 16px; 
  border-radius: 8px; 
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  min-width: 0;
}

.kpi-title { 
  color: #666; 
  font-size: 0.85rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.kpi-value { 
  font-size: 1.4rem; 
  margin-top: 6px;
  word-break: break-all;
}

.kpi-sub { 
  color: #999; 
  font-size: 0.85rem;
}

/* 行布局 */
.row { 
  display: flex; 
  gap: 12px; 
  margin-bottom: 16px;
}

.col { 
  flex: 1;
  min-width: 0;
}

.col.left { 
  flex: 2;
}

.card { 
  background: #fff; 
  border-radius: 8px; 
  padding: 12px; 
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  overflow-x: auto;
}

.card-head { 
  font-weight: 600; 
  margin-bottom: 10px;
}

/* 第三行布局 */
.third { 
  display: flex; 
  gap: 12px;
}

.third-left { 
  flex: 1.5;
  min-width: 0;
}

.third-mid { 
  flex: 1;
  min-width: 0;
}

.third-right { 
  flex: 0.8;
  min-width: 0;
}

.activity-list { 
  list-style: none; 
  padding: 0; 
  margin: 0;
}

.activity-list li { 
  padding: 8px 0; 
  border-bottom: 1px dashed #eee;
}

.activity-list .time { 
  color: #999; 
  font-size: 0.85rem;
}

.ops { 
  display: flex; 
  flex-direction: column; 
  gap: 8px;
}

.bottom { 
  margin-top: 12px; 
  color: #666;
  text-align: center;
}

/* 涨跌颜色 */
.pos { color: #f5222d; }
.neg { color: #52c41a; }

/* 平板适配 (768px - 1024px) */
@media (max-width: 1024px) {
  .kpi-row { 
    grid-template-columns: repeat(2, 1fr);
  }
  
  .row { 
    flex-direction: column;
  }
  
  .col.left { 
    flex: 1;
  }
  
  .third { 
    flex-direction: column;
  }
  
  .title-block h1 { 
    font-size: 1.3rem;
  }
}

/* 手机适配 (小于 768px) */
@media (max-width: 768px) {
  .home-dashboard { 
    padding: 12px;
  }
  
  .top-bar { 
    flex-direction: column;
    align-items: flex-start;
  }
  
  .title-block h1 { 
    font-size: 1.2rem;
  }
  
  .title-block .sub { 
    font-size: 0.85rem;
  }
  
  .controls { 
    width: 100%;
    justify-content: space-between;
  }
  
  .kpi-row { 
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
  }
  
  .kpi { 
    padding: 12px;
  }
  
  .kpi-title { 
    font-size: 0.8rem;
  }
  
  .kpi-value { 
    font-size: 1.2rem;
  }
  
  .row { 
    gap: 8px;
  }
  
  .card { 
    padding: 10px;
  }
  
  .card-head { 
    font-size: 0.9rem;
  }
}

/* 超小屏幕适配 (小于 480px) */
@media (max-width: 480px) {
  .home-dashboard { 
    padding: 8px;
  }
  
  .title-block h1 { 
    font-size: 1.1rem;
  }
  
  .kpi-row { 
    grid-template-columns: 1fr;
    gap: 8px;
  }
  
  .kpi { 
    padding: 10px;
  }
  
  .controls .meta { 
    font-size: 0.8rem;
  }
  
  /* 表格在小屏幕上自适应 */
  :deep(.el-table) {
    font-size: 12px;
  }
  
  :deep(.el-table th),
  :deep(.el-table td) {
    padding: 8px 4px;
  }
  
  :deep(.el-radio-group) {
    display: flex;
    flex-wrap: wrap;
  }
  
  :deep(.el-radio-button) {
    margin-bottom: 4px;
  }
}

/* 横屏模式优化 */
@media (max-height: 600px) and (orientation: landscape) {
  .kpi-row { 
    grid-template-columns: repeat(4, 1fr);
  }
  
  .home-dashboard { 
    padding: 8px;
  }
  
  .kpi { 
    padding: 8px;
  }
}
</style>
