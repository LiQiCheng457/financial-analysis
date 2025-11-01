<template>
  <div class="financial-metrics">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>加载中...</span>
    </div>

    <!-- 财务指标内容 -->
    <div v-else class="metrics-content">
      <!-- 估值指标 -->
      <el-card class="metrics-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><TrendCharts /></el-icon>
            <span>估值指标</span>
          </div>
        </template>
        <div class="metrics-grid">
          <div class="metric-item">
            <div class="metric-label">市盈率 (PE)</div>
            <div class="metric-value" :class="getPEClass(metrics.valuation.pe)">
              {{ metrics.valuation.pe }}
            </div>
            <div class="metric-desc">{{ getPEDesc(metrics.valuation.pe) }}</div>
          </div>
          <div class="metric-item">
            <div class="metric-label">市净率 (PB)</div>
            <div class="metric-value" :class="getPBClass(metrics.valuation.pb)">
              {{ metrics.valuation.pb }}
            </div>
            <div class="metric-desc">{{ getPBDesc(metrics.valuation.pb) }}</div>
          </div>
          <div class="metric-item">
            <div class="metric-label">市销率 (PS)</div>
            <div class="metric-value">{{ metrics.valuation.ps }}</div>
            <div class="metric-desc">衡量股价与销售收入的比率</div>
          </div>
          <div class="metric-item">
            <div class="metric-label">股息率 (%)</div>
            <div class="metric-value" :class="getDividendClass(metrics.valuation.dividendYield)">
              {{ metrics.valuation.dividendYield }}%
            </div>
            <div class="metric-desc">{{ getDividendDesc(metrics.valuation.dividendYield) }}</div>
          </div>
        </div>
      </el-card>

      <!-- 盈利能力 -->
      <el-card class="metrics-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Odometer /></el-icon>
            <span>盈利能力</span>
          </div>
        </template>
        <div class="metrics-grid">
          <div class="metric-item">
            <div class="metric-label">净资产收益率 (ROE)</div>
            <div class="metric-value" :class="getROEClass(metrics.profitability.roe)">
              {{ metrics.profitability.roe }}%
            </div>
            <div class="metric-desc">{{ getROEDesc(metrics.profitability.roe) }}</div>
          </div>
          <div class="metric-item">
            <div class="metric-label">总资产收益率 (ROA)</div>
            <div class="metric-value">{{ metrics.profitability.roa }}%</div>
            <div class="metric-desc">资产利用效率指标</div>
          </div>
          <div class="metric-item">
            <div class="metric-label">毛利率 (%)</div>
            <div class="metric-value">{{ metrics.profitability.grossMargin }}%</div>
            <div class="metric-desc">毛利占营业收入比例</div>
          </div>
          <div class="metric-item">
            <div class="metric-label">净利率 (%)</div>
            <div class="metric-value" :class="getNetMarginClass(metrics.profitability.netMargin)">
              {{ metrics.profitability.netMargin }}%
            </div>
            <div class="metric-desc">{{ getNetMarginDesc(metrics.profitability.netMargin) }}</div>
          </div>
        </div>
      </el-card>

      <!-- 营收与利润趋势图 -->
      <el-card class="chart-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><DataLine /></el-icon>
            <span>营收与利润趋势（近4年）</span>
          </div>
        </template>
        <div ref="revenueChartRef" class="chart-container"></div>
      </el-card>

      <!-- 财务健康度 -->
      <el-card class="metrics-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><CircleCheck /></el-icon>
            <span>财务健康度</span>
          </div>
        </template>
        <div class="metrics-grid">
          <div class="metric-item">
            <div class="metric-label">资产负债率 (%)</div>
            <div class="metric-value" :class="getDebtRatioClass(metrics.financial.debtRatio)">
              {{ metrics.financial.debtRatio }}%
            </div>
            <div class="metric-desc">{{ getDebtRatioDesc(metrics.financial.debtRatio) }}</div>
          </div>
          <div class="metric-item">
            <div class="metric-label">流动比率</div>
            <div class="metric-value" :class="getCurrentRatioClass(metrics.financial.currentRatio)">
              {{ metrics.financial.currentRatio }}
            </div>
            <div class="metric-desc">{{ getCurrentRatioDesc(metrics.financial.currentRatio) }}</div>
          </div>
          <div class="metric-item">
            <div class="metric-label">速动比率</div>
            <div class="metric-value">{{ metrics.financial.quickRatio }}</div>
            <div class="metric-desc">短期偿债能力指标</div>
          </div>
          <div class="metric-item">
            <div class="metric-label">现金流健康度</div>
            <div class="metric-value good">
              <el-icon><SuccessFilled /></el-icon>
              健康
            </div>
            <div class="metric-desc">经营现金流为正</div>
          </div>
        </div>
      </el-card>

      <!-- ROE趋势图 -->
      <el-card class="chart-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><TrendCharts /></el-icon>
            <span>ROE趋势（近4年）</span>
          </div>
        </template>
        <div ref="roeChartRef" class="chart-container"></div>
      </el-card>

      <!-- 综合评分 -->
      <el-card class="score-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Trophy /></el-icon>
            <span>财务综合评分</span>
          </div>
        </template>
        <div class="score-content">
          <div class="score-main">
            <div class="score-number" :class="getScoreClass(comprehensiveScore)">
              {{ comprehensiveScore }}
            </div>
            <div class="score-label">分</div>
          </div>
          <div class="score-bar">
            <el-progress 
              :percentage="comprehensiveScore" 
              :color="getScoreColor(comprehensiveScore)"
              :stroke-width="20"
            />
          </div>
          <div class="score-desc">
            <div class="score-rating" :class="getScoreClass(comprehensiveScore)">
              {{ getScoreRating(comprehensiveScore) }}
            </div>
            <div class="score-detail">
              基于估值、盈利能力、财务健康度的综合评估
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'
import {
  Loading,
  TrendCharts,
  Odometer,
  DataLine,
  CircleCheck,
  SuccessFilled,
  Trophy
} from '@element-plus/icons-vue'

interface Props {
  stockCode?: string
  stockName?: string
}

const props = withDefaults(defineProps<Props>(), {
  stockCode: '600000',
  stockName: '浦发银行'
})

// reference props to avoid unused variable lint in some toolchains
void props

const loading = ref(false)
const revenueChartRef = ref<HTMLElement>()
const roeChartRef = ref<HTMLElement>()

// 模拟财务数据
const metrics = ref({
  valuation: {
    pe: 5.23,
    pb: 0.48,
    ps: 0.92,
    dividendYield: 5.67
  },
  profitability: {
    roe: 8.45,
    roa: 0.68,
    grossMargin: 48.32,
    netMargin: 21.56
  },
  financial: {
    debtRatio: 92.34,
    currentRatio: 1.15,
    quickRatio: 1.12
  }
})

// 综合评分（基于各项指标）
const comprehensiveScore = ref(72)

// 营收与利润趋势数据
const revenueData = [
  { year: '2021', revenue: 1823.45, profit: 589.34 },
  { year: '2022', revenue: 1956.78, profit: 623.12 },
  { year: '2023', revenue: 2045.23, profit: 658.45 },
  { year: '2024', revenue: 2134.56, profit: 685.23 }
]

// ROE趋势数据
const roeData = [
  { year: '2021', roe: 9.23 },
  { year: '2022', roe: 8.95 },
  { year: '2023', roe: 8.67 },
  { year: '2024', roe: 8.45 }
]

// PE评价
const getPEClass = (pe: number) => {
  if (pe < 0) return 'negative'
  if (pe < 15) return 'good'
  if (pe < 25) return 'normal'
  return 'warning'
}

const getPEDesc = (pe: number) => {
  if (pe < 0) return '公司亏损'
  if (pe < 15) return '估值较低，可能被低估'
  if (pe < 25) return '估值合理'
  return '估值较高，需谨慎'
}

// PB评价
const getPBClass = (pb: number) => {
  if (pb < 1) return 'good'
  if (pb < 3) return 'normal'
  return 'warning'
}

const getPBDesc = (pb: number) => {
  if (pb < 1) return '股价低于净资产'
  if (pb < 3) return '估值合理'
  return '估值偏高'
}

// 股息率评价
const getDividendClass = (dividend: number) => {
  if (dividend >= 4) return 'good'
  if (dividend >= 2) return 'normal'
  return 'warning'
}

const getDividendDesc = (dividend: number) => {
  if (dividend >= 4) return '高股息，适合价值投资'
  if (dividend >= 2) return '股息适中'
  return '股息较低'
}

// ROE评价
const getROEClass = (roe: number) => {
  if (roe >= 15) return 'good'
  if (roe >= 10) return 'normal'
  return 'warning'
}

const getROEDesc = (roe: number) => {
  if (roe >= 15) return '盈利能力优秀'
  if (roe >= 10) return '盈利能力良好'
  return '盈利能力一般'
}

// 净利率评价
const getNetMarginClass = (margin: number) => {
  if (margin >= 20) return 'good'
  if (margin >= 10) return 'normal'
  return 'warning'
}

const getNetMarginDesc = (margin: number) => {
  if (margin >= 20) return '利润率较高'
  if (margin >= 10) return '利润率正常'
  return '利润率偏低'
}

// 资产负债率评价
const getDebtRatioClass = (ratio: number) => {
  if (ratio < 40) return 'good'
  if (ratio < 70) return 'normal'
  return 'warning'
}

const getDebtRatioDesc = (ratio: number) => {
  if (ratio < 40) return '负债水平低，财务稳健'
  if (ratio < 70) return '负债水平适中'
  return '负债较高（金融行业正常）'
}

// 流动比率评价
const getCurrentRatioClass = (ratio: number) => {
  if (ratio >= 2) return 'good'
  if (ratio >= 1) return 'normal'
  return 'warning'
}

const getCurrentRatioDesc = (ratio: number) => {
  if (ratio >= 2) return '短期偿债能力强'
  if (ratio >= 1) return '短期偿债能力正常'
  return '短期偿债能力不足'
}

// 综合评分评价
const getScoreClass = (score: number) => {
  if (score >= 80) return 'excellent'
  if (score >= 60) return 'good'
  if (score >= 40) return 'normal'
  return 'warning'
}

const getScoreRating = (score: number) => {
  if (score >= 80) return '优秀'
  if (score >= 60) return '良好'
  if (score >= 40) return '一般'
  return '较差'
}

const getScoreColor = (score: number) => {
  if (score >= 80) return '#67c23a'
  if (score >= 60) return '#409eff'
  if (score >= 40) return '#e6a23c'
  return '#f56c6c'
}

// 初始化营收利润趋势图
let _revResize: ResizeObserver | null = null
let _roeResize: ResizeObserver | null = null

const initRevenueChart = () => {
  if (!revenueChartRef.value) return
  const el = revenueChartRef.value
  const tryInit = () => {
    const w = (el as HTMLElement).clientWidth
    const h = (el as HTMLElement).clientHeight
    if (!w || !h) return false
    const chart = echarts.init(el)
    const option: EChartsOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['营业收入', '净利润'],
      top: 0
    },
    grid: {
      left: 60,
      right: 60,
      top: 40,
      bottom: 30
    },
    xAxis: {
      type: 'category',
      data: revenueData.map(d => d.year),
      axisLine: {
        lineStyle: { color: '#ddd' }
      }
    },
    yAxis: {
      type: 'value',
      name: '金额（亿元）',
      axisLine: {
        lineStyle: { color: '#ddd' }
      },
      splitLine: {
        lineStyle: { color: '#f0f0f0' }
      }
    },
    series: [
      {
        name: '营业收入',
        type: 'bar',
        data: revenueData.map(d => d.revenue),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#409eff' },
            { offset: 1, color: '#79bbff' }
          ])
        },
        barWidth: '30%'
      },
      {
        name: '净利润',
        type: 'line',
        data: revenueData.map(d => d.profit),
        itemStyle: { color: '#67c23a' },
        lineStyle: { width: 3 },
        smooth: true,
        symbol: 'circle',
        symbolSize: 8
      }
    ]
  }

    chart.setOption(option)

    // 响应式
    const resizeObserver = new ResizeObserver(() => {
      chart.resize()
    })
    resizeObserver.observe(el)
    _revResize = resizeObserver
    return true
  }

  // try immediate init; otherwise observe
  if (!tryInit()) {
    _revResize = new ResizeObserver(() => {
      if (tryInit() && _revResize) {
        _revResize.disconnect()
        _revResize = null
      }
    })
    _revResize.observe(el)
  }
}

// 初始化ROE趋势图
const initROEChart = () => {
  if (!roeChartRef.value) return
  const el = roeChartRef.value
  const tryInit = () => {
    const w = (el as HTMLElement).clientWidth
    const h = (el as HTMLElement).clientHeight
    if (!w || !h) return false
    const chart = echarts.init(el)
    const option: EChartsOption = {
    tooltip: {
      trigger: 'axis',
      formatter: '{b}: {c}%'
    },
    grid: {
      left: 60,
      right: 60,
      top: 30,
      bottom: 30
    },
    xAxis: {
      type: 'category',
      data: roeData.map(d => d.year),
      axisLine: {
        lineStyle: { color: '#ddd' }
      }
    },
    yAxis: {
      type: 'value',
      name: 'ROE (%)',
      axisLine: {
        lineStyle: { color: '#ddd' }
      },
      splitLine: {
        lineStyle: { color: '#f0f0f0' }
      }
    },
    series: [
      {
        type: 'line',
        data: roeData.map(d => d.roe),
        itemStyle: { color: '#e6a23c' },
        lineStyle: { width: 3 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(230, 162, 60, 0.3)' },
            { offset: 1, color: 'rgba(230, 162, 60, 0.05)' }
          ])
        },
        smooth: true,
        symbol: 'circle',
        symbolSize: 10
      }
    ]
  }

    chart.setOption(option)

    // 响应式
    const resizeObserver = new ResizeObserver(() => {
      chart.resize()
    })
    resizeObserver.observe(el)
    _roeResize = resizeObserver
    return true
  }

  if (!tryInit()) {
    _roeResize = new ResizeObserver(() => {
      if (tryInit() && _roeResize) {
        _roeResize.disconnect()
        _roeResize = null
      }
    })
    _roeResize.observe(el)
  }
}

onMounted(async () => {
  loading.value = true
  
  // 模拟加载延迟
  await new Promise(resolve => setTimeout(resolve, 500))
  
  loading.value = false

  // 等待DOM渲染完成后初始化图表
  await nextTick()
  initRevenueChart()
  initROEChart()
})

onBeforeUnmount(() => {
  try { if (_revResize) { _revResize.disconnect(); _revResize = null } } catch(e) {}
  try { if (_roeResize) { _roeResize.disconnect(); _roeResize = null } } catch(e) {}
})
</script>

<style scoped lang="scss">
.financial-metrics {
  padding: 20px;
  background: #f5f7fa;
  min-height: calc(100vh - 200px);

  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 100px 0;
    gap: 16px;

    .el-icon {
      font-size: 48px;
      color: #409eff;
    }

    span {
      font-size: 16px;
      color: #909399;
    }
  }

  .metrics-content {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;

    .metrics-card,
    .chart-card,
    .score-card {
      :deep(.el-card__header) {
        padding: 16px 20px;
        border-bottom: 2px solid #f0f0f0;
      }

      :deep(.el-card__body) {
        padding: 24px;
      }
    }

    .card-header {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 16px;
      font-weight: 600;
      color: #303133;

      .el-icon {
        font-size: 20px;
        color: #409eff;
      }
    }

    .metrics-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 24px;

      .metric-item {
        text-align: center;

        .metric-label {
          font-size: 14px;
          color: #909399;
          margin-bottom: 12px;
        }

        .metric-value {
          font-size: 28px;
          font-weight: 700;
          margin-bottom: 8px;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 6px;

          &.good {
            color: #67c23a;
          }

          &.normal {
            color: #409eff;
          }

          &.warning {
            color: #e6a23c;
          }

          &.negative {
            color: #f56c6c;
          }

          .el-icon {
            font-size: 24px;
          }
        }

        .metric-desc {
          font-size: 12px;
          color: #c0c4cc;
          line-height: 1.5;
        }
      }
    }

    .chart-card {
      .chart-container {
        width: 100%;
        height: 300px;
      }
    }

    .score-card {
      grid-column: span 2;

      .score-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 24px;
        padding: 20px 0;

        .score-main {
          display: flex;
          align-items: baseline;
          gap: 8px;

          .score-number {
            font-size: 72px;
            font-weight: 700;

            &.excellent {
              color: #67c23a;
            }

            &.good {
              color: #409eff;
            }

            &.normal {
              color: #e6a23c;
            }

            &.warning {
              color: #f56c6c;
            }
          }

          .score-label {
            font-size: 24px;
            color: #909399;
          }
        }

        .score-bar {
          width: 100%;
          max-width: 600px;
        }

        .score-desc {
          text-align: center;

          .score-rating {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 8px;

            &.excellent {
              color: #67c23a;
            }

            &.good {
              color: #409eff;
            }

            &.normal {
              color: #e6a23c;
            }

            &.warning {
              color: #f56c6c;
            }
          }

          .score-detail {
            font-size: 14px;
            color: #909399;
          }
        }
      }
    }
  }

  @media (max-width: 1400px) {
    .metrics-content {
      grid-template-columns: 1fr;
    }
  }
}
</style>
