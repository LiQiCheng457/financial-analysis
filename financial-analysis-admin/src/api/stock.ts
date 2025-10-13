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

