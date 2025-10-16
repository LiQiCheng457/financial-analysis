import type { MenuItem } from '@/types/menu'

const menu: MenuItem[] = [
  {
    key: 'home',
    title: '主页',
    icon: 'home',
    path: '/',
  },
  {
    key: 'market',
    title: '行情中心',
    icon: 'document',
    children: [
      { key: 'market-summary', title: '每日概况', path: '/market-summary' },
      { key: 'stock-history', title: '历史行情数据', path: '/stock-history' },
      { key: 'market-kline', title: 'K线图', path: '/market/kline' },
      { key: 'market-timeseries', title: '分时图', path: '/market/timeseries' },
      { key: 'market-snapshot', title: '公司概括', path: '/market/snapshot' },
    ],
  },
  {
    key: 'watchlist',
    title: '自选股',
    icon: 'bell',
    children: [
      { key: 'watchlist-crud', title: '增删改查', path: '/watchlist/crud' },
      { key: 'watchlist-groups', title: '分组管理', path: '/watchlist/groups' },
      { key: 'watchlist-alerts', title: '涨跌提醒', path: '/watchlist/alerts' },
    ],
  },
  {
    key: 'picker',
    title: '选股器',
    icon: 'document',
    children: [
      { key: 'picker-filter', title: '条件筛选', path: '/picker/filter' },
      { key: 'picker-backtest', title: '策略回测', path: '/picker/backtest' },
      { key: 'picker-hot', title: '热门策略', path: '/picker/hot' },
    ],
  },
  {
    key: 'finance',
    title: '财务分析',
    icon: 'document',
    children: [
      { key: 'finance-reports', title: '财务报表', path: '/finance/reports' },
      { key: 'finance-metrics', title: '关键指标', path: '/finance/metrics' },
      { key: 'finance-peer', title: '同业对比', path: '/finance/peer' },
    ],
  },
  {
    key: 'news',
    title: '新闻报告',
    icon: 'document',
    children: [
      { key: 'news-realtime', title: '实时新闻', path: '/news/realtime' },
      { key: 'news-announcements', title: '公司公告', path: '/news/announcements' },
    ],
  },
  {
    key: 'user',
    title: '用户系统',
    icon: 'user',
    children: [
      { key: 'user-profile', title: '个人中心', path: '/user/profile' },
      { key: 'user-permissions', title: '权限管理', path: '/user/permissions' },
    ],
  },
]

export default menu
