/**
 * 分页功能 Composable
 * 提供通用的分页逻辑、页码管理、数据加载
 */
import { ref, computed, Ref } from 'vue'
import { ElMessage } from 'element-plus'

export interface PaginationOptions<T> {
  fetchFn: (page: number, pageSize: number) => Promise<{ data: T[]; total: number }>
  initialPage?: number
  initialPageSize?: number
  autoLoad?: boolean
  onSuccess?: (data: T[], total: number) => void
  onError?: (error: Error) => void
}

export function usePagination<T = any>(options: PaginationOptions<T>) {
  const {
    fetchFn,
    initialPage = 1,
    initialPageSize = 20,
    autoLoad = false,
    onSuccess,
    onError
  } = options

  const currentPage = ref(initialPage)
  const pageSize = ref(initialPageSize)
  const total = ref(0)
  const data: Ref<T[]> = ref([])
  const loading = ref(false)
  const error: Ref<Error | null> = ref(null)

  const totalPages = computed(() => Math.ceil(total.value / pageSize.value))
  const hasNextPage = computed(() => currentPage.value < totalPages.value)
  const hasPrevPage = computed(() => currentPage.value > 1)

  const loadData = async () => {
    loading.value = true
    error.value = null

    try {
      const result = await fetchFn(currentPage.value, pageSize.value)
      data.value = result.data
      total.value = result.total
      onSuccess?.(result.data, result.total)
    } catch (err) {
      error.value = err as Error
      data.value = []
      onError?.(err as Error)
      ElMessage.error('数据加载失败，请重试')
    } finally {
      loading.value = false
    }
  }

  const goToPage = async (page: number) => {
    if (page < 1 || page > totalPages.value) return
    currentPage.value = page
    await loadData()
  }

  const nextPage = async () => {
    if (hasNextPage.value) {
      await goToPage(currentPage.value + 1)
    }
  }

  const prevPage = async () => {
    if (hasPrevPage.value) {
      await goToPage(currentPage.value - 1)
    }
  }

  const changePageSize = async (newSize: number) => {
    pageSize.value = newSize
    currentPage.value = 1
    await loadData()
  }

  const refresh = async () => {
    await loadData()
  }

  const reset = () => {
    currentPage.value = initialPage
    pageSize.value = initialPageSize
    total.value = 0
    data.value = []
    error.value = null
  }

  // 自动加载
  if (autoLoad) {
    loadData()
  }

  return {
    // 状态
    currentPage,
    pageSize,
    total,
    totalPages,
    data,
    loading,
    error,
    hasNextPage,
    hasPrevPage,

    // 方法
    loadData,
    goToPage,
    nextPage,
    prevPage,
    changePageSize,
    refresh,
    reset
  }
}
