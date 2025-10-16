<template>
  <PlaceholderView
    title="⭐ 自选股管理"
    icon="⭐"
    description="添加、编辑、删除自选股，打造个性化投资池"
    :features="[
      '快速添加：搜索添加股票到自选股列表',
      '实时行情：自选股实时价格和涨跌幅展示',
      '批注备忘：为每只股票添加个人备注和标签',
      '排序筛选：按涨跌幅、市值、自定义排序',
      '一键同步：自选股数据云端同步，多端共享'
    ]"
  />
</template>

<script setup lang="ts">
import PlaceholderView from '@/components/PlaceholderView.vue'
</script>
