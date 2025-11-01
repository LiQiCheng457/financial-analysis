import { defineStore } from 'pinia'
import request from '@/utils/request'
import type { User, LoginCredentials, RegisterInfo, LoginResponse } from '@/types'
import { UserRole } from '@/types'

interface AuthState {
  token: string | null
  user: User | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('token') || null,
    user: null
  }),

  getters: {
    /**
     * 判断是否为管理员
     */
    isAdmin: (state): boolean => state.user?.role === UserRole.ADMIN,

    /**
     * 判断是否已登录
     */
    isAuthenticated: (state): boolean => !!state.token,

    /**
     * 获取用户角色显示名称
     */
    roleDisplayName: (state): string => {
      if (!state.user) return '未登录'
      return state.user.role === UserRole.ADMIN ? '管理员' : '普通用户'
    }
  },

  actions: {
    /**
     * 用户登录
     * @param credentials 登录凭证
     */
    async login (credentials: LoginCredentials) {
      const response = await request.post<LoginResponse>('/auth/login', credentials)

      // 提取 token
      let token: string | null = null
      if (response && typeof response === 'object') {
        if ('access_token' in response && typeof response.access_token === 'string') {
          token = response.access_token
        } else if ('data' in response && response.data && typeof response.data.access_token === 'string') {
          token = response.data.access_token
        }
      }

      this.token = token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }

      // 处理用户信息
      if (response && typeof response === 'object') {
        if ('user' in response && response.user) {
          this.user = response.user as User
          return
        } else if ('data' in response && response.data && response.data.user) {
          this.user = response.data.user as User
          return
        }
      }

      // 向后兼容：根据用户名临时识别角色（仅用于测试）
      const role = credentials.username === 'admin' ? UserRole.ADMIN : UserRole.USER
      this.user = {
        username: credentials.username,
        avatar: null,
        role
      }
    },

    /**
     * 用户注册
     * @param credentials 注册信息
     */
    async register (credentials: RegisterInfo) {
      await request.post('/auth/register', credentials)
    },

    /**
     * 获取当前用户信息
     */
    async fetchUser () {
      if (!this.token) return

      try {
        const response = await request.get<User>('/users/me') as any

        if (response && typeof response === 'object') {
          if ('username' in response && 'role' in response) {
            this.user = response as User
          } else if ('data' in response && response.data) {
            this.user = response.data as User
          }
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
        this.logout() // 获取失败，可能 token 已失效
      }
    },

    /**
     * 用户登出
     */
    logout () {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    }
  }
})
