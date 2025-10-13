import { defineStore } from 'pinia'
import request from '@/utils/request'

interface User {
  username: string;
  avatar: string | null;
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null as User | null
  }),
  actions: {
    async login(credentials) {
      const response = await request.post('/auth/login', credentials)
      // `request` helper returns data directly; but be defensive if it returns AxiosResponse
      let token: string | null = null
      if (response && typeof response === 'object') {
        if ('access_token' in response && typeof response.access_token === 'string') {
          token = response.access_token as string
        } else if ('data' in response && response.data && typeof response.data.access_token === 'string') {
          token = response.data.access_token as string
        }
      }
      this.token = token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
      await this.fetchUser()
    },
    async register(credentials) {
      await request.post('/auth/register', credentials)
    },
    async fetchUser() {
      if (!this.token) return
      try {
        const response = await request.get('/users/me')
        // request returns data directly; be defensive and accept wrapped AxiosResponse as well
        if (response && typeof response === 'object') {
          if ('username' in response) {
            this.user = response as any
          } else if ('data' in response && response.data) {
            this.user = response.data as any
          }
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
        this.logout() // 获取失败，可能token已失效
      }
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    }
  }
})
