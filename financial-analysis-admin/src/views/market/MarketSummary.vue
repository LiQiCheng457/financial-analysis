<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>上海证券交易所 - 每日概况
            <small v-if="formattedQueryDate" style="margin-left:8px;color:#909399;font-size:12px">({{ formattedQueryDate }} 查询)</small>
          </span>
          <span v-if="actualDate" class="actual-date-tip">
            数据日期: {{ formattedActualDate }}
            <el-tooltip v-if="isHoliday" content="您选择的日期为休市日，已自动为您展示前一交易日的数据。" placement="top">
              <el-icon><QuestionFilled /></el-icon>
            </el-tooltip>
          </span>
        </div>
      </template>

      <el-form :inline="true" @submit.prevent="fetchSummaryData">
        <el-form-item label="查询日期">
          <el-date-picker
            v-model="queryDate"
            type="date"
            placeholder="选择日期"
            format="YYYY-MM-DD"
            value-format="YYYYMMDD"
            :disabled-date="disabledDate"
            style="width: 150px;"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchSummaryData" :loading="loading">查询</el-button>
        </el-form-item>
      </el-form>

          <!-- date navigator: prev / next / today -->
          <div style="display:flex;align-items:center;gap:8px;margin-top:8px;">
            <el-button size="mini" @click="prevDates">上一组</el-button>
            <el-button size="mini" @click="centerToday">回到今天</el-button>
            <el-button size="mini" @click="nextDates">下一组</el-button>
            <div style="margin-left:8px;display:flex;align-items:center;gap:6px">
              <span style="color:#909399">显示天数</span>
              <el-input-number :min="7" :max="60" v-model="windowSize" @change="onWindowSizeChange" size="small" />
            </div>
          </div>

          <!-- small date grid (horizontal, scrollable) -->
          <div class="date-grid" ref="dateGridRef">
        <div v-for="d in dateGrid" :key="d" class="date-cell"
          :class="{
            'future': isFuture(d),
            'today': isTodayStr(d),
            'holiday': !tradeDates.has(d) && !isFuture(d),
            'selectable': tradeDates.has(d) && !isFuture(d) && !isTodayStr(d)
          }"
          @click="onGridDateClick(d)">
          <div class="date-label">{{ dayjs(d, 'YYYYMMDD').format('MM-DD') }}</div>
        </div>
      </div>

      <el-table
        v-if="summaryData.length > 0"
        :data="summaryData"
        v-loading="loading"
        border
        stripe
        style="width: 100%"
      >
        <!-- 后端返回的字段示例在 tmp_logs 中为: "单日情况", "股票", "主板A", "主板B", "科创板", "股票回购" -->
        <el-table-column prop="单日情况" label="单日情况" width="180" />
        <el-table-column prop="股票" label="股票" />
        <el-table-column prop="主板A" label="主板A" />
        <el-table-column prop="主板B" label="主板B" />
        <el-table-column prop="科创板" label="科创板" />
        <el-table-column prop="股票回购" label="股票回购" />
        
      </el-table>
      <el-empty v-else-if="!loading" :description="emptyText" />

      

    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { getSseDailySummary, getTradeDates } from '@/api/stock'
import { ElMessage } from 'element-plus'
import { QuestionFilled } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const queryDate = ref('')
const actualDate = ref('')
const summaryData = ref<any[]>([])
const loading = ref(false)
const tradeDates = ref<Set<string>>(new Set())
const emptyText = ref('请选择日期进行查询')
// date window for sliding navigator
const STORAGE_KEY = 'marketSummary.windowSize'
const windowSize = ref<number>(20) // number of days shown in the grid
const windowOffset = ref(0) // offset in days from today (negative means earlier)
const dateGridRef = ref<HTMLElement | null>(null)
const CELL_GAP = 6
const CELL_WIDTH = 64

const isHoliday = computed(() => !!(queryDate.value && summaryDataHoliday.value))
const formattedActualDate = computed(() => actualDate.value ? dayjs(actualDate.value, 'YYYYMMDD').format('YYYY-MM-DD') : '')
const summaryDataHoliday = ref(false)

// 日期选择器中禁用非交易日
const disabledDate = (time: Date) => {
  if (tradeDates.value.size === 0) {
    return false // 如果交易日历还没加载好，暂时不禁用任何日期
  }
  const dateStr = dayjs(time).format('YYYYMMDD')
  return !tradeDates.value.has(dateStr)
}

const formattedQueryDate = computed(() => queryDate.value ? dayjs(queryDate.value, 'YYYYMMDD').format('YYYY-MM-DD') : '')

const fetchTradeDates = async () => {
  try {
    const datesResp = await getTradeDates()
    // normalize: request util returns response.data usually, but be defensive
    const dates = Array.isArray(datesResp) ? datesResp : (datesResp && datesResp.data) ? datesResp.data : []
    tradeDates.value = new Set(dates)
    // 设置默认查询日期为最近的一个交易日 (不晚于今天)
    if (dates.length > 0) {
      const today = dayjs().format('YYYYMMDD')
      // 找到最后一个 < today 的交易日，避免把今天(未结束)作为默认
      const candidate = dates.slice().reverse().find((d: string) => d < today) || dates[dates.length - 1]
      queryDate.value = candidate
      fetchSummaryData() // 加载默认数据
    }
  } catch (error) {
    ElMessage.error('获取交易日历失败')
  }
}

const fetchSummaryData = async () => {
    if (!queryDate.value) {
    ElMessage.warning('请选择查询日期')
    return
  }
  // 处理当天和未来日期：当天提示未结束，未来提示还未开市
  const today = dayjs().format('YYYYMMDD')
  if (queryDate.value === today) {
    ElMessage.info('今日开市未结束，无数据')
    return
  }
  if (queryDate.value > today) {
    ElMessage.info(`${dayjs(queryDate.value, 'YYYYMMDD').format('YYYY-MM-DD')} 还未开市`)
    return
  }
  loading.value = true
  emptyText.value = '正在加载...'
  try {
  const res: any = await getSseDailySummary(queryDate.value)
    // normalize various possible shapes returned by the request util / backend
    // cases:
    // - res is an array => treat as payload.data
    // - res is payload object { date, data, holiday, message }
    // - res is wrapper { data: payload } (less likely since interceptor returns response.data)
    let payload: any = null
    if (!res) {
      payload = null
    } else if (Array.isArray(res)) {
      payload = { data: res, date: queryDate.value }
    } else if (typeof res === 'object') {
      // if res already looks like the payload (has date/status/holiday or data array), use it
      if ('date' in res || 'status' in res || 'holiday' in res) {
        payload = res
      } else if ('data' in res && Array.isArray(res.data)) {
        payload = res
      } else if ('data' in res && typeof res.data === 'object') {
        // res.data might be the actual payload
        payload = res.data
      } else {
        // fallback: treat object as payload with data possibly absent
        payload = res
      }
    } else {
      payload = res
    }
    
    if (!payload) {
      ElMessage.error('接口返回异常')
      summaryData.value = []
      summaryDataHoliday.value = false
      actualDate.value = ''
    } else if (payload.holiday) {
      summaryData.value = []
      summaryDataHoliday.value = true
      actualDate.value = payload.date
      emptyText.value = payload.message || `${payload.date} 为休市日`
      ElMessage.info(emptyText.value)
    } else {
      summaryData.value = Array.isArray(payload.data) ? payload.data : []
      // debug log to browser console
      try { console.log('summaryData set, length=', summaryData.value.length, summaryData.value[0]) } catch(e) {}
      summaryDataHoliday.value = false
      actualDate.value = payload.date
      if (!summaryData.value || summaryData.value.length === 0) {
        emptyText.value = payload.message || '暂无数据'
      }
    }
  } catch (error) {
    ElMessage.error('请求失败，请检查网络或联系管理员')
    summaryData.value = []
    emptyText.value = '请求失败'
    console.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // load persisted window size
  try {
    const v = window.localStorage.getItem(STORAGE_KEY)
    if (v) windowSize.value = Math.max(7, Math.min(60, Number(v)))
  } catch (e) {}
  fetchTradeDates()
})

const centerToday = () => {
  windowOffset.value = 0
  // smooth scroll to center after grid recomputes
  nextTick(() => scrollToCenter())
}

const prevDates = () => {
  windowOffset.value -= windowSize.value
  nextTick(() => smoothScrollBy(-1))
}

const nextDates = () => {
  windowOffset.value += windowSize.value
  nextTick(() => smoothScrollBy(1))
}

// persist windowSize changes
const onWindowSizeChange = (v: number) => {
  try { window.localStorage.setItem(STORAGE_KEY, String(v)) } catch(e) {}
}

// helpers to scroll the dateGrid
function getGridEl(): HTMLElement | null {
  return (dateGridRef.value as unknown as HTMLElement) || document.querySelector('.date-grid')
}

function smoothScrollBy(direction: number) {
  // direction: ±1 number of windows to move (we already changed offset), smoothly scroll container by approx window width
  const grid = getGridEl()
  if (!grid) return
  const step = (CELL_WIDTH + CELL_GAP) * windowSize.value
  grid.scrollBy({ left: direction * step, behavior: 'smooth' })
}

function scrollToCenter() {
  const grid = getGridEl()
  if (!grid) return
  // if a queryDate is set, center it; otherwise center today's middle position
  const targetDate = queryDate.value || dayjs().format('YYYYMMDD')
  const idx = dateGrid.value.indexOf(targetDate)
  if (idx === -1) return
  const items = grid.querySelectorAll('.date-cell')
  const item = items[idx] as HTMLElement
  if (!item) return
  const containerRect = grid.getBoundingClientRect()
  const itemRect = item.getBoundingClientRect()
  const targetScrollLeft = grid.scrollLeft + (itemRect.left - containerRect.left) - (containerRect.width / 2) + (itemRect.width / 2)
  grid.scrollTo({ left: targetScrollLeft, behavior: 'smooth' })
}

// recompute dateGrid to be a sliding window centered at today + offset
const gridStart = computed(() => dayjs().add(windowOffset.value, 'day').subtract(Math.floor(windowSize.value / 2), 'day'))
const gridEnd = computed(() => dayjs().add(windowOffset.value, 'day').add(Math.ceil(windowSize.value / 2) - 1, 'day'))
const dateGrid = computed(() => {
  const arr: string[] = []
  let ptr = gridStart.value
  while (ptr.isBefore(gridEnd.value) || ptr.isSame(gridEnd.value, 'day')) {
    arr.push(ptr.format('YYYYMMDD'))
    ptr = ptr.add(1, 'day')
  }
  return arr
})

// (dateGrid is computed above as a sliding window)

const isFuture = (d: string) => d > dayjs().format('YYYYMMDD')
const isTodayStr = (d: string) => d === dayjs().format('YYYYMMDD')

const onGridDateClick = (d: string) => {
  if (isTodayStr(d)) {
    ElMessage.info('今日开市未结束，无数据')
    return
  }
  if (isFuture(d)) {
    ElMessage.info(`${dayjs(d, 'YYYYMMDD').format('YYYY-MM-DD')} 还未开市`)
    return
  }
  // 若为休市（tradeDates 不包含），提示休市信息
  if (!tradeDates.value.has(d)) {
    ElMessage.info(`${dayjs(d, 'YYYYMMDD').format('YYYY-MM-DD')} 休市`)
    return
  }
  queryDate.value = d
  fetchSummaryData()
}

</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.actual-date-tip {
  font-size: 14px;
  color: #909399;
  display: flex;
  align-items: center;
}
.actual-date-tip .el-icon {
  margin-left: 5px;
  cursor: pointer;
}

.date-grid {
  display: flex;
  flex-wrap: nowrap;
  gap: 6px;
  margin: 12px 0 18px 0;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  padding-bottom: 6px;
}
.date-cell {
  width: 64px;
  height: 36px;
  display:flex;
  align-items:center;
  justify-content:center;
  border-radius:4px;
  background: #f5f7fa;
  cursor: default;
  color: #606266;
  font-size: 12px;
}
.date-cell.selectable {
  cursor: pointer;
  background: #ffffff;
  border: 1px solid #ebeef5;
}
.date-cell.today {
  background: #fff7cc;
  border: 1px dashed #ffd666;
}
.date-cell.future {
  background: #f0f9ff;
  color: #409eff;
}
.date-cell.holiday {
  background: #fff0f0;
  color: #f56c6c;
}
.date-label { font-weight: 500 }
</style>
