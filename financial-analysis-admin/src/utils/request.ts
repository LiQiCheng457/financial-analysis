import axios from 'axios'
import { useAuthStore } from '@/store/auth'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const service = axios.create({
  baseURL: '/api', // Vite proxy 会将 /api 转发到 http://127.0.0.1:8000/api
  timeout: 10000 // 请求超时时间
})

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      // 让每个请求携带自定义 token
      config.headers['Authorization'] = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    // 对请求错误做些什么
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    // 直接返回 `response.data`
    return response.data
  },
  (error) => {
    console.error('响应错误: ', error)
    if (error.response) {
        // 后端返回的业务错误
        const data = error.response.data;
        ElMessage({
            message: data.detail || '服务器内部错误',
            type: 'error',
            duration: 5 * 1000
        })

        // 如果是 401 Unauthorized，可能是 token 失效，登出
        if (error.response.status === 401) {
            const authStore = useAuthStore();
            authStore.logout();
            // 可以选择跳转到登录页
            // router.push('/login');
        }
    } else {
        // 网络错误等
        ElMessage({
            message: '网络错误，请检查您的连接',
            type: 'error',
            duration: 5 * 1000
        })
    }
    return Promise.reject(error)
  }
)

export default service
