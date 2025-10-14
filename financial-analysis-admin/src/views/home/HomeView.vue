<template>
  <div class="home">
    <h1>欢迎来到证券分析项目主界面</h1>
    <stock-chart />
  </div>
</template>

<script lang="ts" setup>
import StockChart from '@/components/StockChart.vue'
</script>

<script lang="ts">
export default {
  components: { StockChart }
}
</script>
