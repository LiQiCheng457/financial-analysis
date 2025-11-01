<template>
  <div class="company-kline-wrapper">
    <div class="kline-header">
      <h3 class="kline-title">
        <span class="icon">📈</span>
        {{ stockCode }} 股票走势
      </h3>
      <div class="kline-controls">
        <el-radio-group v-model="period" size="small" @change="loadData">
          <el-radio-button label="day">日线</el-radio-button>
          <el-radio-button label="week">周线</el-radio-button>
          <el-radio-button label="month">月线</el-radio-button>
        </el-radio-group>
        <el-button size="small" @click="loadData" :loading="loading" :icon="Refresh" class="refresh-btn">
          刷新
        </el-button>
      </div>
    </div>
    
    <!-- 日期范围选择器 -->
    <div class="date-range-selector">
      <el-date-picker
        v-model="dateRange"
        type="daterange"
        range-separator="至"
        start-placeholder="开始日期"
        end-placeholder="结束日期"
        size="small"
        :shortcuts="dateShortcuts"
        @change="onDateRangeChange"
        style="width: 100%; max-width: 400px"
      />
      <el-button size="small" type="primary" @click="applyDateRange" :loading="loading" style="margin-left: 12px">
        查询
      </el-button>
      <el-button size="small" @click="resetDateRange" style="margin-left: 8px">
        重置
      </el-button>
    </div>
    
    <el-skeleton :rows="8" animated v-if="loading && !records.length" />
    <el-alert v-if="error" :title="error" type="error" show-icon :closable="false" style="margin: 12px 0" />
    
    <div v-if="records.length > 0" class="chart-container">
      <OHLCVChart ref="chartRef" :data="records" :period="period" @visible-range="onVisibleRange" />
      <div class="chart-info">
        <span>数据范围: {{ dataRange }}</span>
        <span style="margin-left: 16px">当前可见: {{ visibleStart }} ~ {{ visibleEnd }}</span>
      </div>
    </div>
    
    <el-empty v-if="!loading && !error && records.length === 0" description="暂无K线数据" />
  </div>
</template>

<script setup lang="ts">
import { ref, watch, computed, onMounted, nextTick } from 'vue'
import { Refresh } from '@element-plus/icons-vue'
import OHLCVChart from '@/components/OHLCVChart.vue'
import { getStockHistory } from '@/api/stock'

const props = defineProps<{
  stockCode: string
  autoLoad?: boolean
}>()

const period = ref<'day' | 'week' | 'month'>('day')
const records = ref<any[]>([])
const loading = ref(false)
const error = ref('')
const visibleStart = ref('')
const visibleEnd = ref('')
const chartRef = ref<any>(null)
const dateRange = ref<[Date, Date] | null>(null)

// 日期快捷选项
const dateShortcuts = [
  {
    text: '最近一周',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    }
  },
  {
    text: '最近一个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
      return [start, end]
    }
  },
  {
    text: '最近三个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
      return [start, end]
    }
  },
  {
    text: '最近半年',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 180)
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

const dataRange = computed(() => {
  if (!records.value.length) return '-'
  const dates = records.value.map(r => r['日期']).sort()
  return `${dates[0]} ~ ${dates[dates.length - 1]}`
})

async function loadData() {
  if (!props.stockCode) return
  
  loading.value = true
  error.value = ''
  
  try {
    let start: Date, end: Date
    
    // 如果有选择日期范围，使用选择的范围；否则默认最近一年
    if (dateRange.value && dateRange.value.length === 2) {
      start = dateRange.value[0]
      end = dateRange.value[1]
    } else {
      end = new Date()
      start = new Date()
      start.setFullYear(start.getFullYear() - 1)
    }
    
    const fmt = (d: Date) => 
      `${d.getFullYear()}${String(d.getMonth() + 1).padStart(2, '0')}${String(d.getDate()).padStart(2, '0')}`
    
    const resp: any = await getStockHistory({
      code: props.stockCode,
      start_date: fmt(start),
      end_date: fmt(end),
      source: 'eastmoney'
    })
    
    records.value = Array.isArray(resp) ? resp : []
    
    if (records.value.length === 0) {
      error.value = '未获取到K线数据，请检查股票代码或日期范围'
    } else {
      // 等待 DOM 更新后触发图表 resize
      await nextTick()
      setTimeout(() => {
        if (chartRef.value?.resize) {
          chartRef.value.resize()
        }
      }, 100)
    }
  } catch (e: any) {
    error.value = e.response?.data?.detail || e.message || '加载K线数据失败'
    console.error('加载K线数据失败:', e)
  } finally {
    loading.value = false
  }
}

function onDateRangeChange() {
  // 日期范围改变时可以做一些验证
}

function applyDateRange() {
  if (!dateRange.value || dateRange.value.length !== 2) {
    error.value = '请选择有效的日期范围'
    return
  }
  loadData()
}

function resetDateRange() {
  dateRange.value = null
  loadData()
}

function onVisibleRange(payload: any) {
  visibleStart.value = payload.startDateRaw || payload.startDate || ''
  visibleEnd.value = payload.endDateRaw || payload.endDate || ''
}

// 监听股票代码变化
watch(() => props.stockCode, (newCode) => {
  if (newCode) {
    loadData()
  }
}, { immediate: true })

// 可选的自动加载
onMounted(() => {
  if (props.autoLoad !== false && props.stockCode) {
    loadData()
  }
})

// 暴露给父组件的方法
defineExpose({
  loadData,
  setPeriod: (p: 'day' | 'week' | 'month') => { period.value = p }
})
</script>

<style scoped>
.company-kline-wrapper {
  background: #ffffff;
  border-radius: 8px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  width: 100%;
  overflow: hidden;
}

.kline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e4e7ed;
  flex-wrap: wrap;
  gap: 12px;
}

.kline-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
}

.kline-title .icon {
  font-size: 20px;
}

.kline-controls {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.chart-container {
  margin-top: 16px;
  width: 100%;
  min-height: 550px;
  position: relative;
}

.date-range-selector {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 12px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 6px;
}

.date-range-selector :deep(.el-date-editor) {
  max-width: 100%;
}

.refresh-btn {
  flex-shrink: 0;
}

.chart-container :deep(.ohlcv-chart) {
  width: 100% !important;
  height: 520px !important;
}

.chart-info {
  margin-top: 12px;
  padding: 8px 12px;
  background: #f5f7fa;
  border-radius: 4px;
  font-size: 13px;
  color: #606266;
  display: flex;
  justify-content: space-between;
}
</style>
