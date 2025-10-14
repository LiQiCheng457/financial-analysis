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
