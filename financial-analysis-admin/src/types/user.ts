/**
 * 用户相关类型定义
 */

// 用户角色枚举
export enum UserRole {
  ADMIN = 'admin',
  USER = 'user'
}

// 用户信息
export interface User {
  id?: number
  username: string
  email?: string
  avatar?: string | null
  role: UserRole
  created_at?: string
  updated_at?: string
}

// 登录凭证
export interface LoginCredentials {
  username: string
  password: string
}

// 注册信息
export interface RegisterInfo {
  username: string
  password: string
  email?: string
}

// 登录响应
export interface LoginResponse {
  access_token: string
  token_type: string
  user?: User
}
