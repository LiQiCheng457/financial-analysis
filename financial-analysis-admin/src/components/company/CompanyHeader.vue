<template>
  <div class="company-header">
    <h1 class="company-main-title">{{ companyName }}</h1>
    <div class="company-subtitle">
      <span class="english-name">{{ englishName || '—' }}</span>
      <span class="stock-code">{{ stockCode || '—' }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

const props = defineProps<{
  companyName: string,
  englishName?: string | null,
  stockCode?: string | null
}>()
</script>

<style scoped>
.company-header {
  padding: 24px 24px 20px 24px;
  border-bottom: 1px solid #e5e5e5;
  text-align: center;
}

.company-main-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0 0 12px 0;
  line-height: 1.3;
}

.company-subtitle {
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 12px;
  font-size: 1.05rem;
}

.english-name {
  color: #666;
  font-style: italic;
}

.stock-code {
  color: #1890ff;
  font-family: 'Consolas', 'Monaco', monospace;
  font-weight: 600;
  font-size: 1rem;
  letter-spacing: 0.5px;
}
</style>