<template>
  <PageShell>
    <template #title> 个股快照 </template>
    <template #actions>
      <el-button size="small">刷新</el-button>
    </template>

    <div>
      <p>此页面为占位组件，后续实现个股快照功能。</p>
    </div>
  </PageShell>
</template>

<script setup lang="ts">
import PageShell from '@/components/PageShell.vue'
import { ElButton } from 'element-plus'
</script>
