<template>
  <div class="profile-container">
    <!-- 头部信息卡片 -->
    <el-card class="profile-header">
      <div class="header-content">
        <div class="avatar-section">
          <el-avatar :size="120" :src="userInfo.avatar || undefined" class="user-avatar">
            <el-icon :size="60"><User /></el-icon>
          </el-avatar>
          <el-upload
            :show-file-list="false"
            :before-upload="handleAvatarUpload"
            accept="image/*"
            class="avatar-upload"
          >
            <el-button size="small" type="primary" :icon="Camera">更换头像</el-button>
          </el-upload>
        </div>
        <div class="user-info">
          <h2 class="username">{{ userInfo.username }}</h2>
          <div class="user-meta">
            <el-tag 
              :type="userInfo.role === 'admin' ? 'danger' : 'primary'" 
              size="large" 
              effect="dark"
            >
              <el-icon><UserFilled /></el-icon>
              {{ getRoleDisplayName(userInfo.role) }}
            </el-tag>
            <el-tag type="info" size="small">
              <el-icon><Clock /></el-icon>
              注册时间：{{ formatDate(userInfo.created_at) }}
            </el-tag>
            <el-tag type="success" size="small">
              <el-icon><Connection /></el-icon>
              在线
            </el-tag>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 标签页 -->
    <el-card class="tabs-card">
      <el-tabs v-model="activeTab" class="profile-tabs">
        <!-- 个人资料 -->
        <el-tab-pane label="个人资料" name="profile">
          <div class="tab-content">
            <el-form :model="profileForm" label-width="100px" class="profile-form">
              <el-form-item label="用户名">
                <el-input v-model="profileForm.username" disabled>
                  <template #suffix>
                    <el-tooltip content="用户名不可修改" placement="top">
                      <el-icon><Lock /></el-icon>
                    </el-tooltip>
                  </template>
                </el-input>
              </el-form-item>
              
              <el-form-item label="昵称">
                <el-input v-model="profileForm.nickname" placeholder="请输入昵称" clearable />
              </el-form-item>
              
              <el-form-item label="手机号">
                <el-input v-model="profileForm.phone" placeholder="请输入手机号" clearable>
                  <template #prefix>
                    <el-icon><Iphone /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
              
              <el-form-item label="邮箱">
                <el-input v-model="profileForm.email" placeholder="请输入邮箱" clearable>
                  <template #prefix>
                    <el-icon><Message /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
              
              <el-form-item label="个性签名">
                <el-input 
                  v-model="profileForm.signature" 
                  type="textarea" 
                  :rows="3"
                  placeholder="写点什么介绍自己吧..."
                  maxlength="100"
                  show-word-limit
                />
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="handleUpdateProfile" :loading="profileLoading">
                  保存修改
                </el-button>
                <el-button @click="resetProfileForm">重置</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>

        <!-- 安全设置 -->
        <el-tab-pane label="安全设置" name="security">
          <div class="tab-content">
            <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="100px" class="security-form">
              <el-alert
                title="密码修改提示"
                type="info"
                description="为了您的账户安全，建议定期更换密码，密码长度至少6位"
                :closable="false"
                show-icon
                class="security-alert"
              />
              
              <el-form-item label="旧密码" prop="oldPassword">
                <el-input 
                  v-model="passwordForm.oldPassword" 
                  type="password" 
                  placeholder="请输入当前密码"
                  show-password
                >
                  <template #prefix>
                    <el-icon><Lock /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
              
              <el-form-item label="新密码" prop="newPassword">
                <el-input 
                  v-model="passwordForm.newPassword" 
                  type="password" 
                  placeholder="请输入新密码（至少6位）"
                  show-password
                >
                  <template #prefix>
                    <el-icon><Key /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
              
              <el-form-item label="确认密码" prop="confirmPassword">
                <el-input 
                  v-model="passwordForm.confirmPassword" 
                  type="password" 
                  placeholder="请再次输入新密码"
                  show-password
                >
                  <template #prefix>
                    <el-icon><Key /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="handleChangePassword" :loading="passwordLoading">
                  修改密码
                </el-button>
                <el-button @click="resetPasswordForm">重置</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>

        <!-- 偏好设置 -->
        <el-tab-pane label="偏好设置" name="preferences">
          <div class="tab-content">
            <el-form label-width="120px" class="preferences-form">
              <el-divider content-position="left">
                <span class="divider-title">界面设置</span>
              </el-divider>
              
              <el-form-item label="主题模式">
                <el-radio-group v-model="preferences.theme" disabled>
                  <el-radio label="light">浅色</el-radio>
                  <el-radio label="dark">深色</el-radio>
                  <el-radio label="auto">跟随系统</el-radio>
                </el-radio-group>
                <el-text type="info" size="small" style="margin-left: 12px;">功能开发中</el-text>
              </el-form-item>
              
              <el-form-item label="语言设置">
                <el-select v-model="preferences.language" placeholder="请选择语言" disabled>
                  <el-option label="简体中文" value="zh-CN" />
                  <el-option label="English" value="en-US" />
                </el-select>
                <el-text type="info" size="small" style="margin-left: 12px;">功能开发中</el-text>
              </el-form-item>
              
              <el-divider content-position="left">
                <span class="divider-title">数据展示</span>
              </el-divider>
              
              <el-form-item label="默认复权方式">
                <el-radio-group v-model="preferences.adjustType" disabled>
                  <el-radio label="">不复权</el-radio>
                  <el-radio label="qfq">前复权</el-radio>
                  <el-radio label="hfq">后复权</el-radio>
                </el-radio-group>
                <el-text type="info" size="small" style="margin-left: 12px;">功能开发中</el-text>
              </el-form-item>
              
              <el-form-item label="图表类型">
                <el-checkbox-group v-model="preferences.chartTypes" disabled>
                  <el-checkbox label="line">折线图</el-checkbox>
                  <el-checkbox label="candlestick">K线图</el-checkbox>
                  <el-checkbox label="bar">柱状图</el-checkbox>
                </el-checkbox-group>
                <el-text type="info" size="small" style="margin-left: 12px;">功能开发中</el-text>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>

        <!-- 订阅管理 -->
        <el-tab-pane label="订阅管理" name="subscriptions">
          <div class="tab-content">
            <el-form label-width="150px" class="subscriptions-form">
              <el-alert
                title="消息订阅说明"
                type="warning"
                description="开启订阅后，系统将通过站内消息、邮件等方式推送相关信息"
                :closable="false"
                show-icon
                class="security-alert"
              />
              
              <el-divider content-position="left">
                <span class="divider-title">市场资讯</span>
              </el-divider>
              
              <el-form-item label="每日市场概况">
                <el-switch v-model="subscriptions.dailyMarket" disabled />
                <el-text type="info" size="small" style="margin-left: 12px;">功能开发中</el-text>
              </el-form-item>
              
              <el-form-item label="重要公告推送">
                <el-switch v-model="subscriptions.announcements" disabled />
                <el-text type="info" size="small" style="margin-left: 12px;">功能开发中</el-text>
              </el-form-item>
              
              <el-divider content-position="left">
                <span class="divider-title">自选股提醒</span>
              </el-divider>
              
              <el-form-item label="价格异动提醒">
                <el-switch v-model="subscriptions.priceAlert" disabled />
                <el-text type="info" size="small" style="margin-left: 12px;">功能开发中</el-text>
              </el-form-item>
              
              <el-form-item label="成交量异动提醒">
                <el-switch v-model="subscriptions.volumeAlert" disabled />
                <el-text type="info" size="small" style="margin-left: 12px;">功能开发中</el-text>
              </el-form-item>
              
              <el-divider content-position="left">
                <span class="divider-title">系统通知</span>
              </el-divider>
              
              <el-form-item label="系统更新通知">
                <el-switch v-model="subscriptions.systemUpdate" disabled />
                <el-text type="info" size="small" style="margin-left: 12px;">功能开发中</el-text>
              </el-form-item>
            </el-form>
          </div>
        </el-tab-pane>

        <!-- 账户统计 -->
        <el-tab-pane label="账户统计" name="statistics">
          <div class="tab-content">
            <el-row :gutter="20" class="stats-cards">
              <el-col :xs="24" :sm="12" :md="6">
                <div class="stat-card">
                  <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <el-icon :size="30"><TrendCharts /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">--</div>
                    <div class="stat-label">查询次数</div>
                  </div>
                </div>
              </el-col>
              
              <el-col :xs="24" :sm="12" :md="6">
                <div class="stat-card">
                  <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
                    <el-icon :size="30"><Star /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">--</div>
                    <div class="stat-label">自选股数</div>
                  </div>
                </div>
              </el-col>
              
              <el-col :xs="24" :sm="12" :md="6">
                <div class="stat-card">
                  <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
                    <el-icon :size="30"><Clock /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">--</div>
                    <div class="stat-label">在线时长</div>
                  </div>
                </div>
              </el-col>
              
              <el-col :xs="24" :sm="12" :md="6">
                <div class="stat-card">
                  <div class="stat-icon" style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);">
                    <el-icon :size="30"><DocumentCopy /></el-icon>
                  </div>
                  <div class="stat-info">
                    <div class="stat-value">--</div>
                    <div class="stat-label">报告生成</div>
                  </div>
                </div>
              </el-col>
            </el-row>
            
            <el-divider content-position="left">
              <span class="divider-title">最近操作</span>
            </el-divider>
            
            <el-empty description="暂无操作记录" :image-size="120">
              <el-text type="info">功能开发中，敬请期待</el-text>
            </el-empty>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, FormInstance, FormRules } from 'element-plus'
import { getCurrentUser, updateUserProfile, updateUserAvatar, changePassword } from '@/api/user'
import { 
  User, Camera, Clock, Connection, Lock, Iphone, Message, Key,
  TrendCharts, Star, DocumentCopy, UserFilled
} from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import { useAuthStore } from '@/store/auth'
import type { UserRole } from '@/store/auth'

// 用户信息类型
interface UserInfo {
  id: number
  username: string
  role: UserRole
  avatar?: string
  nickname?: string
  phone?: string
  email?: string
  signature?: string
  created_at?: string
}

const authStore = useAuthStore()

// 用户信息
const userInfo = reactive<UserInfo>({
  id: 0,
  username: '',
  role: 'user',
  avatar: '',
  nickname: '',
  phone: '',
  email: '',
  signature: '',
  created_at: ''
})

// 当前激活的标签页
const activeTab = ref('profile')

// 个人资料表单
const profileForm = reactive({
  username: '',
  nickname: '',
  phone: '',
  email: '',
  signature: ''
})

const profileLoading = ref(false)

// 密码修改表单
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const passwordFormRef = ref<FormInstance>()
const passwordLoading = ref(false)

// 密码验证规则
const passwordRules = reactive<FormRules>({
  oldPassword: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (_rule, value, callback) => {
        if (value !== passwordForm.newPassword) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
})

// 获取角色显示名称
const getRoleDisplayName = (role: UserRole) => {
  return role === 'admin' ? '管理员' : '普通用户'
}

// 偏好设置
const preferences = reactive({
  theme: 'light',
  language: 'zh-CN',
  adjustType: '',
  chartTypes: ['line', 'candlestick']
})

// 订阅管理
const subscriptions = reactive({
  dailyMarket: false,
  announcements: false,
  priceAlert: false,
  volumeAlert: false,
  systemUpdate: false
})

// 格式化日期
const formatDate = (date: string | undefined) => {
  if (!date) return '未知'
  return dayjs(date).format('YYYY-MM-DD')
}

// 加载用户信息
const loadUserInfo = async () => {
  try {
    // 优先从后端获取最新用户信息，如果失败则回退到 store
    try {
      const res: any = await getCurrentUser()
      if (res) {
        const u = res as any
        Object.assign(userInfo, {
          id: u.id || 0,
          username: u.username,
          role: u.role,
          avatar: u.avatar || '',
          nickname: u.nickname || '',
          phone: u.phone || '',
          email: u.email || '',
          signature: u.signature || '',
          created_at: u.created_at || new Date().toISOString()
        })
        Object.assign(profileForm, {
          username: userInfo.username,
          nickname: userInfo.nickname || '',
          phone: userInfo.phone || '',
          email: userInfo.email || '',
          signature: userInfo.signature || ''
        })
        // 更新 store 中的用户信息副本
        authStore.user = authStore.user || {}
        authStore.user.username = userInfo.username
        authStore.user.role = userInfo.role as any
        authStore.user.avatar = userInfo.avatar
        authStore.user.email = userInfo.email
      } else {
        // 回退
        if (authStore.user) {
          Object.assign(userInfo, {
            id: 0,
            username: authStore.user.username,
            role: authStore.user.role,
            avatar: authStore.user.avatar || '',
            email: authStore.user.email || '',
            created_at: authStore.user.created_at || new Date().toISOString()
          })
          Object.assign(profileForm, {
            username: authStore.user.username,
            nickname: userInfo.nickname || '',
            phone: userInfo.phone || '',
            email: authStore.user.email || '',
            signature: userInfo.signature || ''
          })
        }
      }
    } catch (e) {
      // 若后端请求失败，使用 store 中已有信息
      if (authStore.user) {
        Object.assign(userInfo, {
          id: 0,
          username: authStore.user.username,
          role: authStore.user.role,
          avatar: authStore.user.avatar || '',
          email: authStore.user.email || '',
          created_at: authStore.user.created_at || new Date().toISOString()
        })
        Object.assign(profileForm, {
          username: authStore.user.username,
          nickname: userInfo.nickname || '',
          phone: userInfo.phone || '',
          email: authStore.user.email || '',
          signature: userInfo.signature || ''
        })
      }
    }
  } catch (error) {
    console.error('加载用户信息失败:', error)
    ElMessage.error('加载用户信息失败')
  }
}

// 处理头像上传
const handleAvatarUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }

  // 转换为Base64
  const reader = new FileReader()
  reader.onload = async (e) => {
    const avatar = e.target?.result as string
    try {
      // 调用接口上传 avatar（后端期望 base64 字符串）
      const resp: any = await updateUserAvatar({ avatar })
      // 更新本地和 store
      if (resp) {
        userInfo.avatar = resp.avatar || avatar
      } else {
        userInfo.avatar = avatar
      }
      // 让 authStore 刷新
      await authStore.fetchUser()
      ElMessage.success('头像上传成功')
    } catch (error) {
      console.error('头像上传失败:', error)
      ElMessage.error('头像上传失败')
    }
  }
  reader.readAsDataURL(file)
  
  return false // 阻止自动上传
}

// 更新个人资料
const handleUpdateProfile = async () => {
  profileLoading.value = true
  try {
    // 调用后端 API 更新资料
    const payload = {
      nickname: profileForm.nickname || undefined,
      phone: profileForm.phone || undefined,
      email: profileForm.email || undefined,
      signature: profileForm.signature || undefined
    }
    await updateUserProfile(payload)
    // 刷新 store 中用户信息
    await authStore.fetchUser()
    // 更新本地视图
    Object.assign(userInfo, {
      nickname: profileForm.nickname,
      phone: profileForm.phone,
      email: profileForm.email,
      signature: profileForm.signature
    })
    ElMessage.success('个人资料更新成功')
  } catch (error) {
    console.error('更新失败:', error)
    ElMessage.error('更新失败，请重试')
  } finally {
    profileLoading.value = false
  }
}

// 重置个人资料表单
const resetProfileForm = () => {
  Object.assign(profileForm, {
    username: userInfo.username,
    nickname: userInfo.nickname || '',
    phone: userInfo.phone || '',
    email: userInfo.email || '',
    signature: userInfo.signature || ''
  })
}

// 修改密码
const handleChangePassword = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    passwordLoading.value = true
    try {
      // 调用后端修改密码接口
      await changePassword({ old_password: passwordForm.oldPassword, new_password: passwordForm.newPassword })
      ElMessage.success('密码修改成功，请重新登录')
      resetPasswordForm()
      // 延迟后登出并跳转登录页
      setTimeout(() => {
        authStore.logout()
        window.location.href = '/login'
      }, 1500)
    } catch (error: any) {
      console.error('密码修改失败:', error)
      const msg = error?.response?.data?.detail || error?.message || '密码修改失败，请检查原密码是否正确'
      ElMessage.error(msg)
    } finally {
      passwordLoading.value = false
    }
  })
}

// 重置密码表单
const resetPasswordForm = () => {
  passwordForm.oldPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
  passwordFormRef.value?.resetFields()
}

onMounted(() => {
  loadUserInfo()
})
</script>

<style scoped>
.profile-container {
  animation: fadeIn 0.4s ease;
  padding: 0 16px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 头部卡片 */
.profile-header {
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}

.profile-header :deep(.el-card__body) {
  padding: 40px;
}

.header-content {
  display: flex;
  align-items: center;
  gap: 40px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.user-avatar {
  border: 4px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  color: #909399;
}

.avatar-upload :deep(.el-button) {
  border-radius: 20px;
}

.user-info {
  flex: 1;
  color: white;
  min-width: 0;
}

.username {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 16px 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  word-break: break-word;
}

.user-meta {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.user-meta .el-tag {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  backdrop-filter: blur(10px);
}

/* 标签页卡片 */
.tabs-card {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.profile-tabs :deep(.el-tabs__header) {
  margin-bottom: 24px;
}

.profile-tabs :deep(.el-tabs__item) {
  font-size: 15px;
  font-weight: 500;
}

.tab-content {
  padding: 20px;
  min-height: 400px;
}

/* 表单样式 */
.profile-form,
.security-form,
.preferences-form,
.subscriptions-form {
  max-width: 600px;
}

.security-alert {
  margin-bottom: 24px;
}

.divider-title {
  font-weight: 600;
  color: #409eff;
  font-size: 14px;
}

/* 统计卡片 */
.stats-cards {
  margin-bottom: 32px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  margin-bottom: 16px;
}

.stat-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  transform: translateY(-4px);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-info {
  flex: 1;
  min-width: 0;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.9rem;
  color: #909399;
}

/* 平板适配 (768px - 1024px) */
@media (max-width: 1024px) {
  .profile-header :deep(.el-card__body) {
    padding: 32px;
  }
  
  .header-content {
    gap: 30px;
  }
  
  .username {
    font-size: 1.75rem;
  }
  
  .tab-content {
    padding: 16px;
  }
}

/* 手机适配 (小于 768px) */
@media (max-width: 768px) {
  .profile-container {
    padding: 0 8px;
  }
  
  .profile-header {
    margin-bottom: 16px;
  }
  
  .profile-header :deep(.el-card__body) {
    padding: 24px 16px;
  }
  
  .header-content {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }
  
  .avatar-section {
    width: 100%;
  }
  
  .user-avatar {
    width: 100px !important;
    height: 100px !important;
  }
  
  .user-avatar :deep(.el-icon) {
    font-size: 50px !important;
  }
  
  .username {
    font-size: 1.5rem;
  }
  
  .user-meta {
    justify-content: center;
    font-size: 13px;
  }
  
  .user-meta :deep(.el-tag) {
    font-size: 12px;
    padding: 4px 8px;
  }
  
  .tab-content {
    padding: 12px 8px;
    min-height: 300px;
  }
  
  .profile-form,
  .security-form,
  .preferences-form,
  .subscriptions-form {
    max-width: 100%;
  }
  
  .profile-form :deep(.el-form-item__label),
  .security-form :deep(.el-form-item__label),
  .preferences-form :deep(.el-form-item__label),
  .subscriptions-form :deep(.el-form-item__label) {
    width: 80px !important;
    font-size: 14px;
  }
  
  .stat-card {
    padding: 16px;
  }
  
  .stat-icon {
    width: 50px;
    height: 50px;
  }
  
  .stat-icon :deep(.el-icon) {
    font-size: 24px;
  }
  
  .stat-value {
    font-size: 1.5rem;
  }
  
  .stat-label {
    font-size: 0.85rem;
  }
}

/* 超小屏幕适配 (小于 480px) */
@media (max-width: 480px) {
  .profile-header :deep(.el-card__body) {
    padding: 20px 12px;
  }
  
  .username {
    font-size: 1.3rem;
    margin-bottom: 12px;
  }
  
  .user-meta {
    gap: 8px;
  }
  
  .user-meta :deep(.el-tag) {
    font-size: 11px;
    padding: 3px 6px;
  }
  
  .profile-tabs :deep(.el-tabs__item) {
    font-size: 14px;
    padding: 0 12px;
  }
  
  .tab-content {
    padding: 8px 4px;
  }
  
  .profile-form :deep(.el-form-item__label),
  .security-form :deep(.el-form-item__label),
  .preferences-form :deep(.el-form-item__label),
  .subscriptions-form :deep(.el-form-item__label) {
    width: 70px !important;
    font-size: 13px;
  }
  
  .profile-form :deep(.el-input__inner),
  .security-form :deep(.el-input__inner) {
    font-size: 14px;
  }
  
  .security-alert {
    margin-bottom: 16px;
  }
  
  .security-alert :deep(.el-alert__title) {
    font-size: 13px;
  }
  
  .security-alert :deep(.el-alert__description) {
    font-size: 12px;
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
    padding: 12px;
  }
  
  .stat-info {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
}

/* 横屏模式优化 */
@media (max-height: 600px) and (orientation: landscape) {
  .profile-header :deep(.el-card__body) {
    padding: 20px;
  }
  
  .header-content {
    gap: 20px;
  }
  
  .user-avatar {
    width: 80px !important;
    height: 80px !important;
  }
  
  .username {
    font-size: 1.3rem;
    margin-bottom: 8px;
  }
  
  .tab-content {
    min-height: 250px;
  }
}
</style>
