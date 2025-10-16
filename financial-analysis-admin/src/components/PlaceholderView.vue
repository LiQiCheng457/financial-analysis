<template>
  <PageShell>
    <template #title>{{ title }}</template>
    <template #actions>
      <el-button size="small" type="primary" disabled>
        <el-icon><Plus /></el-icon>
        功能开发中
      </el-button>
    </template>

    <div class="placeholder-container">
      <div class="placeholder-card">
        <div class="placeholder-icon">{{ icon }}</div>
        <h2 class="placeholder-title">{{ title }}</h2>
        <p class="placeholder-desc">{{ description }}</p>
        <div class="placeholder-features">
          <div v-for="(feature, index) in features" :key="index" class="feature-item">
            <el-icon class="feature-icon"><Check /></el-icon>
            <span>{{ feature }}</span>
          </div>
        </div>
        <div class="placeholder-status">
          <el-tag type="warning" effect="dark">功能开发中</el-tag>
          <span class="status-text">敬请期待</span>
        </div>
      </div>
    </div>
  </PageShell>
</template>

<script setup lang="ts">
import { Check, Plus } from '@element-plus/icons-vue'
import PageShell from '@/components/PageShell.vue'

defineProps<{
  title: string
  icon: string
  description: string
  features: string[]
}>()
</script>

<style scoped>
.placeholder-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  padding: 40px 20px;
}

.placeholder-card {
  background: linear-gradient(to bottom, #ffffff 0%, #fafbfc 100%);
  border-radius: 20px;
  padding: 60px 40px;
  max-width: 600px;
  width: 100%;
  text-align: center;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

.placeholder-icon {
  font-size: 6rem;
  margin-bottom: 24px;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
}

.placeholder-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.placeholder-desc {
  font-size: 1.1rem;
  color: #5a6c7d;
  margin-bottom: 32px;
  line-height: 1.6;
}

.placeholder-features {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 32px;
  text-align: left;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 0;
  color: #2c3e50;
  font-size: 1rem;
  border-bottom: 1px dashed #e4e7ed;
}

.feature-item:last-child {
  border-bottom: none;
}

.feature-icon {
  color: #67c23a;
  font-size: 1.2rem;
  flex-shrink: 0;
}

.placeholder-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.status-text {
  color: #909399;
  font-size: 0.95rem;
}

@media (max-width: 768px) {
  .placeholder-card {
    padding: 40px 24px;
  }
  
  .placeholder-icon {
    font-size: 4rem;
  }
  
  .placeholder-title {
    font-size: 1.6rem;
  }
  
  .placeholder-desc {
    font-size: 1rem;
  }
}
</style>
