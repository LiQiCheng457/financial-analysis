import axios, { type AxiosInstance, type AxiosResponse } from 'axios'
import { useAuthStore } from '@/store/auth'
import { ElMessage } from 'element-plus'
import type { ApiResponse } from '@/types'

// 创建 axios 实例
const service: AxiosInstance = axios.create({
  baseURL: '/api', // Vite proxy 会将 /api 转发到后端
  timeout: 10000 // 请求超时时间
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      // 让每个请求携带 token
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    // 直接返回 data
    return response.data as any
  },
  (error) => {
    console.error('响应错误:', error)

    if (error.response) {
      // 后端返回的业务错误
      const data = error.response.data
      ElMessage({
        message: data.detail || '服务器内部错误',
        type: 'error',
        duration: 5000
      })

      // 如果是 401 Unauthorized，token 可能失效，登出
      if (error.response.status === 401) {
        const authStore = useAuthStore()
        authStore.logout()
      }
    } else {
      // 网络错误等
      ElMessage({
        message: '网络错误，请检查您的连接',
        type: 'error',
        duration: 5000
      })
    }

    return Promise.reject(error)
  }
)

export default service
