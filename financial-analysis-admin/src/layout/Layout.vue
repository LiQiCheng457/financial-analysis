<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <el-scrollbar>
        <el-menu :default-openeds="['1']" router>
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>主页</span>
          </el-menu-item>
          <el-sub-menu index="1">
            <template #title>
              <el-icon><TrendCharts /></el-icon>数据分析
            </template>
            <el-menu-item index="/market-summary">每日概况</el-menu-item>
            <el-menu-item index="/stock-history">历史行情数据</el-menu-item>
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
import { HomeFilled, TrendCharts, Setting } from '@element-plus/icons-vue'
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
