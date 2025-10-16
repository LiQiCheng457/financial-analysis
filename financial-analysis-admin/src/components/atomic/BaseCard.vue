<template>
  <el-card 
    :class="['base-card', `base-card--${variant}`, { 'base-card--hover': hover }]"
    :shadow="shadow"
    :body-style="bodyStyle"
  >
    <template v-if="$slots.header" #header>
      <div class="base-card__header">
        <slot name="header" />
      </div>
    </template>

    <div class="base-card__body">
      <slot />
    </div>

    <template v-if="$slots.footer">
      <div class="base-card__footer">
        <slot name="footer" />
      </div>
    </template>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'default' | 'gradient' | 'flat'
  shadow?: 'always' | 'hover' | 'never'
  hover?: boolean
  padding?: string
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default',
  shadow: 'hover',
  hover: false,
  padding: '24px'
})

const bodyStyle = computed(() => ({
  padding: props.padding
}))
</script>

<style scoped lang="scss">
.base-card {
  transition: all 0.3s ease;

  &--default {
    background: linear-gradient(to bottom, #ffffff 0%, #fafbfc 100%);
  }

  &--gradient {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
  }

  &--flat {
    background: #ffffff;
    border: 1px solid #e4e7ed;
  }

  &--hover:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
  }

  &__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  &__body {
    min-height: 60px;
  }

  &__footer {
    padding-top: 16px;
    margin-top: 16px;
    border-top: 1px solid #e4e7ed;
  }
}
</style>
