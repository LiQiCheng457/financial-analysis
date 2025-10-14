<template>
  <div class="ohlcv-chart" ref="root" style="width:100%;height:500px"></div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'

interface RecordRow {
  日期: string
  开盘: number
  最高: number
  最低: number
  收盘: number
  成交量: number
  [k: string]: any
}

const props = defineProps<{
  data: RecordRow[]
  period?: 'day' | 'week' | 'month'
  autoResize?: boolean
}>()

const root = ref<HTMLDivElement | null>(null)
const emit = defineEmits<{
  (e: 'visible-range', payload: { startIndex: number; endIndex: number; startDate: string; endDate: string; startDateRaw: string; endDateRaw: string }): void
}>()
let chart: echarts.ECharts | null = null
let currentDates: string[] = []
let currentRawRanges: Array<[string,string]> = []

function aggregate(records: RecordRow[], period: string) {
  if (!records || !records.length) return { dates: [], ohlc: [], volumes: [] }

  if (period === 'day') {
    const dates = records.map(r => r['日期'])
    const ohlc = records.map(r => [r['开盘'], r['收盘'], r['最低'], r['最高']])
    const vols = records.map(r => r['成交量'] ?? 0)
    const rawRanges = dates.map(d => [d, d] as [string,string])
    return { dates, ohlc, volumes: vols, rawRanges }
  }

  // group by week or month
  const groups: Record<string, RecordRow[]> = {}
  records.forEach(r => {
    const d = new Date(r['日期'])
    let key = ''
    if (period === 'week') {
      // ISO week year-week
      const year = d.getFullYear()
      const week = getWeekNumber(d)
      key = `${year}-W${String(week).padStart(2, '0')}`
    } else {
      const year = d.getFullYear()
      const m = d.getMonth() + 1
      key = `${year}-${String(m).padStart(2, '0')}`
    }
    groups[key] = groups[key] || []
    groups[key].push(r)
  })

  const dates: string[] = []
  const ohlc: number[][] = []
  const volumes: number[] = []

  for (const key of Object.keys(groups).sort()) {
    const arr = groups[key].sort((a, b) => a['日期'].localeCompare(b['日期']))
    const open = arr[0]['开盘']
    const close = arr[arr.length - 1]['收盘']
    const high = Math.max(...arr.map(x => x['最高']))
    const low = Math.min(...arr.map(x => x['最低']))
    const vol = arr.reduce((s, x) => s + (x['成交量'] || 0), 0)
    dates.push(key)
    ohlc.push([open, close, low, high])
    volumes.push(vol)
  }

  const rawRanges = dates.map((_, i) => [dates[i], dates[i]] as [string,string])
  return { dates, ohlc, volumes, rawRanges }
}

function getWeekNumber(d: Date) {
  // Copy date so don't modify original
  const dt = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()))
  // Set to nearest Thursday: current date + 4 - current day number
  dt.setUTCDate(dt.getUTCDate() + 4 - (dt.getUTCDay() || 7))
  const yearStart = new Date(Date.UTC(dt.getUTCFullYear(), 0, 1))
  const weekNo = Math.ceil((((dt.getTime() - yearStart.getTime()) / 86400000) + 1) / 7)
  return weekNo
}

function buildOption(dates: string[], ohlc: number[][], volumes: number[]) {
  return {
    animation: false,
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      formatter: function (params: any) {
        // params is array: kline series first then volume
        const k = params[0]
        if (!k) return ''
        const idx = k.dataIndex
        const d = dates[idx]
        const o = k.data[0]
        const c = k.data[1]
        const l = k.data[2]
        const h = k.data[3]
        const v = volumes[idx]
        return `${d}<br/>开盘: ${o}<br/>最高: ${h}<br/>最低: ${l}<br/>收盘: ${c}<br/>成交量: ${v}`
      }
    },
    axisPointer: {
      link: [{ xAxisIndex: [0, 1] }]
    },
    toolbox: { show: false },
    grid: [
      { left: '10%', right: '8%', top: 20, height: '60%' },
      { left: '10%', right: '8%', top: '72%', height: '18%' }
    ],
    xAxis: [
      {
        type: 'category',
        data: dates,
        scale: true,
        boundaryGap: false,
        axisLine: { onZero: false },
        splitLine: { show: false },
        min: 'dataMin',
        max: 'dataMax'
      },
      {
        type: 'category',
        gridIndex: 1,
        data: dates,
        axisLabel: { show: false }
      }
    ],
    yAxis: [
      { scale: true, splitArea: { show: false }, splitLine: { show: false } },
      { gridIndex: 1, splitNumber: 3, axisLabel: { show: true } }
    ],
    dataZoom: [
      { type: 'inside', xAxisIndex: [0, 1], start: 0, end: 100 },
      { show: true, xAxisIndex: [0, 1], type: 'slider', top: '85%', start: 0, end: 100 }
    ],
    series: [
      {
        name: 'K',
        type: 'candlestick',
        data: ohlc,
        itemStyle: { color: '#ec0000', color0: '#00da3c', borderColor: '#8A0000', borderColor0: '#008F28' }
      },
      {
        name: 'Volume',
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        data: volumes,
        itemStyle: { color: '#7f8c8d' }
      }
    ]
  }
}

function renderChart() {
  if (!chart || !props.data) return
  const { dates, ohlc, volumes, rawRanges } = aggregate(props.data, props.period || 'day')
  currentDates = dates
  currentRawRanges = rawRanges || []
  const option = buildOption(dates, ohlc, volumes)
  chart.setOption(option)
}

onMounted(() => {
  if (root.value) {
    chart = echarts.init(root.value)
    renderChart()
    // listen to dataZoom events and emit visible-range
    chart.on('datazoom', (e: any) => {
      try {
        const zr = e.batch && e.batch.length ? e.batch[0] : e
        const start = (zr.start != null) ? zr.start : (e.start || 0)
        const end = (zr.end != null) ? zr.end : (e.end || 100)
        // start/end are percent; convert to index
        if (currentDates && currentDates.length) {
          const len = currentDates.length
          const sIdx = Math.floor((start/100) * len)
          const eIdx = Math.min(len-1, Math.ceil((end/100) * len)-1)
          const startDate = currentDates[sIdx]
          const endDate = currentDates[eIdx]
          const startDateRaw = (currentRawRanges[sIdx] && currentRawRanges[sIdx][0]) || startDate
          const endDateRaw = (currentRawRanges[eIdx] && currentRawRanges[eIdx][1]) || endDate
          emit('visible-range', { startIndex: sIdx, endIndex: eIdx, startDate, endDate, startDateRaw, endDateRaw })
        }
      } catch (err) {
        // ignore
      }
    })
    window.addEventListener('resize', () => chart && chart.resize())
  }
})

onBeforeUnmount(() => {
  if (chart) {
    chart.dispose()
    chart = null
  }
  window.removeEventListener('resize', () => chart && chart.resize())
})

watch(() => [props.data, props.period], () => {
  try {
    renderChart()
  } catch (e) {
    // ignore
  }
}, { deep: true })

// expose getter to parent
function getVisibleRange() {
  if (!currentDates || !currentDates.length) return null
  // try to read dataZoom start/end from chart
  try {
    const options = chart?.getOption()
    const dz = options?.dataZoom?.[0]
    if (dz && dz.start != null && dz.end != null) {
      const len = currentDates.length
      const sIdx = Math.floor((dz.start/100) * len)
      const eIdx = Math.min(len-1, Math.ceil((dz.end/100) * len)-1)
      return { startIndex: sIdx, endIndex: eIdx, startDate: currentDates[sIdx], endDate: currentDates[eIdx], startDateRaw: currentRawRanges[sIdx]?.[0], endDateRaw: currentRawRanges[eIdx]?.[1] }
    }
  } catch (e) {
    // ignore
  }
  return null
}

defineExpose({ getVisibleRange })
</script>

<style scoped>
.ohlcv-chart { background: var(--el-bg-color) }
</style>
