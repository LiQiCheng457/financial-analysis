<template>
  <div class="not-found-page">
    <div class="content">
      <h1 class="error-code">404</h1>
      <p class="error-message">页面未找到</p>
      <el-button type="primary" @click="router.push('/')">
        返回首页
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped lang="scss">
.not-found-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

  .content {
    text-align: center;
    color: white;

    .error-code {
      font-size: 120px;
      font-weight: bold;
      margin-bottom: 20px;
      text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
    }

    .error-message {
      font-size: 24px;
      margin-bottom: 30px;
    }

    .el-button {
      font-size: 16px;
      padding: 12px 30px;
    }
  }
}
</style>
