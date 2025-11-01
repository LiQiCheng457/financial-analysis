<template>
  <PageShell>
    <template #title>🏆 行业轮动策略</template>
    <template #subtitle>基于双向LSTM+注意力机制的AI量化交易策略</template>
    <template #actions>
      <el-button type="primary" :icon="Refresh" @click="refreshData">刷新数据</el-button>
      <el-button :icon="Download">导出报告</el-button>
    </template>

    <div class="strategy-container">
      <!-- 策略概览卡片 -->
      <el-card class="overview-card" shadow="never">
        <div class="overview-header">
          <div class="period-info">
            <el-icon><Calendar /></el-icon>
            <span>回测期间：{{ backTestPeriod }}</span>
          </div>
          <div class="status-badge">
            <el-tag type="success" effect="dark" size="large">
              <el-icon><Trophy /></el-icon>
              策略运行中
            </el-tag>
          </div>
        </div>
      </el-card>

      <!-- 核心绩效指标 -->
      <StrategyMetrics :metrics="performanceMetrics" :loading="loading" />

      <!-- 策略亮点提示 -->
      <el-alert
        class="highlight-alert"
        type="success"
        :closable="false"
        show-icon
      >
        <template #title>
          <strong>💡 策略亮点</strong>
        </template>
        <ul class="highlight-list">
          <li>年化收益 <strong>{{ performanceMetrics.annualReturn }}%</strong> 显著超越市场平均水平（沪深300约5-6%）</li>
          <li>夏普比率 <strong>{{ performanceMetrics.sharpeRatio }}</strong> 达到优秀量化策略标准（>1.5）</li>
          <li>AI模型方向准确率 <strong>{{ modelInfo.directionAccuracy }}%</strong>，Top 20%预测准确率高达 <strong>{{ modelInfo.top20Accuracy }}%</strong></li>
        </ul>
      </el-alert>

      <!-- 累计收益曲线 -->
      <el-card class="chart-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>📈 累计收益曲线</span>
            <el-radio-group v-model="returnChartType" size="small">
              <el-radio-button value="cumulative">累计收益</el-radio-button>
              <el-radio-button value="daily">日收益率</el-radio-button>
            </el-radio-group>
          </div>
        </template>
        <div ref="returnChartRef" class="chart-container"></div>
      </el-card>

      <!-- 回撤分析 -->
      <el-card class="chart-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>📉 回撤分析</span>
            <el-tag type="danger" size="small">最大回撤：{{ performanceMetrics.maxDrawdown }}%</el-tag>
          </div>
        </template>
        <div ref="drawdownChartRef" class="chart-container"></div>
      </el-card>

      <!-- 当前推荐行业 -->
      <el-card class="recommendation-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <span>🎯 当前推荐行业配置</span>
            <el-text type="info" size="small">基于最新AI预测</el-text>
          </div>
        </template>
        <div class="industry-recommendations">
          <div 
            v-for="industry in currentRecommendations" 
            :key="industry.name"
            class="industry-item"
            :class="getRecommendationClass(industry.score)"
          >
            <div class="industry-icon">{{ industry.icon }}</div>
            <div class="industry-info">
              <div class="industry-name">{{ industry.name }}</div>
              <div class="industry-score">
                <el-progress 
                  :percentage="industry.score" 
                  :color="getScoreColor(industry.score)"
                  :stroke-width="8"
                />
              </div>
            </div>
            <div class="industry-action">
              <el-tag 
                :type="getActionType(industry.score)" 
                effect="dark"
                size="large"
              >
                {{ getActionText(industry.score) }}
              </el-tag>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 行业配置与轮动分析 -->
      <el-row :gutter="20">
        <el-col :xs="24" :lg="12">
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <span>🔄 行业配置分析</span>
            </template>
            <div ref="allocationChartRef" class="chart-container" style="height: 350px"></div>
          </el-card>
        </el-col>
        <el-col :xs="24" :lg="12">
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <span>📅 月度收益分析</span>
            </template>
            <div ref="monthlyChartRef" class="chart-container" style="height: 350px"></div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 行业轮动热力图 -->
      <el-card class="chart-card" shadow="hover">
        <template #header>
          <span>🔥 行业轮动热力图（2023-2024）</span>
        </template>
        <div ref="heatmapChartRef" class="chart-container" style="height: 400px"></div>
      </el-card>

      <!-- 模型信息 -->
      <el-card class="info-card" shadow="hover">
        <template #header>
          <span>🤖 模型信息</span>
        </template>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="模型架构">
            {{ modelInfo.architecture }}
          </el-descriptions-item>
          <el-descriptions-item label="模型参数量">
            {{ formatNumber(modelInfo.parameters) }}
          </el-descriptions-item>
          <el-descriptions-item label="方向准确率">
            <el-tag type="success">{{ modelInfo.directionAccuracy }}%</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="Top 20%准确率">
            <el-tag type="success">{{ modelInfo.top20Accuracy }}%</el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="训练数据量">
            {{ formatNumber(modelInfo.trainingSamples) }} 样本
          </el-descriptions-item>
          <el-descriptions-item label="特征维度">
            {{ modelInfo.features }} 个技术指标
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
    </div>
  </PageShell>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import type { EChartsOption } from 'echarts'
import PageShell from '@/components/PageShell.vue'
import StrategyMetrics from '@/components/strategy/StrategyMetrics.vue'
import { 
  Refresh, 
  Download, 
  Calendar, 
  Trophy 
} from '@element-plus/icons-vue'

const loading = ref(false)
const returnChartType = ref('cumulative')

// 回测周期
const backTestPeriod = ref('2023-01-01 至 2024-12-31')

// 绩效指标（模拟数据）
const performanceMetrics = ref({
  totalReturn: 27.05,
  annualReturn: 13.13,
  sharpeRatio: 1.53,
  maxDrawdown: -22.71,
  tradingDays: 95,
  totalTrades: 285
})

// 模型信息
const modelInfo = ref({
  architecture: '双向LSTM + 注意力机制',
  directionAccuracy: 67.87,
  top20Accuracy: 79.98,
  parameters: 3992706,
  trainingSamples: 865477,
  features: 50
})

// 当前推荐行业
const currentRecommendations = ref([
  { name: '银行', icon: '🏦', score: 95.2 },
  { name: '科技', icon: '💻', score: 88.6 },
  { name: '医药', icon: '💊', score: 82.3 },
  { name: '能源', icon: '⚡', score: 75.4 },
  { name: '制造', icon: '🏭', score: 68.9 },
  { name: '消费', icon: '🛒', score: 62.1 },
  { name: '房地产', icon: '🏢', score: 55.8 },
  { name: '金融', icon: '💰', score: 48.3 }
])

const returnChartRef = ref<HTMLElement>()
const drawdownChartRef = ref<HTMLElement>()
const allocationChartRef = ref<HTMLElement>()
const monthlyChartRef = ref<HTMLElement>()
const heatmapChartRef = ref<HTMLElement>()

// 格式化数字
const formatNumber = (num: number) => {
  return num.toLocaleString('zh-CN')
}

// 获取推荐等级样式
const getRecommendationClass = (score: number) => {
  if (score >= 85) return 'strong-buy'
  if (score >= 70) return 'buy'
  if (score >= 50) return 'hold'
  return 'sell'
}

// 获取分数颜色
const getScoreColor = (score: number) => {
  if (score >= 85) return '#67c23a'
  if (score >= 70) return '#409eff'
  if (score >= 50) return '#e6a23c'
  return '#f56c6c'
}

// 获取操作类型
const getActionType = (score: number) => {
  if (score >= 85) return 'success'
  if (score >= 70) return 'primary'
  if (score >= 50) return 'warning'
  return 'danger'
}

// 获取操作文字
const getActionText = (score: number) => {
  if (score >= 85) return '🟢 强烈推荐'
  if (score >= 70) return '🟢 推荐'
  if (score >= 50) return '🟡 持有'
  return '🔴 规避'
}

// 累计收益曲线数据（模拟）
const generateReturnData = () => {
  const dates: string[] = []
  const strategyReturns: number[] = []
  const benchmarkReturns: number[] = []
  
  let strategyValue = 100000
  let benchmarkValue = 100000
  
  const startDate = new Date('2023-01-01')
  
  for (let i = 0; i < 95; i++) {
    const date = new Date(startDate)
    date.setDate(date.getDate() + i * 2) // 每2天一个数据点
    dates.push(date.toISOString().split('T')[0])
    
    // 策略收益波动
    const strategyChange = (Math.random() - 0.45) * 0.02 // 略微偏正
    strategyValue *= (1 + strategyChange)
    strategyReturns.push(((strategyValue - 100000) / 100000) * 100)
    
    // 基准收益波动
    const benchmarkChange = (Math.random() - 0.48) * 0.015
    benchmarkValue *= (1 + benchmarkChange)
    benchmarkReturns.push(((benchmarkValue - 100000) / 100000) * 100)
  }
  
  return { dates, strategyReturns, benchmarkReturns }
}

// 初始化收益曲线图
const initReturnChart = () => {
  if (!returnChartRef.value) return
  
  const chart = echarts.init(returnChartRef.value)
  const { dates, strategyReturns, benchmarkReturns } = generateReturnData()
  
  const option: EChartsOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['策略收益', '沪深300基准'],
      top: 10
    },
    grid: {
      left: 60,
      right: 60,
      top: 60,
      bottom: 40
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: {
        lineStyle: { color: '#ddd' }
      }
    },
    yAxis: {
      type: 'value',
      name: '累计收益率 (%)',
      axisLine: {
        lineStyle: { color: '#ddd' }
      },
      splitLine: {
        lineStyle: { color: '#f0f0f0' }
      }
    },
    series: [
      {
        name: '策略收益',
        type: 'line',
        data: strategyReturns,
        itemStyle: { color: '#67c23a' },
        lineStyle: { width: 3 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(103, 194, 58, 0.3)' },
            { offset: 1, color: 'rgba(103, 194, 58, 0.05)' }
          ])
        },
        smooth: true
      },
      {
        name: '沪深300基准',
        type: 'line',
        data: benchmarkReturns,
        itemStyle: { color: '#909399' },
        lineStyle: { width: 2, type: 'dashed' },
        smooth: true
      }
    ]
  }
  
  chart.setOption(option)
  
  const resizeObserver = new ResizeObserver(() => chart.resize())
  resizeObserver.observe(returnChartRef.value)
}

// 初始化回撤图
const initDrawdownChart = () => {
  if (!drawdownChartRef.value) return
  
  const chart = echarts.init(drawdownChartRef.value)
  const { dates } = generateReturnData()
  
  // 生成回撤数据
  const drawdowns = dates.map(() => Math.random() * -25)
  
  const option: EChartsOption = {
    tooltip: {
      trigger: 'axis',
      formatter: '{b}: {c}%'
    },
    grid: {
      left: 60,
      right: 60,
      top: 40,
      bottom: 40
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: '#ddd' } }
    },
    yAxis: {
      type: 'value',
      name: '回撤 (%)',
      axisLine: { lineStyle: { color: '#ddd' } },
      splitLine: { lineStyle: { color: '#f0f0f0' } }
    },
    series: [{
      type: 'line',
      data: drawdowns,
      itemStyle: { color: '#f56c6c' },
      lineStyle: { width: 2 },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(245, 108, 108, 0.3)' },
          { offset: 1, color: 'rgba(245, 108, 108, 0.05)' }
        ])
      },
      smooth: true
    }]
  }
  
  chart.setOption(option)
  
  const resizeObserver = new ResizeObserver(() => chart.resize())
  resizeObserver.observe(drawdownChartRef.value)
}

// 初始化行业配置饼图
const initAllocationChart = () => {
  if (!allocationChartRef.value) return
  
  const chart = echarts.init(allocationChartRef.value)
  
  const option: EChartsOption = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}% ({d}%)'
    },
    legend: {
      orient: 'vertical',
      right: 10,
      top: 'center'
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 16,
          fontWeight: 'bold'
        }
      },
      data: [
        { value: 25, name: '银行', itemStyle: { color: '#5470c6' } },
        { value: 20, name: '科技', itemStyle: { color: '#91cc75' } },
        { value: 18, name: '医药', itemStyle: { color: '#fac858' } },
        { value: 15, name: '能源', itemStyle: { color: '#ee6666' } },
        { value: 12, name: '制造', itemStyle: { color: '#73c0de' } },
        { value: 10, name: '其他', itemStyle: { color: '#9a60b4' } }
      ]
    }]
  }
  
  chart.setOption(option)
  
  const resizeObserver = new ResizeObserver(() => chart.resize())
  resizeObserver.observe(allocationChartRef.value)
}

// 初始化月度收益柱状图
const initMonthlyChart = () => {
  if (!monthlyChartRef.value) return
  
  const chart = echarts.init(monthlyChartRef.value)
  
  const months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
  const returns = months.map(() => (Math.random() - 0.4) * 10)
  
  const option: EChartsOption = {
    tooltip: {
      trigger: 'axis',
      formatter: '{b}: {c}%'
    },
    grid: {
      left: 50,
      right: 30,
      top: 30,
      bottom: 40
    },
    xAxis: {
      type: 'category',
      data: months,
      axisLine: { lineStyle: { color: '#ddd' } }
    },
    yAxis: {
      type: 'value',
      name: '收益率 (%)',
      axisLine: { lineStyle: { color: '#ddd' } },
      splitLine: { lineStyle: { color: '#f0f0f0' } }
    },
    series: [{
      type: 'bar',
      data: returns.map(val => ({
        value: val,
        itemStyle: {
          color: val >= 0 ? '#67c23a' : '#f56c6c'
        }
      })),
      barWidth: '60%'
    }]
  }
  
  chart.setOption(option)
  
  const resizeObserver = new ResizeObserver(() => chart.resize())
  resizeObserver.observe(monthlyChartRef.value)
}

// 初始化热力图
const initHeatmapChart = () => {
  if (!heatmapChartRef.value) return
  
  const chart = echarts.init(heatmapChartRef.value)
  
  const industries = ['银行', '科技', '医药', '能源', '制造', '消费', '房地产', '金融']
  const months = ['23/1', '23/2', '23/3', '23/4', '23/5', '23/6', '23/7', '23/8', '23/9', '23/10', '23/11', '23/12',
                  '24/1', '24/2', '24/3', '24/4', '24/5', '24/6', '24/7', '24/8', '24/9', '24/10', '24/11', '24/12']
  
  const data = industries.flatMap((industry, i) =>
    months.map((month, j) => [j, i, (Math.random() - 0.4) * 15])
  )
  
  const option: EChartsOption = {
    tooltip: {
      position: 'top',
      formatter: (params: any) => {
        return `${months[params.data[0]]}<br/>${industries[params.data[1]]}: ${params.data[2].toFixed(2)}%`
      }
    },
    grid: {
      left: 80,
      right: 40,
      top: 40,
      bottom: 80
    },
    xAxis: {
      type: 'category',
      data: months,
      splitArea: { show: true },
      axisLabel: { rotate: 45 }
    },
    yAxis: {
      type: 'category',
      data: industries,
      splitArea: { show: true }
    },
    visualMap: {
      min: -10,
      max: 10,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 10,
      inRange: {
        color: ['#313695', '#4575b4', '#74add1', '#abd9e9', '#e0f3f8', '#ffffbf', '#fee090', '#fdae61', '#f46d43', '#d73027', '#a50026']
      }
    },
    series: [{
      type: 'heatmap',
      data: data,
      label: {
        show: false
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  }
  
  chart.setOption(option)
  
  const resizeObserver = new ResizeObserver(() => chart.resize())
  resizeObserver.observe(heatmapChartRef.value)
}

// 刷新数据
const refreshData = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    ElMessage.success('数据已更新')
  }, 1000)
}

onMounted(async () => {
  loading.value = true
  await new Promise(resolve => setTimeout(resolve, 500))
  loading.value = false
  
  await nextTick()
  initReturnChart()
  initDrawdownChart()
  initAllocationChart()
  initMonthlyChart()
  initHeatmapChart()
})
</script>

<style scoped lang="scss">
.strategy-container {
  padding: 20px;
  background: #f5f7fa;
  min-height: calc(100vh - 200px);

  .overview-card {
    margin-bottom: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;

    :deep(.el-card__body) {
      padding: 20px;
    }

    .overview-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .period-info {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 16px;

        .el-icon {
          font-size: 20px;
        }
      }

      .status-badge {
        .el-tag {
          font-size: 14px;
          padding: 8px 16px;
        }
      }
    }
  }

  .highlight-alert {
    margin: 20px 0;

    :deep(.el-alert__content) {
      .highlight-list {
        margin: 10px 0 0 0;
        padding-left: 20px;
        line-height: 2;

        li {
          margin: 8px 0;
        }

        strong {
          color: #67c23a;
          font-size: 16px;
        }
      }
    }
  }

  .chart-card {
    margin-bottom: 20px;

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 16px;
      font-weight: 600;
      color: #303133;
    }

    .chart-container {
      width: 100%;
      height: 400px;
    }
  }

  .recommendation-card {
    margin-bottom: 20px;

    .industry-recommendations {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 16px;

      .industry-item {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 16px;
        border-radius: 8px;
        border: 2px solid transparent;
        transition: all 0.3s;

        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        &.strong-buy {
          background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
          border-color: #67c23a;
        }

        &.buy {
          background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
          border-color: #409eff;
        }

        &.hold {
          background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
          border-color: #e6a23c;
        }

        &.sell {
          background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
          border-color: #f56c6c;
        }

        .industry-icon {
          font-size: 48px;
        }

        .industry-info {
          flex: 1;

          .industry-name {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 8px;
          }

          .industry-score {
            :deep(.el-progress__text) {
              display: none;
            }
          }
        }

        .industry-action {
          .el-tag {
            font-size: 14px;
            padding: 8px 12px;
            white-space: nowrap;
          }
        }
      }
    }
  }

  .info-card {
    :deep(.el-descriptions__label) {
      font-weight: 600;
    }
  }
}

@media (max-width: 768px) {
  .strategy-container {
    padding: 10px;

    .overview-card .overview-header {
      flex-direction: column;
      gap: 12px;
    }

    .chart-container {
      height: 300px !important;
    }

    .industry-recommendations {
      grid-template-columns: 1fr !important;
    }
  }
}
</style>
