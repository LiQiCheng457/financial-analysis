<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <el-scrollbar>
        <el-menu :default-openeds="['market']" router>
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>主页</span>
          </el-menu-item>

          <!-- 行情中心 -->
          <el-sub-menu index="market">
            <template #title>
              <el-icon><Document /></el-icon>行情中心
            </template>
            <el-menu-item index="/market/summary">每日概况</el-menu-item>
            <el-menu-item index="/market/history">历史行情数据</el-menu-item>
            <el-menu-item index="/market/kline">K线图</el-menu-item>
            <el-menu-item index="/market/timeseries">分时图</el-menu-item>
            <el-menu-item index="/market/snapshot">个股快照</el-menu-item>
          </el-sub-menu>

          <!-- 自选股 -->
          <el-sub-menu index="watchlist">
            <template #title>
              <el-icon><Bell /></el-icon>自选股
            </template>
            <el-menu-item index="/watchlist/crud">增删改查</el-menu-item>
            <el-menu-item index="/watchlist/groups">分组管理</el-menu-item>
            <el-menu-item index="/watchlist/alerts">涨跌提醒</el-menu-item>
          </el-sub-menu>

          <!-- 选股器 -->
          <el-sub-menu index="picker">
            <template #title>
              <el-icon><Document /></el-icon>选股器
            </template>
            <el-menu-item index="/picker/filter">条件筛选</el-menu-item>
            <el-menu-item index="/picker/backtest">策略回测</el-menu-item>
            <el-menu-item index="/picker/hot">热门策略</el-menu-item>
          </el-sub-menu>

          <!-- 财务分析 -->
          <el-sub-menu index="finance">
            <template #title>
              <el-icon><Document /></el-icon>财务分析
            </template>
            <el-menu-item index="/finance/reports">财务报表</el-menu-item>
            <el-menu-item index="/finance/metrics">关键指标</el-menu-item>
            <el-menu-item index="/finance/peer">同业对比</el-menu-item>
          </el-sub-menu>

          <!-- 新闻报告 -->
          <el-sub-menu index="news">
            <template #title>
              <el-icon><Document /></el-icon>新闻报告
            </template>
            <el-menu-item index="/news/realtime">实时新闻</el-menu-item>
            <el-menu-item index="/news/announcements">公司公告</el-menu-item>
          </el-sub-menu>

          <!-- 用户系统 -->
          <el-sub-menu index="user">
            <template #title>
              <el-icon><User /></el-icon>用户系统
            </template>
            <el-menu-item index="/user/profile">个人中心</el-menu-item>
            <el-menu-item index="/user/permissions">权限管理</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-scrollbar>
    </el-aside>

    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <div class="toolbar">
          <UserAvatar />
          <el-dropdown>
            <el-icon style="margin-right: 8px; margin-top: 1px"
              ><setting
            /></el-icon>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <span>{{ username }}</span>
        </div>
      </el-header>

      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script lang="ts" setup>
import { computed, onMounted } from 'vue'
import { HomeFilled, Setting, Document, Bell, User } from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'
import UserAvatar from '@/components/UserAvatar.vue'

const authStore = useAuthStore()
const router = useRouter()

const username = computed(() => authStore.user?.username || '未登录')

const handleLogout = () => {
  authStore.logout()
  router.push({ name: 'login' })
}

onMounted(() => {
  if (authStore.token && !authStore.user) {
    authStore.fetchUser()
  }
})
</script>

<style scoped>
.layout-container {
  height: 100vh;
}
.el-header {
  position: relative;
  background-color: var(--el-color-primary-light-7);
  color: var(--el-text-color-primary);
}
.toolbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  right: 20px;
}
</style>
