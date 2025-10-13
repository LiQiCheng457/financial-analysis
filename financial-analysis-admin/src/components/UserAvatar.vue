<template>
  <el-avatar :src="src" :size="size" @click="openAvatarDialog" class="user-avatar"></el-avatar>

  <el-dialog v-model="dialogVisible" title="修改头像" width="30%">
    <div class="avatar-uploader-container">
      <el-upload
        class="avatar-uploader"
        action="#"
        :show-file-list="false"
        :before-upload="beforeAvatarUpload"
        :http-request="handleHttpRequest"
      >
        <img v-if="imageUrl" :src="imageUrl" class="avatar" />
        <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
      </el-upload>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitAvatar">
          确认
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import type { UploadProps } from 'element-plus'
import { useAuthStore } from '@/store/auth'
import axios from 'axios'

const props = defineProps({
  size: {
    type: Number,
    default: 40
  }
})

const authStore = useAuthStore()
const dialogVisible = ref(false)
const imageUrl = ref('')

const defaultAvatar = 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'

const src = computed(() => {
  return authStore.user?.avatar || defaultAvatar
})

const openAvatarDialog = () => {
  imageUrl.value = authStore.user?.avatar || ''
  dialogVisible.value = true
}

const beforeAvatarUpload: UploadProps['beforeUpload'] = (rawFile) => {
  if (rawFile.type !== 'image/jpeg' && rawFile.type !== 'image/png') {
    ElMessage.error('头像图片只能是 JPG 或 PNG 格式!')
    return false
  } else if (rawFile.size / 1024 / 1024 > 2) {
    ElMessage.error('头像图片大小不能超过 2MB!')
    return false
  }
  return true
}

const handleHttpRequest: UploadProps['httpRequest'] = (options) => {
  const reader = new FileReader()
  reader.readAsDataURL(options.file)
  reader.onload = () => {
    imageUrl.value = reader.result as string
  }
  return Promise.resolve()
}

const submitAvatar = async () => {
  if (!imageUrl.value) {
    ElMessage.warning('请先上传一张图片')
    return
  }
  try {
    const response = await axios.put('/api/users/me/avatar', 
      { avatar: imageUrl.value },
      {
        headers: {
          Authorization: `Bearer ${authStore.token}`
        }
      }
    )
    // 更新 store 中的用户信息
    authStore.user = response.data
    ElMessage.success('头像修改成功!')
    dialogVisible.value = false
  } catch (error) {
    console.error('头像上传失败:', error)
    ElMessage.error('头像上传失败，请稍后重试')
  }
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
