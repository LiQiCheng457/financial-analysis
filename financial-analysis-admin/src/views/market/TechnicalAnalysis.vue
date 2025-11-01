<template>
  <PageShell>
    <template #title>📈 技术指标分析</template>
    <template #subtitle>支持MA、MACD、KDJ、RSI、BOLL等核心技术指标</template>

    <div class="technical-analysis-container">
      <!-- 查询表单 -->
      <el-card class="query-card" shadow="hover">
        <el-form :inline="true" :model="queryForm" label-width="80px">
          <el-form-item label="股票搜索">
            <StockSearch 
              v-model="queryForm.code"
              @select="handleStockSelect"
              placeholder="输入代码或名称搜索"
              :show-favorites="true"
              :show-history="true"
              :show-actions="false"
              style="width: 300px"
            />
          </el-form-item>

          <el-form-item label="时间范围">
            <el-date-picker
              v-model="dateRange"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYYMMDD"
              :shortcuts="dateShortcuts"
              style="width: 350px"
            />
          </el-form-item>

          <el-form-item>
            <el-button 
              type="primary" 
              :icon="Search" 
              @click="loadData"
              :loading="loading"
            >
              查询分析
            </el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 加载状态 -->
      <el-skeleton :rows="8" animated v-if="loading && !chartData.length" style="margin-top: 20px" />

      <!-- 错误提示 -->
      <el-alert 
        v-if="errorMsg" 
        :title="errorMsg" 
        type="error" 
        show-icon 
        :closable="false" 
        style="margin-top: 20px"
      />

      <!-- 技术指标图表 -->
      <div v-if="!loading && chartData.length > 0" class="chart-section">
        <TechnicalChart 
          ref="chartRef" 
          :data="chartData" 
          :defaultIndicators="['MA', 'VOL']"
        />

        <!-- 技术信号检测 -->
        <div class="signals-section" style="margin-top: 20px">
          <TechnicalSignals 
            :signals="signals"
            :advice="tradingAdvice"
            :loading="signalsLoading"
          />
        </div>

        <!-- 数据统计信息 -->
        <el-card class="stats-card" shadow="hover" style="margin-top: 20px">
          <div class="stats-grid">
            <div class="stat-item">
              <div class="stat-label">数据范围</div>
              <div class="stat-value">{{ dataRange }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">数据条数</div>
              <div class="stat-value">{{ chartData.length }} 条</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">最新收盘</div>
              <div class="stat-value" :class="latestPriceClass">{{ latestClose }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-label">区间涨跌</div>
              <div class="stat-value" :class="rangeChangeClass">{{ rangeChange }}</div>
            </div>
          </div>
        </el-card>

        <!-- 技术指标说明 -->
        <el-card class="info-card" shadow="hover" style="margin-top: 20px">
          <template #header>
            <div class="card-header">
              <span>📊 技术指标说明</span>
            </div>
          </template>
          <el-collapse accordion>
            <el-collapse-item title="MA - 移动平均线" name="ma">
              <div class="indicator-desc">
                <p><strong>定义：</strong>一定周期内股价的算术平均值连线</p>
                <p><strong>用法：</strong></p>
                <ul>
                  <li>金叉：短期均线向上穿越长期均线，看涨信号</li>
                  <li>死叉：短期均线向下穿越长期均线，看跌信号</li>
                  <li>支撑/压力：股价回调至均线附近可能获得支撑或遇到压力</li>
                </ul>
                <p><strong>参数：</strong>MA5、MA10、MA20、MA60（常用周期）</p>
              </div>
            </el-collapse-item>

            <el-collapse-item title="MACD - 平滑异同移动平均线" name="macd">
              <div class="indicator-desc">
                <p><strong>定义：</strong>利用快慢速EMA差值判断趋势</p>
                <p><strong>用法：</strong></p>
                <ul>
                  <li>DIF上穿DEA（金叉）：买入信号</li>
                  <li>DIF下穿DEA（死叉）：卖出信号</li>
                  <li>MACD柱由负转正：多头市场</li>
                  <li>MACD柱由正转负：空头市场</li>
                  <li>背离：价格与MACD走势相反，可能反转</li>
                </ul>
                <p><strong>参数：</strong>快线12，慢线26，信号线9</p>
              </div>
            </el-collapse-item>

            <el-collapse-item title="KDJ - 随机指标" name="kdj">
              <div class="indicator-desc">
                <p><strong>定义：</strong>衡量价格超买超卖的摆动指标</p>
                <p><strong>用法：</strong></p>
                <ul>
                  <li>K值>80：超买区域，可能回调</li>
                  <li>K值<20：超卖区域，可能反弹</li>
                  <li>K线上穿D线：买入信号</li>
                  <li>K线下穿D线：卖出信号</li>
                  <li>J值>100或<0：极端超买/超卖</li>
                </ul>
                <p><strong>参数：</strong>周期9，平滑3</p>
              </div>
            </el-collapse-item>

            <el-collapse-item title="RSI - 相对强弱指标" name="rsi">
              <div class="indicator-desc">
                <p><strong>定义：</strong>测量价格涨跌强度的震荡指标</p>
                <p><strong>用法：</strong></p>
                <ul>
                  <li>RSI>70：超买，可能回调</li>
                  <li>RSI<30：超卖，可能反弹</li>
                  <li>RSI在50附近：多空平衡</li>
                  <li>背离：价格创新高/低但RSI未创新高/低</li>
                </ul>
                <p><strong>参数：</strong>RSI6、RSI12、RSI24</p>
              </div>
            </el-collapse-item>

            <el-collapse-item title="BOLL - 布林带" name="boll">
              <div class="indicator-desc">
                <p><strong>定义：</strong>利用统计学标准差确定价格波动区间</p>
                <p><strong>用法：</strong></p>
                <ul>
                  <li>价格触及上轨：可能回调</li>
                  <li>价格触及下轨：可能反弹</li>
                  <li>布林带收窄：盘整，可能突破</li>
                  <li>布林带扩张：趋势明确</li>
                  <li>中轨作为支撑/压力位</li>
                </ul>
                <p><strong>参数：</strong>周期20，标准差2倍</p>
              </div>
            </el-collapse-item>

            <el-collapse-item title="VOL - 成交量" name="vol">
              <div class="indicator-desc">
                <p><strong>定义：</strong>市场交易活跃度指标</p>
                <p><strong>用法：</strong></p>
                <ul>
                  <li>价涨量增：健康上涨</li>
                  <li>价涨量缩：动能不足，可能回调</li>
                  <li>价跌量增：抛压沉重</li>
                  <li>价跌量缩：下跌动能减弱，可能止跌</li>
                  <li>放量突破：有效突破</li>
                </ul>
                <p><strong>参数：</strong>VOL_MA5、VOL_MA10</p>
              </div>
            </el-collapse-item>
          </el-collapse>
        </el-card>
      </div>

      <!-- 空状态 -->
      <el-empty 
        v-if="!loading && !errorMsg && chartData.length === 0" 
        description="请输入股票代码并选择时间范围进行查询"
        style="margin-top: 40px"
      />
    </div>
  </PageShell>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Search } from '@element-plus/icons-vue'
import PageShell from '@/components/PageShell.vue'
import TechnicalChart from '@/components/TechnicalChart.vue'
import TechnicalSignals from '@/components/TechnicalSignals.vue'
import StockSearch from '@/components/business/StockSearch.vue'
import { getTechnicalIndicators, getTechnicalSignals } from '@/api/stock'

const queryForm = ref({
  code: '600000',
  indicators: 'MA,MACD,KDJ,RSI,BOLL,VOL'
})

const dateRange = ref<[string, string] | null>(null)
const loading = ref(false)
const errorMsg = ref('')
const chartData = ref<any[]>([])
const chartRef = ref<any>(null)
const selectedStockName = ref('')

// 信号检测相关
const signals = ref<any[]>([])
const tradingAdvice = ref<any>(null)
const signalsLoading = ref(false)

// 处理股票选择
const handleStockSelect = (stock: any) => {
  queryForm.value.code = stock.code
  selectedStockName.value = stock.name
}

// 日期快捷选项
const dateShortcuts = [
  {
    text: '最近一个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setMonth(start.getMonth() - 1)
      return [start, end]
    }
  },
  {
    text: '最近三个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setMonth(start.getMonth() - 3)
      return [start, end]
    }
  },
  {
    text: '最近半年',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setMonth(start.getMonth() - 6)
      return [start, end]
    }
  },
  {
    text: '最近一年',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setFullYear(start.getFullYear() - 1)
      return [start, end]
    }
  }
]

// 计算属性
const dataRange = computed(() => {
  if (chartData.value.length === 0) return '-'
  const first = chartData.value[0].日期
  const last = chartData.value[chartData.value.length - 1].日期
  return `${first} ~ ${last}`
})

const latestClose = computed(() => {
  if (chartData.value.length === 0) return '-'
  return chartData.value[chartData.value.length - 1].收盘.toFixed(2)
})

const latestPriceClass = computed(() => {
  if (chartData.value.length < 2) return ''
  const curr = chartData.value[chartData.value.length - 1].收盘
  const prev = chartData.value[chartData.value.length - 2].收盘
  return curr > prev ? 'price-up' : curr < prev ? 'price-down' : ''
})

const rangeChange = computed(() => {
  if (chartData.value.length === 0) return '-'
  const first = chartData.value[0].收盘
  const last = chartData.value[chartData.value.length - 1].收盘
  const change = ((last - first) / first * 100).toFixed(2)
  return `${change}%`
})

const rangeChangeClass = computed(() => {
  if (chartData.value.length === 0) return ''
  const first = chartData.value[0].收盘
  const last = chartData.value[chartData.value.length - 1].收盘
  return last > first ? 'price-up' : last < first ? 'price-down' : ''
})

async function loadData() {
  if (!queryForm.value.code) {
    errorMsg.value = '请输入股票代码'
    return
  }

  loading.value = true
  errorMsg.value = ''
  chartData.value = []

  try {
    const params: any = {
      code: queryForm.value.code,
      indicators: queryForm.value.indicators,
      source: 'eastmoney'
    }

    if (dateRange.value && dateRange.value.length === 2) {
      params.start_date = dateRange.value[0]
      params.end_date = dateRange.value[1]
    }

    const res: any = await getTechnicalIndicators(params)

    if (res.status === 'ok' && res.data) {
      chartData.value = res.data
      // 加载完技术指标后，自动检测信号
      await loadSignals()
    } else {
      errorMsg.value = res.message || '获取数据失败'
    }
  } catch (e: any) {
    errorMsg.value = e.response?.data?.detail || e.message || '网络错误'
    console.error('加载技术指标失败:', e)
  } finally {
    loading.value = false
  }
}

// 加载技术信号
async function loadSignals() {
  signalsLoading.value = true
  signals.value = []
  tradingAdvice.value = null

  try {
    const params: any = {
      code: queryForm.value.code,
      lookback: 10,  // 检测最近10天的信号
      source: 'eastmoney'
    }

    if (dateRange.value && dateRange.value.length === 2) {
      params.start_date = dateRange.value[0]
      params.end_date = dateRange.value[1]
    }

    const res: any = await getTechnicalSignals(params)

    if (res.status === 'ok') {
      signals.value = res.signals || []
      tradingAdvice.value = res.advice || null
    }
  } catch (e: any) {
    console.error('加载技术信号失败:', e)
    // 信号加载失败不影响主流程，只记录错误
  } finally {
    signalsLoading.value = false
  }
}

function resetForm() {
  queryForm.value.code = '600000'
  dateRange.value = null
  errorMsg.value = ''
  chartData.value = []
  signals.value = []
  tradingAdvice.value = null
}

// 初始化时设置默认时间范围为最近3个月
const initDateRange = () => {
  const end = new Date()
  const start = new Date()
  start.setMonth(start.getMonth() - 3)
  
  const fmt = (d: Date) => {
    const year = d.getFullYear()
    const month = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${year}${month}${day}`
  }
  
  dateRange.value = [fmt(start), fmt(end)]
}

// 组件挂载时初始化
initDateRange()
</script>

<style scoped>
.technical-analysis-container {
  padding: 20px;
}

.query-card {
  margin-bottom: 20px;
}

.chart-section {
  margin-top: 20px;
}

.stats-card {
  margin-top: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.price-up {
  color: #ef232a;
}

.price-down {
  color: #14b143;
}

.info-card {
  margin-top: 20px;
}

.card-header {
  font-size: 16px;
  font-weight: 600;
}

.indicator-desc {
  line-height: 1.8;
  color: #606266;
}

.indicator-desc p {
  margin: 8px 0;
}

.indicator-desc strong {
  color: #303133;
}

.indicator-desc ul {
  margin: 8px 0;
  padding-left: 24px;
}

.indicator-desc li {
  margin: 4px 0;
}
</style>
