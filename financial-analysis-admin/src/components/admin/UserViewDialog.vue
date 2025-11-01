<template>
  <el-dialog :title="'查看用户 - ' + (user?.username || '')" v-model="visibleLocal" width="520px" append-to-body>
    <div v-if="user">
      <div style="display:flex;gap:12px;align-items:center;margin-bottom:12px">
  <img v-if="user.avatar" :src="user.avatar" alt="avatar" title="用户头像" style="width:72px;height:72px;border-radius:6px;object-fit:cover" />
        <div>
          <div style="font-weight:600">{{ user.username }}</div>
          <div style="color:#888">{{ user.nickname || '' }}</div>
        </div>
      </div>

      <el-descriptions column="1" border>
        <el-descriptions-item label="角色">{{ user.role }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ user.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="手机">{{ user.phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="签名">{{ user.signature || '-' }}</el-descriptions-item>
        <el-descriptions-item label="创建时间">{{ user.created_at || '-' }}</el-descriptions-item>
      </el-descriptions>
    </div>
    <template #footer>
      <el-button @click="close">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { defineProps, defineEmits, toRefs, watch, computed } from 'vue'

const props = defineProps<{ modelValue: boolean; user: any }>()
const emit = defineEmits(['update:modelValue'])

// writable proxy for visible prop so el-dialog can v-model without mutating prop directly
const visibleLocal = computed<boolean>({
  get: () => props.modelValue,
  set: (val: boolean) => emit('update:modelValue', val)
})

function close() {
  visibleLocal.value = false
}

watch(() => props.modelValue, (val) => {
  // placeholder in case we need side-effects when visibility changes
})
</script>
<!-- debug z-index overrides removed -->
