<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <el-scrollbar>
        <el-menu :default-openeds="defaultOpeneds" router>
          <template v-for="item in menu" :key="item.key">
            <el-sub-menu v-if="item.children && item.children.length" :index="item.key">
              <template #title>
                <el-icon>
                  <component :is="getIconComponent(item.icon)" />
                </el-icon>
                {{ item.title }}
              </template>

              <el-menu-item v-for="child in item.children" :key="child.key" :index="child.path">
                {{ child.title }}
              </el-menu-item>
            </el-sub-menu>

            <el-menu-item v-else :index="item.path">
              <el-icon>
                <component :is="getIconComponent(item.icon)" />
              </el-icon>
              <span>{{ item.title }}</span>
            </el-menu-item>
          </template>
        </el-menu>
      </el-scrollbar>
    </el-aside>

    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <div class="toolbar">
          <UserAvatar />
          <el-dropdown>
            <el-icon style="margin-right: 8px; margin-top: 1px">
              <component :is="getIconComponent()" />
            </el-icon>
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
import { computed, onMounted, ref, watch } from 'vue'
import * as Icons from '@element-plus/icons-vue'
import menuConfig from '@/config/menu'
import ICON_MAP from '@/config/icon-map'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'
import UserAvatar from '@/components/UserAvatar.vue'
import { useRoute } from 'vue-router'

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

// menu and icon helpers
const menuItems = menuConfig

// explicit icon mapping to avoid heuristic mismatch
// ICON_MAP imported from config/icon-map.ts

const route = useRoute()
const defaultOpeneds = ref<string[]>([])

function findParentKeysForPath(path: string) {
  const parents: string[] = []
  for (const item of menuItems) {
    if (item.children) {
      for (const c of item.children) {
        if (c.path === path) {
          parents.push(item.key)
        }
      }
    } else if (item.path === path) {
      // top-level item, no parent
    }
  }
  return parents
}

// initialize based on current route
defaultOpeneds.value = findParentKeysForPath(route.path)

// update when route changes
watch(
  () => route.path,
  (newPath) => {
    defaultOpeneds.value = findParentKeysForPath(newPath)
  }
)

/**
 * Return the component for a given icon name string from Element Plus icons.
 * Falls back to a generic Setting icon when not found.
 */
function getIconComponent(name?: string) {
  if (!name) return Icons.Setting
  const key = ICON_MAP[name] || (name.charAt(0).toUpperCase() + name.slice(1))
  return (Icons as any)[key] || Icons.Setting
}

// expose to template
const menu = menuItems
</script>

<style scoped>
.layout-container {
  height: 100vh;
  background: #f5f7fa;
}

.el-aside {
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  transition: width 0.3s ease;
}

.el-aside :deep(.el-menu) {
  background: transparent;
  border-right: none;
}

.el-aside :deep(.el-menu-item),
.el-aside :deep(.el-sub-menu__title) {
  color: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.el-aside :deep(.el-menu-item:hover),
.el-aside :deep(.el-sub-menu__title:hover) {
  background: rgba(102, 126, 234, 0.2) !important;
  color: white;
}

.el-aside :deep(.el-menu-item.is-active) {
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8)) !important;
  color: white;
  border-left: 4px solid #fff;
}

.el-aside :deep(.el-sub-menu.is-active .el-sub-menu__title) {
  color: white;
}

.el-header {
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 24px;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: 16px;
  color: white;
}

.toolbar span {
  color: white;
  font-weight: 500;
}

.toolbar :deep(.el-icon) {
  color: white;
  font-size: 18px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.toolbar :deep(.el-icon:hover) {
  transform: scale(1.1);
  color: rgba(255, 255, 255, 0.8);
}

.el-main {
  padding: 24px;
  background: #f5f7fa;
  min-height: calc(100vh - 60px);
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
