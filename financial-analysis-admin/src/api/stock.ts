import request from '@/utils/request'

// 获取所有交易日
export function getTradeDates() {
  return request({
    url: '/stocks/trade_dates',
    method: 'get',
  })
}

// 获取上交所每日概况
export function getSseDailySummary(date: string) {
  return request({
    url: '/stocks/sse_daily_summary',
    method: 'get',
    params: { date }
  })
}

// 兼容旧的 StockHistory 视图导入：若后端未实现 /stocks/history 则会返回 404
export function getStockHistory(params: { code: string; start_date?: string; end_date?: string; adjust?: string; source?: string }) {
  // adjust: '' (不复权), 'qfq' (前复权), 'hfq' (后复权)
  // source: 'eastmoney' | 'sina' | 'tencent'
  return request({
    url: '/stocks/history',
    method: 'get',
    params,
  })
}


// 搜索股票建议（用于 autocomplete）
export function searchStocks(q: string, limit: number = 20) {
  return request({
    url: '/stocks/search',
    method: 'get',
    params: { q, limit }
  })
}

// 获取公司概况
export function getCompanyProfile(q: string) {
  return request({
    url: '/stocks/company_profile',
    method: 'get',
    params: { q }
  })
}

// 按行业等条件搜索公司列表（分页）
export function searchCompanies(q: string, page: number = 1, page_size: number = 50, industry?: string) {
  const params: any = { q, page, page_size }
  if (industry) params.industry = industry
  return request({
    url: '/stocks/search_companies',
    method: 'get',
    params
  })
}

