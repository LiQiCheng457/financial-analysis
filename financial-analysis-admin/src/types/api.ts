/**
 * API 响应通用类型定义
 */

// API 响应基础接口
export interface ApiResponse<T = any> {
  code?: number
  message?: string
  data: T
  detail?: string
}

// 分页响应接口
export interface PageResponse<T = any> {
  items: T[]
  total: number
  page: number
  page_size: number
  pages?: number
}

// 通用列表响应
export interface ListResponse<T = any> {
  data: T[]
  total?: number
}

// 错误响应
export interface ErrorResponse {
  detail: string
  code?: number
  errors?: Record<string, string[]>
}
