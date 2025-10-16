/**
 * 搜索功能 Composable
 * 提供通用的搜索逻辑、防抖、加载状态管理
 */
import { ref, Ref } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import { ElMessage } from 'element-plus'

export interface SearchOptions<T> {
  searchFn: (query: string) => Promise<T[]>
  debounceTime?: number
  minLength?: number
  onSuccess?: (results: T[]) => void
  onError?: (error: Error) => void
}

export function useSearch<T = any>(options: SearchOptions<T>) {
  const {
    searchFn,
    debounceTime = 300,
    minLength = 1,
    onSuccess,
    onError
  } = options

  const query = ref('')
  const results: Ref<T[]> = ref([])
  const loading = ref(false)
  const error: Ref<Error | null> = ref(null)

  const search = useDebounceFn(async () => {
    // 验证查询长度
    if (query.value.trim().length < minLength) {
      results.value = []
      return
    }

    loading.value = true
    error.value = null

    try {
      const data = await searchFn(query.value.trim())
      results.value = data
      onSuccess?.(data)
    } catch (err) {
      error.value = err as Error
      results.value = []
      onError?.(err as Error)
      ElMessage.error('搜索失败，请重试')
    } finally {
      loading.value = false
    }
  }, debounceTime)

  const reset = () => {
    query.value = ''
    results.value = []
    error.value = null
    loading.value = false
  }

  return {
    query,
    results,
    loading,
    error,
    search,
    reset
  }
}
