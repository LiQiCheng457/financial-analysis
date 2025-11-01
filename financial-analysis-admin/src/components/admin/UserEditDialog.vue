<template>
  <el-dialog :title="title" v-model="visibleLocal" width="560px" append-to-body>
  <el-form :model="local" :rules="rules" ref="formRef" label-width="110px">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="local.username" :disabled="isViewMode" />
      </el-form-item>
      <el-form-item label="昵称" prop="nickname">
        <el-input v-model="local.nickname" />
      </el-form-item>
      <el-form-item label="邮箱" prop="email">
        <el-input v-model="local.email" />
      </el-form-item>
      <el-form-item label="手机" prop="phone">
        <el-input v-model="local.phone" />
      </el-form-item>
      <el-form-item label="角色" prop="role">
        <el-select v-model="local.role" placeholder="选择角色">
          <el-option label="管理员" value="admin" />
          <el-option label="普通用户" value="user" />
        </el-select>
      </el-form-item>
      <template v-if="isCreate">
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="local.password" />
        </el-form-item>
      </template>
      <template v-else>
        <el-form-item label="新密码" prop="password">
         <el-input type="password" v-model="local.password" show-password autocomplete="new-password" />
        </el-form-item>
        <el-form-item label="确认密码" prop="password_confirm">
         <el-input type="password" v-model="local.password_confirm" show-password autocomplete="new-password" />
        </el-form-item>
      </template>
    </el-form>

    <template #footer>
      <el-button @click="onCancel">取消</el-button>
      <el-button type="primary" @click="onSubmit">保存</el-button>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { reactive, watch, ref, computed } from 'vue'

const props = defineProps<{ modelValue: boolean; user: any | null }>()
const emit = defineEmits(['update:modelValue', 'save'])

// create writable computed to proxy v-model value and emit updates
const visibleLocal = computed<boolean>({
  get: () => props.modelValue,
  set: (val: boolean) => emit('update:modelValue', val)
})

const formRef = ref<any>()

const local = reactive({ username: '', password: '', password_confirm: '', role: 'user', email: '', nickname: '', phone: '' })

const rules = computed(() => {
  const base: any = {
    username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    role: [{ required: true, message: '请选择角色', trigger: 'change' }],
    email: [{ type: 'email', required: false, message: '请输入正确的邮箱', trigger: 'blur' }]
  }
  // require password only when creating or when a new password was entered
  if (isCreate.value || (local.password && String(local.password).length > 0)) {
    base.password = [{ required: true, message: '请输入密码', trigger: 'blur' }]
    base.password_confirm = [
      { required: true, message: '请确认密码', trigger: 'blur' },
      { validator: (_rule: any, value: string, callback: any) => {
        if (value !== local.password) callback(new Error('两次密码输入不一致'))
        else callback()
      }, trigger: 'blur' }
    ]
  }
  return base
})

const isCreate = computed(() => !props.user)
const isViewMode = false

watch(() => props.user, (u) => {
  if (u) {
    local.username = u.username || ''
    local.role = u.role || 'user'
    local.email = u.email || ''
    local.nickname = u.nickname || ''
    local.phone = u.phone || ''
  local.password = ''
  local.password_confirm = ''
  } else {
    local.username = ''
    local.password = ''
    local.role = 'user'
    local.email = ''
    local.nickname = ''
    local.phone = ''
  }
}, { immediate: true })

const title = computed(() => (props.user ? `编辑用户 - ${props.user.username}` : '新建用户'))

function onCancel() {
  visibleLocal.value = false
}

async function onSubmit() {
  try {
    await formRef.value.validate()
  } catch (err) {
    return
  }
  const payload: any = { username: local.username, role: local.role, email: local.email, nickname: local.nickname, phone: local.phone }
  if (isCreate.value || (local.password && String(local.password).length > 0)) payload.password = local.password
  emit('save', payload)
  emit('update:modelValue', false)
}
</script>
<!-- debug z-index overrides removed -->
