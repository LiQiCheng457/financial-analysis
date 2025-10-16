<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

onMounted(() => {
  console.log('金融分析系统 - 重构版 v2.0.0')
})
</script>

<style scoped>
#app {
  width: 100%;
  height: 100%;
}
</style>
