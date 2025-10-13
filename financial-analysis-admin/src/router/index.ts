import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/layout/Layout.vue'
import LoginView from '../views/login/LoginView.vue'
import HomeView from '../views/home/HomeView.vue'
import { useAuthStore } from '@/store/auth'

import StockHistory from '@/views/stock/StockHistory.vue'

import MarketSummary from '@/views/market/MarketSummary.vue'

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
        path: 'stock-history',
        name: 'stock-history',
        component: StockHistory,
      },
      {
        path: 'market-summary',
        name: 'market-summary',
        component: MarketSummary,
      }
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

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = !!authStore.token

  // 检查目标路由或其任何匹配的父路由是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

  if (requiresAuth && !isAuthenticated) {
    // 如果目标路由需要认证但用户未登录，则重定向到登录页
    next({ name: 'login' })
  } else if (to.name === 'login' && isAuthenticated) {
    // 如果用户已登录，但试图访问登录页，则重定向到主页
    next({ name: 'home' })
  } else {
    // 其他情况，正常放行
    next()
  }
})

export default router
