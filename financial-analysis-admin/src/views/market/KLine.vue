<template>
  <PageShell>
    <template #title> K 线图 </template>
    <template #actions>
      <el-button type="primary" size="small" @click="exportCsv">导出</el-button>
    </template>

    <div>
      <el-form inline>
        <el-form-item>
          <el-input v-model="code" placeholder="股票代码 (例如 600000 或 sh600000)" style="width:220px" />
        </el-form-item>
        <el-form-item>
          <el-select v-model="period" placeholder="周期" size="small">
            <el-option label="日" value="day" />
            <el-option label="周" value="week" />
            <el-option label="月" value="month" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="small" @click="load">加载</el-button>
        </el-form-item>
      </el-form>

      <div style="margin-top:12px">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px">
          <!-- start date selects -->
          <el-select v-model="startYear" placeholder="年" style="width:100px">
            <el-option v-for="y in years" :key="y" :label="y" :value="y" />
          </el-select>
          <el-select v-model="startMonth" placeholder="月" style="width:80px">
            <el-option v-for="m in months" :key="m" :label="m" :value="m" />
          </el-select>
          <el-select v-model="startDay" placeholder="日" style="width:80px">
            <el-option v-for="d in startDays" :key="d" :label="d" :value="d" />
          </el-select>

          <!-- end date selects -->
          <el-select v-model="endYear" placeholder="年" style="width:100px">
            <el-option v-for="y in years" :key="'e'+y" :label="y" :value="y" />
          </el-select>
          <el-select v-model="endMonth" placeholder="月" style="width:80px">
            <el-option v-for="m in months" :key="'e'+m" :label="m" :value="m" />
          </el-select>
          <el-select v-model="endDay" placeholder="日" style="width:80px">
            <el-option v-for="d in endDays" :key="'e'+d" :label="d" :value="d" />
          </el-select>

          <el-button size="small" @click="applyPickRange">应用范围</el-button>
          <el-button size="small" @click="applyChartVisibleRange">锁定当前视图为查询范围</el-button>
          <div style="margin-left:12px">当前可见: <strong>{{ visibleStart }} - {{ visibleEnd }}</strong></div>
        </div>

        <OHLCVChart ref="chartRef" :data="records" :period="period" @visible-range="onVisibleRange" />
      </div>
    </div>
  </PageShell>
</template>

<script setup lang="ts">
import PageShell from '@/components/PageShell.vue'
import { ElButton } from 'element-plus'
import { ref, watch } from 'vue'
import OHLCVChart from '@/components/OHLCVChart.vue'
import { getStockHistory } from '@/api/stock'

const code = ref('600000')
const period = ref<'day'|'week'|'month'>('day')
const records = ref<any[]>([])
// year/month/day selects
const now = new Date()
const thisYear = now.getFullYear()
const years = Array.from({ length: 6 }).map((_, i) => thisYear - i)
const months = Array.from({ length: 12 }).map((_, i) => i+1)

const startYear = ref<number>(thisYear)
const startMonth = ref<number>(now.getMonth()+1)
const startDay = ref<number>(now.getDate())
const endYear = ref<number>(thisYear)
const endMonth = ref<number>(now.getMonth()+1)
const endDay = ref<number>(now.getDate())

const startDays = ref<number[]>([])
const endDays = ref<number[]>([])

function daysInMonth(year: number, month: number) {
  return new Date(year, month, 0).getDate()
}

function updateStartDays() {
  startDays.value = Array.from({ length: daysInMonth(startYear.value, startMonth.value) }).map((_, i) => i+1)
  if (!startDays.value.includes(startDay.value)) startDay.value = startDays.value[startDays.value.length-1]
}

function updateEndDays() {
  endDays.value = Array.from({ length: daysInMonth(endYear.value, endMonth.value) }).map((_, i) => i+1)
  if (!endDays.value.includes(endDay.value)) endDay.value = endDays.value[endDays.value.length-1]
}

// initialize days
updateStartDays()
updateEndDays()

// watch month/year changes
watch([startYear, startMonth], updateStartDays)
watch([endYear, endMonth], updateEndDays)
const visibleStart = ref<string>('')
const visibleEnd = ref<string>('')
const chartRef = ref<any | null>(null)

async function load() {
  if (!code.value) return
  try {
    // fetch a reasonable date window (1 year)
    const end = new Date()
    const start = new Date()
    start.setFullYear(start.getFullYear() - 1)
    const fmt = (d: Date) => `${d.getFullYear()}${String(d.getMonth()+1).padStart(2,'0')}${String(d.getDate()).padStart(2,'0')}`
    const resp: any = await getStockHistory({ code: code.value, start_date: fmt(start), end_date: fmt(end), source: 'eastmoney' })
    // resp expected to be an array of records with chinese keys like 日期/开盘/最高/最低/收盘/成交量
    records.value = (Array.isArray(resp) ? resp : [])
  } catch (e) {
    console.error(e)
  }
}

// initial load
load()

// no-op: remote search removed; user loads via 点击“加载”或手动刷新

function onVisibleRange(payload: any) {
  visibleStart.value = payload.startDateRaw || payload.startDate || ''
  visibleEnd.value = payload.endDateRaw || payload.endDate || ''
}

function applyPickRange() {
  const s = `${startYear.value}${String(startMonth.value).padStart(2,'0')}${String(startDay.value).padStart(2,'0')}`
  const e = `${endYear.value}${String(endMonth.value).padStart(2,'0')}${String(endDay.value).padStart(2,'0')}`
  loadWithRange(s, e)
}

function applyChartVisibleRange() {
  // try to get visible range from chart component
  try {
    const v = chartRef.value?.getVisibleRange?.()
    if (v && v.startDateRaw && v.endDateRaw) {
      const s = v.startDateRaw.replace(/-/g, '')
      const e = v.endDateRaw.replace(/-/g, '')
      loadWithRange(s, e)
    } else {
      alert('无法获取当前视图范围')
    }
  } catch (e) {
    console.error(e)
  }
}

async function loadWithRange(s: string, e: string) {
  if (!code.value) return
  try {
    const resp: any = await getStockHistory({ code: code.value, start_date: s, end_date: e, source: 'eastmoney' })
    records.value = (Array.isArray(resp) ? resp : [])
  } catch (err) {
    console.error(err)
  }
}

function aggregateForExport(data: any[], periodVal: string) {
  if (!data || !data.length) return []
  if (periodVal === 'day') {
    return data.map(r => ({ date: r['日期'], open: r['开盘'], high: r['最高'], low: r['最低'], close: r['收盘'], volume: r['成交量'] || 0 }))
  }

  // group by week/month similar logic as in OHLCVChart
  const groups: Record<string, any[]> = {}
  data.forEach(r => {
    const d = new Date(r['日期'])
    let key = ''
    if (periodVal === 'week') {
      const year = d.getFullYear()
      const week = getWeekNumber(d)
      key = `${year}-W${String(week).padStart(2,'0')}`
    } else {
      const year = d.getFullYear()
      const m = d.getMonth() + 1
      key = `${year}-${String(m).padStart(2,'0')}`
    }
    groups[key] = groups[key] || []
    groups[key].push(r)
  })

  const out: any[] = []
  for (const k of Object.keys(groups).sort()) {
    const arr = groups[k].sort((a,b)=>a['日期'].localeCompare(b['日期']))
    const open = arr[0]['开盘']
    const close = arr[arr.length-1]['收盘']
    const high = Math.max(...arr.map(x=>x['最高']))
    const low = Math.min(...arr.map(x=>x['最低']))
    const vol = arr.reduce((s,x)=>s + (x['成交量']||0), 0)
    out.push({ date: k, open, high, low, close, volume: vol })
  }
  return out
}

function getWeekNumber(d: Date) {
  const dt = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()))
  dt.setUTCDate(dt.getUTCDate() + 4 - (dt.getUTCDay() || 7))
  const yearStart = new Date(Date.UTC(dt.getUTCFullYear(), 0, 1))
  const weekNo = Math.ceil((((dt.getTime() - yearStart.getTime()) / 86400000) + 1) / 7)
  return weekNo
}

function toCsv(rows: any[]) {
  if (!rows || !rows.length) return ''
  const header = ['日期','开盘','最高','最低','收盘','成交量']
  const lines = [header.join(',')]
  for (const r of rows) {
    lines.push([r.date, r.open, r.high, r.low, r.close, r.volume].join(','))
  }
  return lines.join('\n')
}

function exportCsv() {
  const agg = aggregateForExport(records.value, period.value)
  if (!agg || !agg.length) {
    // 使用 Element Plus 的消息提示更友好，但避免额外依赖，这里用 alert
    alert('暂无数据可导出')
    return
  }
  const csv = toCsv(agg)
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${code.value}_${period.value}_ohlcv.csv`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

</script>
