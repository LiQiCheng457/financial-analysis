<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>历史行情数据</span>
        </div>
      </template>

      <el-form :inline="true" @submit.prevent="fetchStockData">
        <el-form-item label="股票搜索">
          <StockSearch 
            v-model="stockCode"
            @select="handleStockSelect"
            placeholder="输入代码或名称搜索"
            :show-favorites="true"
            :show-history="true"
            style="width: 200px"
          />
        </el-form-item>
        <el-form-item v-if="selectedStockName" label="">
          <el-tag type="info">{{ selectedStockName }}</el-tag>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYYMMDD"
            clearable
          />
        </el-form-item>
        <!-- 调整(复权)选项已移除：数据库中存储的是不复权数据 -->
        <!-- 数据源选项已移除：历史行情将从后端数据库获取 -->
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading">查询</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 视图切换和统计信息 -->
      <div v-if="stockData.length > 0" class="toolbar">
        <el-radio-group v-model="viewMode" size="default">
          <el-radio-button label="table">
            <el-icon><List /></el-icon>
            表格视图
          </el-radio-button>
          <el-radio-button label="chart">
            <el-icon><TrendCharts /></el-icon>
            图表视图
          </el-radio-button>
          <el-radio-button label="both">
            <el-icon><Grid /></el-icon>
            综合视图
          </el-radio-button>
        </el-radio-group>

        <!-- 区间统计卡片 -->
        <div class="stats-summary">
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <span class="stat-label">区间涨跌</span>
              <span class="stat-value" :class="rangeChangeClass">{{ rangeChange }}</span>
            </div>
          </el-card>
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <span class="stat-label">最高价</span>
              <span class="stat-value high">{{ maxPrice }}</span>
            </div>
          </el-card>
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <span class="stat-label">最低价</span>
              <span class="stat-value low">{{ minPrice }}</span>
            </div>
          </el-card>
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <span class="stat-label">平均价</span>
              <span class="stat-value">{{ avgPrice }}</span>
            </div>
          </el-card>
          <el-card shadow="hover" class="stat-card">
            <div class="stat-content">
              <span class="stat-label">波动率</span>
              <span class="stat-value">{{ volatility }}</span>
            </div>
          </el-card>
        </div>
      </div>

      <!-- 图表视图 -->
      <div v-if="(viewMode === 'chart' || viewMode === 'both') && stockData.length > 0" class="chart-container">
        <TechnicalChart 
            :data="chartFormattedData" 
            :defaultIndicators="['MA', 'VOL']"
          />
      </div>

      <!-- 表格视图 -->
      <el-table 
        v-if="(viewMode === 'table' || viewMode === 'both') && stockData.length > 0"
        :data="stockData" 
        v-loading="loading" 
        border 
        stripe 
        :height="viewMode === 'both' ? 400 : 600"
        :row-class-name="tableRowClassName"
        @row-click="handleRowClick"
      >
        <el-table-column prop="日期" label="日期" width="120"></el-table-column>
        <el-table-column prop="开盘" label="开盘"></el-table-column>
        <el-table-column prop="收盘" label="收盘"></el-table-column>
        <el-table-column prop="最高" label="最高"></el-table-column>
        <el-table-column prop="最低" label="最低"></el-table-column>
        <el-table-column prop="成交量" label="成交量"></el-table-column>
        <el-table-column prop="成交额" label="成交额"></el-table-column>
        <el-table-column prop="振幅" label="振幅"></el-table-column>
        <el-table-column prop="涨跌幅" label="涨跌幅"></el-table-column>
        <el-table-column prop="涨跌额" label="涨跌额"></el-table-column>
        <el-table-column prop="换手率" label="换手率"></el-table-column>
      </el-table>

    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { getStockHistory, getTechnicalIndicators } from '@/api/stock'
import { ElMessage } from 'element-plus'
import { List, TrendCharts, Grid } from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import StockSearch from '@/components/business/StockSearch.vue'
import TechnicalChart from '@/components/TechnicalChart.vue'

const stockCode = ref('000001') // 默认查询平安银行
const dateRange = ref<[string, string] | null>(null)
// Type for a single record returned by backend
interface StockRecord {
  日期?: string
  股票代码?: string
  开盘?: number | null
  收盘?: number | null
  最高?: number | null
  最低?: number | null
  成交量?: number | null
  成交额?: number | null
  振幅?: number | null
  涨跌幅?: number | null
  涨跌额?: number | null
  换手率?: number | null
  [key: string]: any
}

const stockData = ref<StockRecord[]>([])
const loading = ref(false)
const useMock = ref(false)
const viewMode = ref<'table' | 'chart' | 'both'>('both')
const selectedStockName = ref('')
const highlightedRowIndex = ref<number | null>(null)

// 处理股票选择
const handleStockSelect = (stock: any) => {
  stockCode.value = stock.code
  selectedStockName.value = stock.name
}

// 重置表单
const resetForm = () => {
  stockCode.value = '000001'
  selectedStockName.value = ''
  dateRange.value = null
  // 数据以不复权的原始值为准，复权选项已从界面移除
  stockData.value = []
}

// 格式化图表数据
const chartFormattedData = computed(() => {
  if (!stockData.value || stockData.value.length === 0) return []
  
  // ✅ 直接返回完整数据,包含所有技术指标字段(MA5/MA10/DIF/DEA/MACD/K/D/J/RSI6等)
  return stockData.value as any[]
})

// 区间统计计算
const rangeChange = computed(() => {
  if (stockData.value.length < 2) return '-'
  const first = stockData.value[0].收盘
  const last = stockData.value[stockData.value.length - 1].收盘
  if (!first || !last) return '-'
  const change = ((last - first) / first * 100).toFixed(2)
  const changeNum = parseFloat(change)
  return `${changeNum > 0 ? '+' : ''}${change}%`
})

const rangeChangeClass = computed(() => {
  if (stockData.value.length < 2) return ''
  const first = stockData.value[0].收盘
  const last = stockData.value[stockData.value.length - 1].收盘
  if (!first || !last) return ''
  return last > first ? 'price-up' : last < first ? 'price-down' : ''
})

const maxPrice = computed(() => {
  if (stockData.value.length === 0) return '-'
  const max = Math.max(...stockData.value.map(item => item.最高 || 0))
  return max > 0 ? max.toFixed(2) : '-'
})

const minPrice = computed(() => {
  if (stockData.value.length === 0) return '-'
  const min = Math.min(...stockData.value.filter(item => item.最低 && item.最低 > 0).map(item => item.最低 || Infinity))
  return min < Infinity ? min.toFixed(2) : '-'
})

const avgPrice = computed(() => {
  if (stockData.value.length === 0) return '-'
  const validPrices = stockData.value.filter(item => item.收盘 && item.收盘 > 0)
  if (validPrices.length === 0) return '-'
  const sum = validPrices.reduce((acc, item) => acc + (item.收盘 || 0), 0)
  return (sum / validPrices.length).toFixed(2)
})

const volatility = computed(() => {
  if (stockData.value.length < 2) return '-'
  const changes = stockData.value.filter(item => item.涨跌幅 !== null && item.涨跌幅 !== undefined)
    .map(item => Math.abs(item.涨跌幅 || 0))
  if (changes.length === 0) return '-'
  const avgChange = changes.reduce((acc, val) => acc + val, 0) / changes.length
  return `${avgChange.toFixed(2)}%`
})

// 表格行类名
const tableRowClassName = ({ rowIndex }: { rowIndex: number }) => {
  if (rowIndex === highlightedRowIndex.value) {
    return 'highlighted-row'
  }
  return ''
}

// 处理行点击
const handleRowClick = (row: StockRecord, _column: any, _event: Event) => {
  const index = stockData.value.findIndex(item => item.日期 === row.日期)
  highlightedRowIndex.value = index
}

const mockData: StockRecord[] = [
  {
    日期: '2023-12-27',
    股票代码: '000001',
    开盘: 9.1,
    收盘: 9.12,
    最高: 9.13,
    最低: 9.02,
    成交量: 641534,
    成交额: 582036660.68,
    振幅: 1.21,
    涨跌幅: 0.22,
    涨跌额: 0.02,
    换手率: 0.33
  },
  {
    日期: '2023-12-28',
    股票代码: '000001',
    开盘: 9.11,
    收盘: 9.45,
    最高: 9.47,
    最低: 9.08,
    成交量: 1661592,
    成交额: 1550256590.59,
    振幅: 4.28,
    涨跌幅: 3.62,
    涨跌额: 0.33,
    换手率: 0.86
  }
  ,
  {
    日期: '2023-12-29',
    股票代码: '000001',
    开盘: 9.42,
    收盘: 9.39,
    最高: 9.48,
    最低: 9.35,
    成交量: 853853,
    成交额: 803196743.82,
    振幅: 1.38,
    涨跌幅: -0.63,
    涨跌额: -0.06,
    换手率: 0.44
  }
]

const fetchStockData = async () => {
  if (!stockCode.value) {
    ElMessage.warning('请输入股票代码')
    return
  }
  loading.value = true
  try {
    if (useMock.value) {
      stockData.value = mockData
      return
    }

    const params = {
      code: stockCode.value,
      start_date: dateRange.value ? dateRange.value[0] : undefined,
      end_date: dateRange.value ? dateRange.value[1] : undefined
    }
    const data = await getStockHistory(params)
    if (Array.isArray(data)) {
      stockData.value = data
    } else if (data && Array.isArray((data as any).data)) {
      stockData.value = (data as any).data
    } else if (data && (data as any).error) {
      stockData.value = []
      ElMessage.error((data as any).error)
    } else {
      stockData.value = []
      ElMessage.error('未能获取到数据，请检查查询条件或后端状态')
    }
    
    // 请求并合并技术指标到 stockData 中
    try {
      const tiParams: any = {
        code: stockCode.value,
        start_date: dateRange.value ? dateRange.value[0] : undefined,
        end_date: dateRange.value ? dateRange.value[1] : undefined,
        indicators: 'MA,MACD,KDJ,RSI,BOLL,VOL'
      }
      
      const tiRes: any = await getTechnicalIndicators(tiParams)
      
      // axios拦截器已经返回了response.data,所以tiRes就是 { status: 'ok', data: [...] }
      if (tiRes && tiRes.status === 'ok' && Array.isArray(tiRes.data)) {
        const tiData = tiRes.data
        
        if (tiData.length > 0 && stockData.value.length > 0) {
          // 将技术指标按日期合并到 stockData
          const tiMap = new Map<string, any>()
          tiData.forEach((row: any) => {
            const dateKey = row.日期 || row.date || row.trade_date || row.tradeDate || ''
            if (dateKey) {
              tiMap.set(dateKey, row)
            }
          })
          
          stockData.value = stockData.value.map(row => {
            const key = (row.日期 || '') as string
            const extra = tiMap.get(key) || {}
            return { ...row, ...extra }
          })
        }
      }
    } catch (e) {
      // 技术指标请求失败不阻塞主流程
      console.error('获取技术指标失败:', e)
    }
  } catch (error) {
    stockData.value = []
    ElMessage.error('请求失败，请检查网络或联系管理员')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 组件挂载后自动加载一次默认股票的数据（最近一年）
onMounted(() => {
  const today = dayjs()
  const oneYearAgo = today.subtract(1, 'year')
  dateRange.value = [oneYearAgo.format('YYYYMMDD'), today.format('YYYYMMDD')]
  fetchStockData()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toolbar {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin: 20px 0;
}

.stats-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
}

.stat-card {
  cursor: default;
}

.stat-card :deep(.el-card__body) {
  padding: 16px;
}

.stat-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.stat-label {
  font-size: 13px;
  color: #909399;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.stat-value.price-up {
  color: #ef232a;
}

.stat-value.price-down {
  color: #14b143;
}

.stat-value.high {
  color: #ef232a;
}

.stat-value.low {
  color: #14b143;
}

.chart-container {
  margin: 20px 0;
}

:deep(.highlighted-row) {
  background-color: #ecf5ff !important;
}

:deep(.highlighted-row:hover) {
  background-color: #d9ecff !important;
}
</style>
