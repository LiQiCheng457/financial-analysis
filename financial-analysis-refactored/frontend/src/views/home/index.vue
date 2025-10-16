<template>
  <div class="home-page">
    <div class="header">
      <h1>🚀 金融分析系统 - 重构版</h1>
      <p class="version">v2.0.0</p>
    </div>

    <BaseCard title="欢迎使用" variant="gradient" class="welcome-card">
      <p>这是完整重构的金融分析平台，采用现代化架构和最佳实践。</p>
      <div class="features">
        <div class="feature-item">
          <el-icon><Checked /></el-icon>
          <span>Vue 3 Composition API</span>
        </div>
        <div class="feature-item">
          <el-icon><Checked /></el-icon>
          <span>TypeScript 类型安全</span>
        </div>
        <div class="feature-item">
          <el-icon><Checked /></el-icon>
          <span>模块化组件设计</span>
        </div>
        <div class="feature-item">
          <el-icon><Checked /></el-icon>
          <span>FastAPI 高性能后端</span>
        </div>
      </div>
    </BaseCard>

    <div class="navigation">
      <BaseCard title="快速导航" class="nav-card">
        <div class="nav-links">
          <el-button type="primary" @click="router.push('/company')">
            <el-icon><Search /></el-icon>
            公司查询
          </el-button>
          <el-button type="success" @click="router.push('/market')">
            <el-icon><TrendCharts /></el-icon>
            市场概况
          </el-button>
          <el-button type="info" @click="router.push('/user')">
            <el-icon><User /></el-icon>
            用户中心
          </el-button>
        </div>
      </BaseCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import BaseCard from '@/components/atomic/BaseCard.vue'
import { Checked, Search, TrendCharts, User } from '@element-plus/icons-vue'

const router = useRouter()
</script>

<style scoped lang="scss">
.home-page {
  min-height: 100vh;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

  .header {
    text-align: center;
    margin-bottom: 40px;
    color: white;

    h1 {
      font-size: 48px;
      margin-bottom: 10px;
      text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }

    .version {
      font-size: 18px;
      opacity: 0.9;
    }
  }

  .welcome-card {
    max-width: 800px;
    margin: 0 auto 30px;

    p {
      font-size: 16px;
      line-height: 1.6;
      color: #666;
      margin-bottom: 20px;
    }

    .features {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 15px;

      .feature-item {
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 10px;
        background: #f5f7fa;
        border-radius: 8px;
        transition: all 0.3s;

        &:hover {
          background: #e8f4ff;
          transform: translateX(5px);
        }

        .el-icon {
          color: #67c23a;
          font-size: 20px;
        }

        span {
          font-size: 14px;
          color: #333;
        }
      }
    }
  }

  .navigation {
    max-width: 800px;
    margin: 0 auto;

    .nav-card {
      .nav-links {
        display: flex;
        gap: 15px;
        justify-content: center;
        flex-wrap: wrap;

        .el-button {
          flex: 1;
          min-width: 150px;
          height: 50px;
          font-size: 16px;
        }
      }
    }
  }
}
</style>
