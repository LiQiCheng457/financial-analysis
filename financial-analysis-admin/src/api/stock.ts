import request from '@/utils/request'
import axios from 'axios'

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
  // Prefer direct backend call (bypass vite proxy) to avoid dev-server 404 when proxy isn't active.
  const base = 'http://127.0.0.1:8000/api'
  try {
    return axios.get(`${base}/stocks/search`, { params: { q, limit } }).then(r => r.data)
  } catch (e) {
    // if direct call fails synchronously, fall back to proxied request
  }

  // fallback to proxied request
  return request({
    url: '/stocks/search',
    method: 'get',
    params: { q, limit }
  })
}

