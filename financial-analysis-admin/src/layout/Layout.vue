<template>
  <el-container class="layout-container">
    <!-- 桌面端固定侧边栏 -->
    <el-aside width="200px" class="desktop-sidebar">
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

    <!-- 移动端抽屉式侧边栏 -->
    <el-drawer
      v-model="mobileMenuVisible"
      direction="ltr"
      :size="260"
      class="mobile-drawer"
      :with-header="false"
    >
      <el-scrollbar>
        <el-menu :default-openeds="defaultOpeneds" router @select="handleMobileMenuSelect">
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
    </el-drawer>

    <el-container>
      <el-header style="text-align: right; font-size: 12px">
        <div class="toolbar">
          <!-- 移动端汉堡菜单按钮 -->
          <el-button 
            class="mobile-menu-btn" 
            :icon="Menu" 
            circle 
            @click="toggleMobileMenu"
          />
          
          <div class="spacer"></div>
          
          <UserAvatar />
          <div class="user-info-section">
            <span class="username">{{ username }}</span>
            <el-tag 
              :type="authStore.isAdmin ? 'danger' : 'primary'" 
              size="small" 
              effect="dark"
              class="role-tag"
            >
              {{ authStore.roleDisplayName }}
            </el-tag>
          </div>
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
import { Menu } from '@element-plus/icons-vue'
import menuConfig from '@/config/menu'
import ICON_MAP from '@/config/icon-map'
import { useAuthStore } from '@/store/auth'
import { useRouter } from 'vue-router'
import UserAvatar from '@/components/UserAvatar.vue'
import { useRoute } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const username = computed(() => authStore.user?.username || '未登录')

// 移动端菜单状态
const mobileMenuVisible = ref(false)

const toggleMobileMenu = () => {
  mobileMenuVisible.value = !mobileMenuVisible.value
}

const handleMobileMenuSelect = () => {
  // 选择菜单项后自动关闭抽屉
  mobileMenuVisible.value = false
}

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

// 根据角色过滤菜单项（如果项或子项设置了 adminOnly，则仅管理员可见）
const filteredMenu = computed(() => {
  const isAdmin = authStore.isAdmin
  const filtered = menuItems
    .map(item => {
      if (item.children && item.children.length) {
        const children = item.children.filter(c => !(c as any).adminOnly || isAdmin)
        return { ...item, children }
      }
      // top-level item
      if ((item as any).adminOnly && !isAdmin) return null
      return item
    })
    .filter(Boolean) as typeof menuItems
  return filtered
})

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
const menu = filteredMenu
</script>

<style scoped>
.layout-container {
  height: 100vh;
  background: #f5f7fa;
}

/* 桌面端侧边栏 */
.desktop-sidebar {
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  transition: width 0.3s ease;
}

.desktop-sidebar :deep(.el-menu) {
  background: transparent;
  border-right: none;
}

.desktop-sidebar :deep(.el-menu-item),
.desktop-sidebar :deep(.el-sub-menu__title) {
  color: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.desktop-sidebar :deep(.el-menu-item:hover),
.desktop-sidebar :deep(.el-sub-menu__title:hover) {
  background: rgba(102, 126, 234, 0.2) !important;
  color: white;
}

.desktop-sidebar :deep(.el-menu-item.is-active) {
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8)) !important;
  color: white;
  border-left: 4px solid #fff;
}

.desktop-sidebar :deep(.el-sub-menu.is-active .el-sub-menu__title) {
  color: white;
}

/* 移动端抽屉 */
.mobile-drawer :deep(.el-drawer__body) {
  padding: 0;
  background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
}

.mobile-drawer :deep(.el-menu) {
  background: transparent;
  border-right: none;
}

.mobile-drawer :deep(.el-menu-item),
.mobile-drawer :deep(.el-sub-menu__title) {
  color: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.mobile-drawer :deep(.el-menu-item:hover),
.mobile-drawer :deep(.el-sub-menu__title:hover) {
  background: rgba(102, 126, 234, 0.2) !important;
  color: white;
}

.mobile-drawer :deep(.el-menu-item.is-active) {
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8)) !important;
  color: white;
  border-left: 4px solid #fff;
}

/* 移动端菜单按钮 */
.mobile-menu-btn {
  display: none;
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
}

.mobile-menu-btn:hover,
.mobile-menu-btn:focus {
  background: rgba(255, 255, 255, 0.3);
  color: white;
}

.spacer {
  flex: 1;
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
  width: 100%;
}

.user-info-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.username {
  color: white;
  font-weight: 500;
  font-size: 14px;
}

.role-tag {
  font-size: 12px;
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

/* ========== 响应式布局 ========== */

/* 平板适配 (768px - 1024px) */
@media (max-width: 1024px) {
  .el-header {
    padding: 0 16px;
  }
  
  .toolbar {
    gap: 12px;
  }
  
  .el-main {
    padding: 16px;
  }
}

/* 手机适配 (小于 768px) */
@media (max-width: 768px) {
  /* 隐藏桌面端侧边栏 */
  .desktop-sidebar {
    display: none !important;
  }
  
  /* 显示移动端菜单按钮 */
  .mobile-menu-btn {
    display: inline-flex !important;
  }
  
  .el-header {
    padding: 0 12px;
  }
  
  .toolbar {
    gap: 8px;
  }
  
  /* 隐藏用户名,只保留头像和下拉菜单 */
  .username {
    display: none;
  }
  
  .role-tag {
    display: none;
  }
  
  .el-main {
    padding: 12px;
  }
}

/* 超小屏幕适配 (小于 480px) */
@media (max-width: 480px) {
  .el-header {
    padding: 0 8px;
    height: 50px;
  }
  
  .toolbar {
    gap: 6px;
  }
  
  .toolbar :deep(.el-avatar) {
    width: 32px !important;
    height: 32px !important;
  }
  
  .toolbar :deep(.el-icon) {
    font-size: 16px;
  }
  
  .mobile-menu-btn {
    width: 36px !important;
    height: 36px !important;
  }
  
  .el-main {
    padding: 8px;
    min-height: calc(100vh - 50px);
  }
  
  /* 抽屉宽度调整 */
  .mobile-drawer :deep(.el-drawer) {
    width: 80% !important;
    max-width: 260px;
  }
}

/* 横屏模式优化 */
@media (max-height: 600px) and (orientation: landscape) {
  .el-header {
    height: 50px;
  }
  
  .el-main {
    min-height: calc(100vh - 50px);
  }
}
</style>
