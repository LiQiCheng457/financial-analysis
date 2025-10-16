/**
 * 股票相关功能 Composable
 * 封装股票查询、实时行情、历史数据等逻辑
 */
import { ref, Ref } from 'vue'
import { 
  searchStocks, 
  getStockHistory,
  type StockSearchResult,
  type StockHistoryParams 
} from '@/api/stock'
import { ElMessage } from 'element-plus'

/**
 * 股票搜索
 */
export function useStockSearch() {
  const results: Ref<StockSearchResult[]> = ref([])
  const loading = ref(false)

  const search = async (query: string, limit = 20) => {
    if (!query.trim()) {
      results.value = []
      return
    }

    loading.value = true
    try {
      const response = await searchStocks(query, limit)
      results.value = response.data || []
    } catch (error) {
      console.error('股票搜索失败:', error)
      results.value = []
      ElMessage.error('股票搜索失败')
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    results.value = []
    loading.value = false
  }

  return {
    results,
    loading,
    search,
    reset
  }
}

/**
 * 股票历史数据
 */
export function useStockHistory() {
  const historyData = ref([])
  const loading = ref(false)
  const error: Ref<Error | null> = ref(null)

  const fetchHistory = async (params: StockHistoryParams) => {
    loading.value = true
    error.value = null

    try {
      const response = await getStockHistory(params)
      historyData.value = response.data || []
      return response.data
    } catch (err) {
      error.value = err as Error
      historyData.value = []
      ElMessage.error('获取历史数据失败')
      throw err
    } finally {
      loading.value = false
    }
  }

  const reset = () => {
    historyData.value = []
    error.value = null
    loading.value = false
  }

  return {
    historyData,
    loading,
    error,
    fetchHistory,
    reset
  }
}

/**
 * 股票实时行情（支持批量）
 */
export function useStockRealtime() {
  const realtimeData = ref<Record<string, any>>({})
  const loading = ref(false)
  const error: Ref<Error | null> = ref(null)

  const fetchRealtime = async (codes: string[]) => {
    if (!codes.length) return

    loading.value = true
    error.value = null

    try {
      // TODO: 实现批量获取实时行情接口
      // const response = await getStockRealtimeBatch(codes)
      // realtimeData.value = response.data
      ElMessage.info('实时行情功能开发中')
    } catch (err) {
      error.value = err as Error
      ElMessage.error('获取实时行情失败')
    } finally {
      loading.value = false
    }
  }

  const updatePrice = (code: string, price: number) => {
    if (realtimeData.value[code]) {
      realtimeData.value[code].price = price
    }
  }

  const reset = () => {
    realtimeData.value = {}
    error.value = null
    loading.value = false
  }

  return {
    realtimeData,
    loading,
    error,
    fetchRealtime,
    updatePrice,
    reset
  }
}
