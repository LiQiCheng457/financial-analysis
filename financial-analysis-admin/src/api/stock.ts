import request from '@/utils/request'
import type {
  StockInfo,
  StockSearchResult,
  StockHistoryData,
  TechnicalIndicator,
  TechnicalSignal,
  TradingAdvice,
  CompanyProfile
} from '@/types'

/**
 * 获取所有交易日
 */
export const getTradeDates = () => {
  return request<string[]>({
    url: '/stocks/trade_dates',
    method: 'get'
  })
}

/**
 * 获取上交所每日概况
 * @param date 日期 (YYYYMMDD)
 */
export const getSseDailySummary = (date: string) => {
  return request({
    url: '/stocks/sse_daily_summary',
    method: 'get',
    params: { date }
  })
}

/**
 * 获取股票历史数据
 * @param params 查询参数
 * @param params.code 股票代码
 * @param params.start_date 开始日期 (YYYYMMDD)
 * @param params.end_date 结束日期 (YYYYMMDD)
 * @param params.adjust 复权类型: '' (不复权), 'qfq' (前复权), 'hfq' (后复权)
 * @param params.source 数据源: 'eastmoney' | 'sina' | 'tencent'
 */
export interface GetStockHistoryParams {
  code: string
  start_date?: string
  end_date?: string
  adjust?: '' | 'qfq' | 'hfq'
  source?: 'eastmoney' | 'sina' | 'tencent'
}

export const getStockHistory = (params: GetStockHistoryParams) => {
  return request<StockHistoryData[]>({
    url: '/stocks/history',
    method: 'get',
    params
  })
}

/**
 * 搜索股票 (自动补全)
 * @param q 搜索关键词
 * @param limit 返回数量限制
 */
export const searchStocks = (q: string, limit = 20) => {
  return request<StockSearchResult[]>({
    url: '/stocks/search',
    method: 'get',
    params: { q, limit }
  })
}

/**
 * 获取公司概况
 * @param q 股票代码或名称
 */
export const getCompanyProfile = async (q: string) => {
  const qs: string[] = []
  const q0 = String(q || '').trim()

  if (!q0) {
    return request<CompanyProfile>({
      url: '/stocks/company_profile',
      method: 'get',
      params: { q: q0 }
    })
  }

  qs.push(q0)
  // 尝试归一化变体以提高命中率
  const last6 = q0.slice(-6)
  if (/^\d{6}$/.test(last6) && last6 !== q0) qs.push(last6)
  if (/^\d{6}$/.test(q0)) {
    qs.push('sh' + q0)
    qs.push('sz' + q0)
  }

  // 去重并尝试
  const tried = new Set<string>()
  for (const tq of qs) {
    if (!tq || tried.has(tq)) continue
    tried.add(tq)

    try {
      const res = await request<CompanyProfile>({
        url: '/stocks/company_profile',
        method: 'get',
        params: { q: tq }
      }) as CompanyProfile

      // 如果响应包含有效数据
      if (res && (res.company_name || res.stock_code)) {
        // 确保数组字段存在
        res.shareholdings = Array.isArray(res.shareholdings) ? res.shareholdings : []
        res.issuance = Array.isArray(res.issuance) ? res.issuance : []
        return res
      }
    } catch {
      // 继续尝试下一个变体
      continue
    }
  }

  // 最后使用原始查询
  const final = await request<CompanyProfile>({
    url: '/stocks/company_profile',
    method: 'get',
    params: { q: q0 }
  }) as CompanyProfile

  if (final) {
    final.shareholdings = Array.isArray(final.shareholdings) ? final.shareholdings : []
    final.issuance = Array.isArray(final.issuance) ? final.issuance : []
  }

  return final
}

/**
 * 按行业等条件搜索公司列表 (分页)
 * @param q 搜索关键词
 * @param page 页码
 * @param page_size 每页数量
 * @param industry 行业过滤
 */
export interface SearchCompaniesParams {
  q: string
  page?: number
  page_size?: number
  industry?: string
  industry_match_mode?: 'any' | 'all'
  search_mode?: 'fuzzy' | 'exact'
  min_capital?: number
  max_capital?: number
  region?: string
  security_types?: string
}

export const searchCompanies = (params: SearchCompaniesParams) => {
  const requestParams: any = { ...params }

  return request<StockInfo[]>({
    url: '/stocks/search_companies',
    method: 'get',
    params: requestParams
  })
}

/**
 * 获取技术指标数据
 * @param params 查询参数
 */
export interface GetTechnicalIndicatorsParams {
  code: string
  start_date?: string
  end_date?: string
  indicators?: string
  source?: string
}

export const getTechnicalIndicators = (params: GetTechnicalIndicatorsParams) => {
  return request<TechnicalIndicator[]>({
    url: '/stocks/technical_indicators',
    method: 'get',
    params
  })
}

/**
 * 获取技术指标配置
 */
export const getIndicatorConfig = () => {
  return request({
    url: '/stocks/indicator_config',
    method: 'get'
  })
}

/**
 * 获取技术信号检测结果
 * @param params 查询参数
 */
export interface GetTechnicalSignalsParams {
  code: string
  start_date?: string
  end_date?: string
  lookback?: number
  source?: string
}

export interface TechnicalSignalsResponse {
  signals: TechnicalSignal[]
  advice: TradingAdvice
}

export const getTechnicalSignals = (params: GetTechnicalSignalsParams) => {
  return request<TechnicalSignalsResponse>({
    url: '/stocks/technical_signals',
    method: 'get',
    params
  })
}
