<template>
  <el-avatar :src="src" :size="size" @click="openProfile" class="user-avatar" />
</template>

<script lang="ts" setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const props = defineProps({
  size: {
    type: Number,
    default: 40
  }
})

const authStore = useAuthStore()
const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'

const src = computed(() => authStore.user?.avatar || defaultAvatar)

const router = useRouter()
const openProfile = () => {
  // navigate to personal profile page
  router.push({ path: '/user/profile' })
}
</script>

<style scoped>
.user-avatar {
  cursor: pointer;
}
.avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
}
.avatar-uploader-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
</style>
