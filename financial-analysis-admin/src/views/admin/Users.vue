<template>
  <div class="users-page">
    <el-card>
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
        <div style="display:flex;align-items:center;gap:12px;flex:1">
          <div style="font-size:18px;font-weight:600">用户管理</div>
          <el-input v-model="searchQuery" placeholder="搜索： 用户名/昵称" size="small" clearable @clear="onSearchClear" @keyup.enter="onSearch" style="width:260px;min-width:200px" />
          <el-button size="small" @click="onSearch">搜索</el-button>
        </div>
        <div>
          <el-button type="primary" size="small" @click="openCreate">新建用户</el-button>
        </div>
      </div>

      <el-table :data="users" stripe style="width:100%" row-key="id" empty-text="暂无用户">
        <el-table-column type="index" label="#" width="80" align="center" :index="indexMethod" />
        <el-table-column label="用户 / 昵称" min-width="200">
          <template #default="{ row }">
            <div class="user-cell">
              <el-avatar v-if="row.avatar" :src="row.avatar" :size="36" />
              <el-avatar v-else :size="36">
                {{ (row.username || '?')[0].toUpperCase() }}
              </el-avatar>
              <div class="user-text">
                <div class="user-name">{{ row.username || '-' }}</div>
                <div class="user-nick">{{ row.nickname || '-' }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="role" label="角色" width="120" align="center">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'info'" size="small">
              {{ roleLabel(row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" align="center">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="info" link size="small" @click="openView(row)">
              查看
            </el-button>
            <el-button type="primary" link size="small" @click="openEdit(row)">
              编辑
            </el-button>
            <el-button type="danger" link size="small" @click="confirmDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 当总数大于每页数量时显示分页 -->
      <div v-if="shouldShowPagination" class="pagination-bar">
        <el-pagination
          v-model:current-page="page"
          :page-size="pageSize"
          :total="total"
          layout="prev, pager, next"
          background
          @current-change="onPageChange"
        />
      </div>
    </el-card>

  <!-- debug banners removed -->

  <!-- Use separate components for view and edit dialogs -->
  <UserViewDialog v-model="showView" :user="selectedUser" />
  <UserEditDialog v-model="showEdit" :user="selectedUser" @save="onDialogSave" />

    <!-- reset password dialog removed per request -->
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import adminApi from '@/api/admin'

const users = ref([] as any[])
const total = ref(0)
const page = ref(1)
const pageSize = ref(8)
const searchQuery = ref('')

// 计算是否显示分页
const shouldShowPagination = computed(() => {
  const show = total.value > 8
  console.log('[Users] shouldShowPagination computed:', show, 'total=', total.value)
  return show
})

import UserViewDialog from '@/components/admin/UserViewDialog.vue'
import UserEditDialog from '@/components/admin/UserEditDialog.vue'

const showView = ref(false)
const showEdit = ref(false)
const selectedUser = ref<any | null>(null)

// reset password UI removed

// local validation rules are handled inside the edit dialog component

const fetchUsers = async () => {
  try {
    const params: any = { skip: (page.value - 1) * pageSize.value, limit: pageSize.value }
    if (searchQuery.value && searchQuery.value.trim()) params.q = searchQuery.value.trim()
    const res: any = await adminApi.listUsers(params)
    
    console.log('[Users] fetchUsers 响应:', res)
    
    // expect { items: [], total: N }
    if (res && (res.items || res.data?.items)) {
      const payload = res.items || res.data.items
      users.value = payload
      total.value = res.total || res.data.total || payload.length
      console.log('[Users] 用户列表:', payload.length, '总数:', total.value)
      console.log('[Users] 是否显示分页?', total.value, '>', pageSize.value, '=', total.value > pageSize.value)
    } else if (Array.isArray(res)) {
      users.value = res
      total.value = res.length
      console.log('[Users] 用户列表(数组):', res.length, '总数:', total.value)
      console.log('[Users] 是否显示分页?', total.value, '>', pageSize.value, '=', total.value > pageSize.value)
    } else if (res && res.data && Array.isArray(res.data)) {
      users.value = res.data
      total.value = res.data.length
      console.log('[Users] 用户列表(data数组):', res.data.length, '总数:', total.value)
      console.log('[Users] 是否显示分页?', total.value, '>', pageSize.value, '=', total.value > pageSize.value)
    } else {
      users.value = []
      total.value = 0
      console.log('[Users] 无用户数据')
    }
  } catch (e) {
    console.error(e)
    ElMessage.error('获取用户列表失败')
  }
}

onMounted(() => {
  fetchUsers()
  // expose reactive state for debugging in browser console
  // usage in console: window.__users_debug.selectedUser.value  or window.__users_debug.users
  // DO NOT leave sensitive tokens here in production
  ;(window as any).__users_debug = { users, selectedUser, showView, showEdit, page, searchQuery }
})

const onPageChange = (p: number) => {
  page.value = p
  fetchUsers()
}

const onSearch = async () => {
  page.value = 1
  fetchUsers()
}

const onSearchClear = () => {
  searchQuery.value = ''
  page.value = 1
  fetchUsers()
}

// 删除 quick reset 按钮功能（如需保留，可改为配置化）

const openView = async (row: any) => {
  console.log('[Users] openView called, row=', row)
  selectedUser.value = row
  showView.value = true
  console.log('[Users] showView set to', showView.value)
  // try refresh latest details
  try {
    const res: any = await adminApi.getUser(row.id)
    const data = res.data || res
    selectedUser.value = data
    console.log('[Users] openView fetched user detail', data)
  } catch (e) {
    console.warn('openView: fetch detail failed, using row data', e)
  }
}

const openCreate = () => {
  selectedUser.value = null
  showEdit.value = true
}

const openEdit = async (row: any) => {
  console.log('[Users] openEdit called, row=', row)
  selectedUser.value = row
  showEdit.value = true
  console.log('[Users] showEdit set to', showEdit.value)
  try {
    const res: any = await adminApi.getUser(row.id)
    const data = res.data || res
    selectedUser.value = data
    console.log('[Users] openEdit fetched user detail', data)
  } catch (e) {
    console.warn('openEdit: fetch detail failed, using row data', e)
  }
}

// watch visibility flags to help debugging in browser console
import { watch } from 'vue'
watch(showView, (v) => {
  console.log('[Users] showView changed ->', v)
  if (v) {
    // after DOM updates, check whether dialog elements were added and their computed styles
    setTimeout(() => {
      try {
        const wrappers = document.querySelectorAll('.el-dialog__wrapper')
        console.log('[Users][DOM] dialog wrappers count=', wrappers.length)
        wrappers.forEach((w, i) => console.log(`[Users][DOM] wrapper[${i}]`, w, getComputedStyle(w)))
        const overlays = document.querySelectorAll('.el-overlay')
        console.log('[Users][DOM] overlays count=', overlays.length)
        overlays.forEach((o, i) => console.log(`[Users][DOM] overlay[${i}]`, o, getComputedStyle(o)))
      } catch (err) {
        console.warn('[Users][DOM] inspect failed', err)
      }
    }, 80)
  }
})

watch(showEdit, (v) => {
  console.log('[Users] showEdit changed ->', v)
  if (v) {
    setTimeout(() => {
      try {
        const wrappers = document.querySelectorAll('.el-dialog__wrapper')
        console.log('[Users][DOM] dialog wrappers count=', wrappers.length)
        wrappers.forEach((w, i) => console.log(`[Users][DOM] wrapper[${i}]`, w, getComputedStyle(w)))
        const overlays = document.querySelectorAll('.el-overlay')
        console.log('[Users][DOM] overlays count=', overlays.length)
        overlays.forEach((o, i) => console.log(`[Users][DOM] overlay[${i}]`, o, getComputedStyle(o)))
      } catch (err) {
        console.warn('[Users][DOM] inspect failed', err)
      }
    }, 80)
  }
})

// handle save event emitted by edit dialog
const onDialogSave = async (payload: any) => {
  try {
    if (selectedUser.value && selectedUser.value.id) {
      await adminApi.updateUser(selectedUser.value.id, payload)
      ElMessage.success('更新成功')
    } else {
      await adminApi.createUser(payload)
      ElMessage.success('创建成功')
    }
    fetchUsers()
  } catch (err: any) {
    console.error('onDialogSave error', err)
    const detail = err?.response?.data?.detail || err?.response?.data || err?.message || '保存失败'
    ElMessage.error(String(detail))
  }
}

// reset removed

const confirmDelete = async (row: any) => {
  try {
    await ElMessageBox.confirm(`确认删除用户 ${row.username} ? 此操作不可恢复`, '删除确认', { type: 'warning' })
  } catch (e) {
    return
  }
  try {
    await adminApi.deleteUser(row.id)
    ElMessage.success('用户已删除')
    fetchUsers()
  } catch (e) {
    console.error(e)
    ElMessage.error('删除失败')
  }
}

// submitReset removed

// helper: map role code to human-readable label
const roleLabel = (role: string) => {
  if (!role) return '-'
  const map: Record<string, string> = { admin: '管理员', user: '普通用户' }
  return map[role] || role
}

// helper: format date/time for display
const formatDate = (val: any) => {
  if (!val) return '-'
  try {
    const d = typeof val === 'number' ? new Date(val) : new Date(String(val))
    if (isNaN(d.getTime())) return '-'
    return d.toLocaleString()
  } catch (e) {
    return '-'
  }
}

// helper: calculate row index for pagination
const indexMethod = (index: number) => {
  return (page.value - 1) * pageSize.value + index + 1
}

</script>

<style scoped>
.users-page {
  width: 100%;
  height: 100%;
  overflow-y: auto;
}

.el-card {
  min-height: 100%;
  height: auto;
}

/* 用户信息单元格 */
.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 4px 0;
}

.user-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}

.user-name {
  font-weight: 500;
  font-size: 14px;
  color: #303133;
}

.user-nick {
  font-size: 12px;
  color: #909399;
}

/* 分页栏 */
.pagination-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  padding: 16px 0;
}

/* 让分页组件更醒目 */
.pagination-bar :deep(.el-pagination) {
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
