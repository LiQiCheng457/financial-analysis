<template>
  <div class="stock-chart-card">
    <el-card>
      <template #header>
        <div style="display:flex;align-items:center;justify-content:space-between;">
          <div>
            <strong>{{ title }}</strong>
            <small style="margin-left:8px;color:#909399;font-size:12px">({{ subtitle }})</small>
          </div>
          <div style="display:flex;gap:8px;align-items:center;">
            <el-input v-model="symbol" size="small" style="width:140px" placeholder="股票代码" />
            <el-button size="small" type="primary" @click="fetchAndRender">刷新</el-button>
          </div>
        </div>
      </template>

      <div ref="chartRef" style="height:360px;width:100%"></div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts/core'
import { LineChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, LegendComponent, DataZoomComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { getStockHistory } from '@/api/stock'
import dayjs from 'dayjs'

echarts.use([LineChart, GridComponent, TooltipComponent, LegendComponent, DataZoomComponent, CanvasRenderer])

const props = defineProps({
  title: { type: String, default: '个股最近一年行情' },
  subtitle: { type: String, default: '折线图 — 收盘价' },
})

const chartRef = ref<HTMLDivElement | null>(null)
let chart: echarts.ECharts | null = null

const symbol = ref('000001')
const loading = ref(false)

// helper: get first existing field from candidates
const pickField = (row: any, candidates: string[]) => {
  for (const k of candidates) {
    if (row == null) break
    if (Object.prototype.hasOwnProperty.call(row, k) && row[k] != null) return row[k]
  }
  return undefined
}

// map of possible column names
const COLS = {
  date: ['日期', 'trade_date', 'date'],
  open: ['开盘', 'open', 'open_price', 'openPrice'],
  close: ['收盘', 'close', 'close_price', 'closePrice'],
  high: ['最高', 'high', 'high_price', 'highPrice'],
  low: ['最低', 'low', 'low_price', 'lowPrice']
}

const fetchAndRender = async () => {
  if (!symbol.value) return
  loading.value = true
  try {
  const end = dayjs()
  const start = end.subtract(1, 'year')
    const params = {
      code: symbol.value,
      start_date: start.format('YYYYMMDD'),
      end_date: end.format('YYYYMMDD'),
      adjust: ''
    }
    console.debug('[StockChart] fetch params:', params)
    const data = await getStockHistory(params)
    console.debug('[StockChart] fetch response:', data)

    const list = Array.isArray(data) ? data : (data && data.data ? data.data : [])

    // normalize rows: extract date and numeric fields
    const normalized = list.map((r: any) => {
      const rawDate = pickField(r, COLS.date) || pickField(r, ['日期', 'trade_date', 'date'])
      // try to parse date into YYYY-MM-DD for x-axis label
      let dateStr = rawDate
      if (rawDate) {
        const d = dayjs(String(rawDate))
        if (d.isValid()) dateStr = d.format('YYYY-MM-DD')
        else dateStr = String(rawDate)
      }
      const openV = pickField(r, COLS.open)
      const closeV = pickField(r, COLS.close)
      const highV = pickField(r, COLS.high)
      const lowV = pickField(r, COLS.low)
      return {
        _raw: r,
        dateRaw: rawDate,
        date: dateStr,
        open: openV == null || openV === '' ? null : Number(openV),
        close: closeV == null || closeV === '' ? null : Number(closeV),
        high: highV == null || highV === '' ? null : Number(highV),
        low: lowV == null || lowV === '' ? null : Number(lowV)
      }
    })

    // sort by parsed date when possible, otherwise keep original order
    const sorted = normalized.slice().sort((a: any, b: any) => {
      const da = dayjs(a.date)
      const db = dayjs(b.date)
      if (da.isValid() && db.isValid()) return da.valueOf() - db.valueOf()
      return String(a.date || '').localeCompare(b.date || '')
    })

// no-op: source selection removed, refresh controlled by symbol input and button
    const x = sorted.map((r: any) => r.date)
  const openArr = sorted.map((r: any) => (r.open == null ? null : r.open))
  const closeArr = sorted.map((r: any) => (r.close == null ? null : r.close))
  const highArr = sorted.map((r: any) => (r.high == null ? null : r.high))
  const lowArr = sorted.map((r: any) => (r.low == null ? null : r.low))

    const seriesMap: Record<string, any[]> = {
      '开盘': openArr,
      '收盘': closeArr,
      '最高': highArr,
      '最低': lowArr
    }
    renderChart(x, seriesMap)
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

const renderChart = (x: string[], seriesMap: Record<string, any[]>) => {
  if (!chartRef.value) return
  if (!chart) chart = echarts.init(chartRef.value as HTMLDivElement)
  try {
    chart.clear()
  } catch (e) {
    // ignore
  }

  const series = Object.keys(seriesMap).map(name => {
    const arr = seriesMap[name] || []
    const lastIndex = arr.length - 1
    const lastVal = lastIndex >= 0 ? arr[lastIndex] : null
    return {
      name,
      type: 'line',
      data: arr,
      showSymbol: false,
      smooth: true,
      markPoint: {
        data: [
          { type: 'max', name: '最大值' },
          { type: 'min', name: '最小值' },
          lastVal != null && x[lastIndex] ? { name: '最新', coord: [x[lastIndex], lastVal] } : null
        ].filter(Boolean)
      }
    }
  })

  const option = {
    tooltip: { trigger: 'axis' },
    legend: { data: Object.keys(seriesMap) },
    xAxis: { type: 'category', data: x },
    yAxis: { type: 'value', scale: true },
    series,
    dataZoom: [{ type: 'inside' }, { type: 'slider' }]
  }
  chart.setOption(option, { notMerge: true })
}

onMounted(() => {
  fetchAndRender()
})

onUnmounted(() => {
  try {
    if (chart) {
      chart.dispose()
      chart = null
    }
    window.removeEventListener('resize', _resizeHandler)
  } catch (e) {
    // ignore
  }
})

const _resizeHandler = () => {
  try {
    if (chart) chart.resize()
  } catch (e) {
    // ignore
  }
}

window.addEventListener('resize', _resizeHandler)

// no-op: source selection removed, refresh controlled by symbol input and button
</script>

<style scoped>
.stock-chart-card {
  margin-bottom: 16px;
}
</style>
