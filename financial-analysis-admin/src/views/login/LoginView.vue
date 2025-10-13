<template>
  <div class="login-container">
    <div class="login-left">
      <div class="login-left-intro">
        <img src="@/assets/svgs/login-box-bg.svg" alt="intro" class="intro-image" />
        <h2 class="intro-title">欢迎使用</h2>
        <p class="intro-description">一个强大的金融分析工具</p>
      </div>
    </div>
    <div class="login-right">
      <div class="login-form-wrapper">
        <h2 class="form-title">{{ isLogin ? '登录' : '注册' }}</h2>
        
        <!-- 登录表单 -->
        <el-form
          v-if="isLogin"
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          @submit.prevent="handleLogin"
        >
          <el-form-item prop="username">
            <el-input v-model="loginForm.username" placeholder="请输入用户名" size="large"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              show-password
              size="large"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" native-type="submit" class="login-button" size="large">登录</el-button>
          </el-form-item>
          <div class="form-footer">
            <el-link type="primary" @click="isLogin = false">没有账户？去注册</el-link>
          </div>
        </el-form>

        <!-- 注册表单 -->
        <el-form
          v-else
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerRules"
          @submit.prevent="handleRegister"
        >
          <el-form-item prop="username">
            <el-input v-model="registerForm.username" placeholder="用户名长度至少3位" size="large"></el-input>
          </el-form-item>
          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="密码长度至少6位"
              show-password
              size="large"
            ></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" native-type="submit" class="login-button" size="large">注册</el-button>
          </el-form-item>
          <div class="form-footer">
            <el-link type="primary" @click="isLogin = true">已有账户？去登录</el-link>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()

const loginFormRef = ref<FormInstance>()
const registerFormRef = ref<FormInstance>()

const isLogin = ref(true)

const loginForm = reactive({
  username: '',
  password: ''
})

const registerForm = reactive({
  username: '',
  password: ''
})

const loginRules = reactive<FormRules>({
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
})

const registerRules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名长度至少为3个字符', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少为6个字符', trigger: 'blur' },
  ],
})

const handleLogin = async () => {
  if (!loginFormRef.value) return
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await authStore.login(loginForm)
        await router.push('/')
      } catch (error) {
        ElMessage.error('登录失败，请检查用户名和密码')
      }
    }
  })
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await authStore.register(registerForm)
        ElMessage.success('注册成功，请登录')
        isLogin.value = true // 注册成功后切换到登录视图
        // 重置表单
        registerForm.username = ''
        registerForm.password = ''
      } catch (error: any) {
        if (error.response && error.response.data && error.response.data.detail) {
            const errorMsg = error.response.data.detail;
            if (typeof errorMsg === 'string') {
                 ElMessage.error(errorMsg);
            } else {
                 ElMessage.error('注册失败，请检查输入');
            }
        } else {
          ElMessage.error('注册失败，用户名可能已被占用')
        }
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  display: flex;
  width: 100vw;
  height: 100vh;
  overflow: hidden;
}

.login-left {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: url('@/assets/svgs/login-bg.svg');
  background-size: cover;
  background-position: center;
  position: relative;
}

.login-left-intro {
  text-align: center;
  color: white;
  z-index: 1;
}

.intro-image {
  width: 350px;
  margin-bottom: 20px;
}

.intro-title {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.intro-description {
  font-size: 1.2rem;
}

.login-right {
  width: 500px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
}

.login-form-wrapper {
  width: 320px;
  padding: 20px;
}

.form-title {
  font-size: 1.8rem;
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.login-button {
  width: 100%;
}

.form-footer {
  text-align: right;
  margin-top: 10px;
}

/* 响应式设计：在小屏幕上隐藏左侧 */
@media (max-width: 992px) {
  .login-left {
    display: none;
  }
  .login-right {
    width: 100%;
  }
}
</style>


