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
        ElMessage.success(`欢迎回来，${authStore.user?.username}！`)
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
  padding: 20px;
}

.intro-image {
  width: 350px;
  max-width: 80%;
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
  padding: 20px;
  box-sizing: border-box;
}

.login-form-wrapper {
  width: 360px;
  max-width: 100%;
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

/* 平板横屏 (768px - 1024px) */
@media (max-width: 1024px) {
  .intro-image {
    width: 280px;
  }
  
  .intro-title {
    font-size: 2rem;
  }
  
  .intro-description {
    font-size: 1rem;
  }
  
  .login-right {
    width: 450px;
  }
  
  .login-form-wrapper {
    width: 320px;
  }
}

/* 平板竖屏和手机横屏 (小于 992px) */
@media (max-width: 992px) {
  .login-left {
    display: none;
  }
  
  .login-right {
    width: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
  
  .login-form-wrapper {
    background: white;
    border-radius: 12px;
    padding: 30px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  }
}

/* 手机竖屏 (小于 768px) */
@media (max-width: 768px) {
  .login-right {
    padding: 16px;
  }
  
  .login-form-wrapper {
    width: 100%;
    max-width: 400px;
    padding: 24px;
  }
  
  .form-title {
    font-size: 1.5rem;
    margin-bottom: 24px;
  }
}

/* 超小屏幕 (小于 480px) */
@media (max-width: 480px) {
  .login-right {
    padding: 12px;
  }
  
  .login-form-wrapper {
    padding: 20px;
  }
  
  .form-title {
    font-size: 1.3rem;
    margin-bottom: 20px;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 18px;
  }
  
  :deep(.el-input__inner) {
    font-size: 14px;
  }
}

/* 横屏模式优化 */
@media (max-height: 600px) and (orientation: landscape) {
  .login-container {
    overflow-y: auto;
  }
  
  .login-right {
    padding: 12px;
  }
  
  .login-form-wrapper {
    padding: 16px;
  }
  
  .form-title {
    font-size: 1.3rem;
    margin-bottom: 16px;
  }
  
  :deep(.el-form-item) {
    margin-bottom: 12px;
  }
}
</style>


