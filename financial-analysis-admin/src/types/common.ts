/**
 * 通用工具类型和常量
 */

// 日期范围类型
export type DateRange = [string, string] | null

// 排序方向
export type SortOrder = 'asc' | 'desc'

// 加载状态
export enum LoadingState {
  IDLE = 'idle',
  LOADING = 'loading',
  SUCCESS = 'success',
  ERROR = 'error'
}

// 分页参数
export interface PaginationParams {
  page: number
  page_size: number
}

// 排序参数
export interface SortParams {
  sort_by?: string
  order?: SortOrder
}

// 查询参数基类
export interface BaseQueryParams extends Partial<PaginationParams>, Partial<SortParams> {
  [key: string]: any
}
