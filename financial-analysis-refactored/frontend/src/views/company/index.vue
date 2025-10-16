<template>
  <div class="company-page">
    <div class="page-header">
      <h1>公司查询</h1>
      <p>搜索和筛选上市公司信息</p>
    </div>

    <CompanySearchPanel @search="handleSearch" />

    <BaseEmpty v-if="!hasSearched" description="请输入关键词或选择行业标签进行搜索" />
    
    <div v-else class="results-section">
      <BaseCard title="搜索结果">
        <p>搜索功能开发中...</p>
      </BaseCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BaseCard from '@/components/atomic/BaseCard.vue'
import BaseEmpty from '@/components/atomic/BaseEmpty.vue'
import CompanySearchPanel from '@/components/business/company/CompanySearchPanel.vue'

const hasSearched = ref(false)

const handleSearch = (params: any) => {
  console.log('搜索参数:', params)
  hasSearched.value = true
}
</script>

<style scoped lang="scss">
.company-page {
  min-height: 100vh;
  padding: 20px;
  background: #f5f7fa;

  .page-header {
    text-align: center;
    margin-bottom: 30px;

    h1 {
      font-size: 32px;
      color: #333;
      margin-bottom: 10px;
    }

    p {
      font-size: 16px;
      color: #666;
    }
  }

  .results-section {
    max-width: 1200px;
    margin: 30px auto;
  }
}
</style>
