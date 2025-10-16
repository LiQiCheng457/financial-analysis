import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/home/index.vue'),
    meta: {
      title: '首页',
    },
  },
  {
    path: '/company',
    name: 'Company',
    component: () => import('@/views/company/index.vue'),
    meta: {
      title: '公司查询',
    },
  },
  {
    path: '/company/:code',
    name: 'CompanyDetail',
    component: () => import('@/views/company/detail.vue'),
    meta: {
      title: '公司详情',
    },
  },
  {
    path: '/market',
    name: 'Market',
    component: () => import('@/views/market/index.vue'),
    meta: {
      title: '市场概况',
    },
  },
  {
    path: '/user',
    name: 'User',
    component: () => import('@/views/user/index.vue'),
    meta: {
      title: '用户中心',
    },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/error/404.vue'),
    meta: {
      title: '页面未找到',
    },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title || '金融分析系统'} - 金融分析系统`
  next()
})

export default router
