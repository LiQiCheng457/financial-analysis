<template>
  <div class="page-shell">
    <div class="page-header">
      <h2><slot name="title">页面标题</slot></h2>
      <div class="actions"><slot name="actions" /></div>
    </div>
    <div class="page-body">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.page-shell { padding: 16px }
.page-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:12px }
.page-body { background:#fff; padding:12px; border-radius:6px }
</style>
