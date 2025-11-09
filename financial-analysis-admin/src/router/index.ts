import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/layout/Layout.vue'
import LoginView from '../views/login/LoginView.vue'
import HomeView from '../views/home/HomeView.vue'
import { useAuthStore } from '@/store/auth'

import StockHistory from '@/views/stock/StockHistory.vue'

import MarketSummary from '@/views/market/MarketSummary.vue'
import Snapshot from '@/views/market/Snapshot.vue'
import TechnicalAnalysis from '@/views/market/TechnicalAnalysis.vue'
import ETFSpecial from '@/views/market/ETFSpecial.vue'

import WatchlistCrud from '@/views/watchlist/Crud.vue'
import WatchlistGroups from '@/views/watchlist/Groups.vue'
import WatchlistAlerts from '@/views/watchlist/Alerts.vue'

import PickerFilter from '@/views/picker/Filter.vue'
import PickerBacktest from '@/views/picker/Backtest.vue'
import PickerHot from '@/views/picker/Hot.vue'

import FinanceReports from '@/views/finance/Reports.vue'
import FinanceMetrics from '@/views/finance/Metrics.vue'
import FinancePeer from '@/views/finance/Peer.vue'

import NewsRealtime from '@/views/news/Realtime.vue'
import NewsAnnouncements from '@/views/news/Announcements.vue'

import IndustryRotation from '@/views/strategy/IndustryRotation.vue'

import UserProfile from '@/views/user/Profile.vue'
import UserPermissions from '@/views/user/Permissions.vue'
import AdminUsers from '@/views/admin/Users.vue'

const routes = [
  {
    path: '/',
    component: Layout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'home',
        component: HomeView,
      },
      {
        path: 'stock/history',
        name: 'stock-history',
        component: StockHistory,
      },
      {
        path: 'market/summary',
        name: 'market-summary',
        component: MarketSummary,
      },
      { path: 'market/snapshot', name: 'market-snapshot', component: Snapshot },
      { path: 'market/technical', name: 'market-technical', component: TechnicalAnalysis },
      { path: 'market/etf', name: 'market-etf', component: ETFSpecial },

      { path: 'watchlist/crud', name: 'watchlist-crud', component: WatchlistCrud },
      { path: 'watchlist/groups', name: 'watchlist-groups', component: WatchlistGroups },
      { path: 'watchlist/alerts', name: 'watchlist-alerts', component: WatchlistAlerts },

      { path: 'picker/filter', name: 'picker-filter', component: PickerFilter },
      { path: 'picker/backtest', name: 'picker-backtest', component: PickerBacktest },
      { path: 'picker/hot', name: 'picker-hot', component: PickerHot },

      { path: 'finance/reports', name: 'finance-reports', component: FinanceReports },
      { path: 'finance/metrics', name: 'finance-metrics', component: FinanceMetrics },
      { path: 'finance/peer', name: 'finance-peer', component: FinancePeer },

      { path: 'news/realtime', name: 'news-realtime', component: NewsRealtime },
      { path: 'news/announcements', name: 'news-announcements', component: NewsAnnouncements },

      { path: 'strategy/industry-rotation', name: 'strategy-industry-rotation', component: IndustryRotation },

      { path: 'user/profile', name: 'user-profile', component: UserProfile },
      { path: 'admin/users', name: 'admin-users', component: AdminUsers, meta: { requiresAdmin: true } },
      { path: 'user/permissions', name: 'user-permissions', component: UserPermissions, meta: { requiresAdmin: true } },
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = !!authStore.token

  // 检查目标路由或其任何匹配的父路由是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin)

  if (requiresAuth && !isAuthenticated) {
    // 如果目标路由需要认证但用户未登录，则重定向到登录页
    next({ name: 'login' })
  } else if (requiresAdmin && !authStore.isAdmin) {
    // 需要管理员权限但当前用户不是管理员，重定向到主页
    next({ name: 'home' })
  } else if (to.name === 'login' && isAuthenticated) {
    // 如果用户已登录，但试图访问登录页，则重定向到主页
    next({ name: 'home' })
  } else {
    // 其他情况，正常放行
    next()
  }
})

export default router
