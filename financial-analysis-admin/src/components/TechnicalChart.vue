<template>
  <div class="technical-chart-wrapper">
    <!-- 指标选择器 -->
    <div class="indicator-selector">
      <el-checkbox-group v-model="selectedIndicators" @change="handleIndicatorChange">
        <el-checkbox label="MA" border>均线(MA)</el-checkbox>
        <el-checkbox label="MACD" border>MACD</el-checkbox>
        <el-checkbox label="KDJ" border>KDJ</el-checkbox>
        <el-checkbox label="RSI" border>RSI</el-checkbox>
        <el-checkbox label="BOLL" border>布林带</el-checkbox>
        <el-checkbox label="VOL" border>成交量</el-checkbox>
      </el-checkbox-group>
    </div>

    <!-- 主图 - K线和均线 -->
    <div class="main-chart" ref="mainChartRef" style="width:100%;height:400px"></div>

    <!-- 副图 - MACD -->
    <div v-if="selectedIndicators.includes('MACD')" class="sub-chart" ref="macdChartRef" style="width:100%;height:150px;margin-top:10px"></div>

    <!-- 副图 - KDJ -->
    <div v-if="selectedIndicators.includes('KDJ')" class="sub-chart" ref="kdjChartRef" style="width:100%;height:150px;margin-top:10px"></div>

    <!-- 副图 - RSI -->
    <div v-if="selectedIndicators.includes('RSI')" class="sub-chart" ref="rsiChartRef" style="width:100%;height:150px;margin-top:10px"></div>

    <!-- 副图 - VOL -->
    <div v-if="selectedIndicators.includes('VOL')" class="sub-chart" ref="volChartRef" style="width:100%;height:150px;margin-top:10px"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import * as echarts from 'echarts'

interface TechnicalData {
  日期: string
  开盘: number
  最高: number
  最低: number
  收盘: number
  成交量: number
  MA5?: number
  MA10?: number
  MA20?: number
  MA60?: number
  DIF?: number
  DEA?: number
  MACD?: number
  K?: number
  D?: number
  J?: number
  RSI6?: number
  RSI12?: number
  RSI24?: number
  BOLL_UPPER?: number
  BOLL_MIDDLE?: number
  BOLL_LOWER?: number
  VOL_MA5?: number
  VOL_MA10?: number
  [k: string]: any
}

const props = defineProps<{
  data: TechnicalData[]
  defaultIndicators?: string[]
}>()

const selectedIndicators = ref<string[]>(props.defaultIndicators || ['MA', 'VOL'])
const mainChartRef = ref<HTMLDivElement | null>(null)
const macdChartRef = ref<HTMLDivElement | null>(null)
const kdjChartRef = ref<HTMLDivElement | null>(null)
const rsiChartRef = ref<HTMLDivElement | null>(null)
const volChartRef = ref<HTMLDivElement | null>(null)

let mainChart: echarts.ECharts | null = null
let macdChart: echarts.ECharts | null = null
let kdjChart: echarts.ECharts | null = null
let rsiChart: echarts.ECharts | null = null
let volChart: echarts.ECharts | null = null

function initCharts() {
  if (!props.data || props.data.length === 0) {
    console.warn('TechnicalChart: 没有数据可以绘制')
    return
  }

  // 初始化主图
  if (mainChartRef.value) {
    mainChart = echarts.init(mainChartRef.value)
    renderMainChart()
  }

  // 初始化副图
  nextTick(() => {
    if (selectedIndicators.value.includes('MACD') && macdChartRef.value) {
      macdChart = echarts.init(macdChartRef.value)
      renderMACDChart()
    }
    if (selectedIndicators.value.includes('KDJ') && kdjChartRef.value) {
      kdjChart = echarts.init(kdjChartRef.value)
      renderKDJChart()
    }
    if (selectedIndicators.value.includes('RSI') && rsiChartRef.value) {
      rsiChart = echarts.init(rsiChartRef.value)
      renderRSIChart()
    }
    if (selectedIndicators.value.includes('VOL') && volChartRef.value) {
      volChart = echarts.init(volChartRef.value)
      renderVOLChart()
    }
  })
}

function renderMainChart() {
  if (!mainChart || !props.data || props.data.length === 0) return

  const dates = props.data.map(d => d.日期 || d.date || '')
  const klineData = props.data.map(d => [d.开盘 || d.open || 0, d.收盘 || d.close || 0, d.最低 || d.low || 0, d.最高 || d.high || 0])

  const series: any[] = [
    {
      name: 'K线',
      type: 'candlestick',
      data: klineData,
      itemStyle: {
        color: '#ef232a',
        color0: '#14b143',
        borderColor: '#ef232a',
        borderColor0: '#14b143'
      }
    }
  ]

  // 添加均线 - 支持多种字段名格式
  if (selectedIndicators.value.includes('MA')) {
    const ma5Data = props.data.map(d => d.MA5 || d.ma5 || d.ma_5 || null).filter(v => v !== null)
    const ma10Data = props.data.map(d => d.MA10 || d.ma10 || d.ma_10 || null).filter(v => v !== null)
    const ma20Data = props.data.map(d => d.MA20 || d.ma20 || d.ma_20 || null).filter(v => v !== null)
    const ma60Data = props.data.map(d => d.MA60 || d.ma60 || d.ma_60 || null).filter(v => v !== null)

    if (ma5Data.length > 0) {
      series.push({
        name: 'MA5',
        type: 'line',
        data: props.data.map(d => d.MA5 || d.ma5 || d.ma_5 || null),
        smooth: true,
        lineStyle: { width: 1, color: '#FF6B6B' },
        showSymbol: false,
        connectNulls: true
      })
    }
    if (ma10Data.length > 0) {
      series.push({
        name: 'MA10',
        type: 'line',
        data: props.data.map(d => d.MA10 || d.ma10 || d.ma_10 || null),
        smooth: true,
        lineStyle: { width: 1, color: '#4ECDC4' },
        showSymbol: false,
        connectNulls: true
      })
    }
    if (ma20Data.length > 0) {
      series.push({
        name: 'MA20',
        type: 'line',
        data: props.data.map(d => d.MA20 || d.ma20 || d.ma_20 || null),
        smooth: true,
        lineStyle: { width: 1, color: '#45B7D1' },
        showSymbol: false,
        connectNulls: true
      })
    }
    if (ma60Data.length > 0) {
      series.push({
        name: 'MA60',
        type: 'line',
        data: props.data.map(d => d.MA60 || d.ma60 || d.ma_60 || null),
        smooth: true,
        lineStyle: { width: 1, color: '#96CEB4' },
        showSymbol: false,
        connectNulls: true
      })
    }
  }

  // 添加布林带 - 支持多种字段名格式
  if (selectedIndicators.value.includes('BOLL')) {
    const bollUpperData = props.data.map(d => d.BOLL_UPPER || d.boll_upper || d.upper || d.UPPER || null).filter(v => v !== null)
    
    if (bollUpperData.length > 0) {
      series.push({
        name: 'BOLL上轨',
        type: 'line',
        data: props.data.map(d => d.BOLL_UPPER || d.boll_upper || d.upper || d.UPPER || null),
        lineStyle: { width: 1, color: '#9B59B6', type: 'dashed' },
        showSymbol: false,
        connectNulls: true
      })
      series.push({
        name: 'BOLL中轨',
        type: 'line',
        data: props.data.map(d => d.BOLL_MIDDLE || d.boll_middle || d.middle || d.MIDDLE || d.boll || d.BOLL || null),
        lineStyle: { width: 1, color: '#E74C3C' },
        showSymbol: false,
        connectNulls: true
      })
      series.push({
        name: 'BOLL下轨',
        type: 'line',
        data: props.data.map(d => d.BOLL_LOWER || d.boll_lower || d.lower || d.LOWER || null),
        lineStyle: { width: 1, color: '#9B59B6', type: 'dashed' },
        showSymbol: false,
        connectNulls: true
      })
    }
  }

  const option = {
    animation: false,
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: series.map(s => s.name),
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
      boundaryGap: true,
      axisLine: { lineStyle: { color: '#8392A5' } }
    },
    yAxis: {
      scale: true,
      splitLine: { show: true, lineStyle: { color: '#eee' } },
      axisLine: { lineStyle: { color: '#8392A5' } }
    },
    dataZoom: [
      { type: 'inside', start: 80, end: 100 },
      { show: true, type: 'slider', top: '90%', start: 80, end: 100 }
    ],
    series
  }

  mainChart.setOption(option)
}

function renderMACDChart() {
  if (!macdChart || !props.data || props.data.length === 0) return

  const dates = props.data.map(d => d.日期 || d.date || '')
  const macdBar = props.data.map(d => d.MACD || d.macd || d.macd_bar || d.MACD_BAR || 0)
  const dif = props.data.map(d => d.DIF || d.dif || d.DIFF || d.diff || 0)
  const dea = props.data.map(d => d.DEA || d.dea || d.SIGNAL || d.signal || 0)

  // 检查是否有数据
  const hasData = macdBar.some(v => v !== 0) || dif.some(v => v !== 0) || dea.some(v => v !== 0)
  if (!hasData) {
    console.warn('MACD数据全部为0，请检查数据源')
  }

  const option = {
    animation: false,
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['MACD', 'DIF', 'DEA'],
      top: 5
    },
    grid: {
      left: 60,
      right: 60,
      top: 40,
      bottom: 30
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: '#8392A5' } }
    },
    yAxis: {
      scale: true,
      splitLine: { lineStyle: { color: '#eee' } },
      axisLine: { lineStyle: { color: '#8392A5' } }
    },
    series: [
      {
        name: 'MACD',
        type: 'bar',
        data: macdBar,
        itemStyle: {
          color: (params: any) => params.value >= 0 ? '#ef232a' : '#14b143'
        }
      },
      {
        name: 'DIF',
        type: 'line',
        data: dif,
        lineStyle: { width: 1, color: '#FF6B6B' },
        showSymbol: false
      },
      {
        name: 'DEA',
        type: 'line',
        data: dea,
        lineStyle: { width: 1, color: '#4ECDC4' },
        showSymbol: false
      }
    ]
  }

  macdChart.setOption(option)
}

function renderKDJChart() {
  if (!kdjChart || !props.data || props.data.length === 0) return

  const dates = props.data.map(d => d.日期 || d.date || '')
  const k = props.data.map(d => d.K || d.k || d.kdj_k || d.KDJ_K || 0)
  const d = props.data.map(d => d.D || d.d || d.kdj_d || d.KDJ_D || 0)
  const j = props.data.map(d => d.J || d.j || d.kdj_j || d.KDJ_J || 0)

  // 检查是否有数据
  const hasData = k.some(v => v !== 0) || d.some(v => v !== 0) || j.some(v => v !== 0)
  if (!hasData) {
    console.warn('KDJ数据全部为0，请检查数据源')
  }

  const option = {
    animation: false,
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['K', 'D', 'J'],
      top: 5
    },
    grid: {
      left: 60,
      right: 60,
      top: 40,
      bottom: 30
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: '#8392A5' } }
    },
    yAxis: {
      scale: true,
      min: 0,
      max: 100,
      splitLine: { lineStyle: { color: '#eee' } },
      axisLine: { lineStyle: { color: '#8392A5' } }
    },
    series: [
      {
        name: 'K',
        type: 'line',
        data: k,
        lineStyle: { width: 1, color: '#FF6B6B' },
        showSymbol: false
      },
      {
        name: 'D',
        type: 'line',
        data: d,
        lineStyle: { width: 1, color: '#4ECDC4' },
        showSymbol: false
      },
      {
        name: 'J',
        type: 'line',
        data: j,
        lineStyle: { width: 1, color: '#FFA500' },
        showSymbol: false
      }
    ]
  }

  kdjChart.setOption(option)
}

function renderRSIChart() {
  if (!rsiChart || !props.data || props.data.length === 0) return

  const dates = props.data.map(d => d.日期 || d.date || '')
  const rsi6 = props.data.map(d => d.RSI6 || d.rsi6 || d.rsi_6 || d.RSI_6 || 0)
  const rsi12 = props.data.map(d => d.RSI12 || d.rsi12 || d.rsi_12 || d.RSI_12 || 0)
  const rsi24 = props.data.map(d => d.RSI24 || d.rsi24 || d.rsi_24 || d.RSI_24 || 0)

  // 检查是否有数据
  const hasData = rsi6.some(v => v !== 0) || rsi12.some(v => v !== 0) || rsi24.some(v => v !== 0)
  if (!hasData) {
    console.warn('RSI数据全部为0，请检查数据源')
  }

  const option = {
    animation: false,
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['RSI6', 'RSI12', 'RSI24'],
      top: 5
    },
    grid: {
      left: 60,
      right: 60,
      top: 40,
      bottom: 30
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: '#8392A5' } }
    },
    yAxis: {
      scale: true,
      min: 0,
      max: 100,
      splitLine: { lineStyle: { color: '#eee' } },
      axisLine: { lineStyle: { color: '#8392A5' } }
    },
    series: [
      {
        name: 'RSI6',
        type: 'line',
        data: rsi6,
        lineStyle: { width: 1, color: '#FF6B6B' },
        showSymbol: false
      },
      {
        name: 'RSI12',
        type: 'line',
        data: rsi12,
        lineStyle: { width: 1, color: '#4ECDC4' },
        showSymbol: false
      },
      {
        name: 'RSI24',
        type: 'line',
        data: rsi24,
        lineStyle: { width: 1, color: '#45B7D1' },
        showSymbol: false
      }
    ]
  }

  rsiChart.setOption(option)
}

function renderVOLChart() {
  if (!volChart || !props.data || props.data.length === 0) return

  const dates = props.data.map(d => d.日期 || d.date || '')
  const volumes = props.data.map(d => d.成交量 || d.volume || d.vol || d.VOL || 0)
  const volMa5 = props.data.map(d => d.VOL_MA5 || d.vol_ma5 || d.volume_ma5 || 0)
  const volMa10 = props.data.map(d => d.VOL_MA10 || d.vol_ma10 || d.volume_ma10 || 0)

  // 检查是否有数据
  const hasData = volumes.some(v => v !== 0)
  if (!hasData) {
    console.warn('成交量数据全部为0，请检查数据源')
  }

  const option = {
    animation: false,
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' },
      formatter: (params: any) => {
        let result = params[0].axisValue + '<br/>'
        params.forEach((item: any) => {
          const value = item.value
          const formattedValue = value >= 100000000 
            ? (value / 100000000).toFixed(2) + '亿'
            : value >= 10000 
            ? (value / 10000).toFixed(2) + '万'
            : value.toFixed(0)
          result += item.marker + item.seriesName + ': ' + formattedValue + '<br/>'
        })
        return result
      }
    },
    legend: {
      data: ['成交量', 'VOL_MA5', 'VOL_MA10'],
      top: 5
    },
    grid: {
      left: 60,
      right: 60,
      top: 40,
      bottom: 30
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: '#8392A5' } }
    },
    yAxis: {
      scale: true,
      splitLine: { lineStyle: { color: '#eee' } },
      axisLine: { lineStyle: { color: '#8392A5' } },
      axisLabel: {
        formatter: (value: number) => {
          if (value >= 100000000) return (value / 100000000).toFixed(0) + '亿'
          if (value >= 10000) return (value / 10000).toFixed(0) + '万'
          return value.toString()
        }
      }
    },
    series: [
      {
        name: '成交量',
        type: 'bar',
        data: volumes,
        itemStyle: {
          color: (params: any) => {
            const idx = params.dataIndex
            if (idx === 0) return '#ef232a'
            const curr = props.data[idx]
            const prev = props.data[idx - 1]
            const currClose = curr.收盘 || curr.close || 0
            const prevClose = prev.收盘 || prev.close || 0
            return currClose >= prevClose ? '#ef232a' : '#14b143'
          }
        }
      },
      {
        name: 'VOL_MA5',
        type: 'line',
        data: volMa5,
        lineStyle: { width: 1, color: '#FF6B6B' },
        showSymbol: false
      },
      {
        name: 'VOL_MA10',
        type: 'line',
        data: volMa10,
        lineStyle: { width: 1, color: '#4ECDC4' },
        showSymbol: false
      }
    ]
  }

  volChart.setOption(option)
}

function handleIndicatorChange() {
  destroyCharts()
  nextTick(() => {
    initCharts()
  })
}

function destroyCharts() {
  if (mainChart) {
    mainChart.dispose()
    mainChart = null
  }
  if (macdChart) {
    macdChart.dispose()
    macdChart = null
  }
  if (kdjChart) {
    kdjChart.dispose()
    kdjChart = null
  }
  if (rsiChart) {
    rsiChart.dispose()
    rsiChart = null
  }
  if (volChart) {
    volChart.dispose()
    volChart = null
  }
}

function resize() {
  mainChart?.resize()
  macdChart?.resize()
  kdjChart?.resize()
  rsiChart?.resize()
  volChart?.resize()
}

watch(() => props.data, () => {
  destroyCharts()
  nextTick(() => {
    initCharts()
  })
}, { deep: true })

onMounted(() => {
  initCharts()
  window.addEventListener('resize', resize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resize)
  destroyCharts()
})

defineExpose({ resize })
</script>

<style scoped>
.technical-chart-wrapper {
  background: #ffffff;
  padding: 20px;
  border-radius: 8px;
}

.indicator-selector {
  margin-bottom: 20px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 6px;
}

.indicator-selector :deep(.el-checkbox) {
  margin-right: 12px;
  margin-bottom: 8px;
}

.main-chart, .sub-chart {
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 10px;
  background: #fff;
}
</style>
