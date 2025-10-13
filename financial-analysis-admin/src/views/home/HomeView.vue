<template>
  <div class="home">
    <h1>欢迎来到金融分析项目主界面</h1>
    <p>这里是主内容区域。</p>
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
