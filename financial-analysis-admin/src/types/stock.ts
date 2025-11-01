/**
 * 股票相关类型定义
 */

// 股票基本信息
export interface StockInfo {
  stock_code: string
  stock_name: string
  market?: string
  industry?: string
  list_date?: string
}

// 股票搜索结果
export interface StockSearchResult {
  code: string
  name: string
  market?: string
  pinyin?: string
}

// 股票历史数据
export interface StockHistoryData {
  date: string
  open: number
  high: number
  low: number
  close: number
  volume: number
  amount?: number
  turnover_rate?: number
  amplitude?: number
}

// 技术指标数据
export interface TechnicalIndicator {
  date: string
  [key: string]: number | string
}

// 技术信号
export interface TechnicalSignal {
  type: string
  name: string
  signal: 'buy' | 'sell' | 'hold' | 'neutral'
  strength: number
  description: string
  date?: string
}

// 交易建议
export interface TradingAdvice {
  overall_signal: 'buy' | 'sell' | 'hold' | 'neutral'
  confidence: number
  summary: string
  reasons: string[]
}

// 公司概况
export interface CompanyProfile {
  stock_code?: string
  company_name?: string
  industry?: string
  registered_capital?: string
  legal_representative?: string
  business_scope?: string
  shareholdings?: Shareholding[]
  issuance?: IssuanceInfo[]
}

// 股东信息
export interface Shareholding {
  shareholder_name: string
  shareholding_ratio: string
  shareholding_amount?: string
}

// 发行信息
export interface IssuanceInfo {
  issue_date: string
  issue_price: string
  issue_amount: string
}
