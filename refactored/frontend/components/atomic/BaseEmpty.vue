<template>
  <div :class="['base-empty', `base-empty--${size}`]">
    <div class="base-empty__icon">
      <component v-if="icon" :is="icon" :size="iconSize" />
      <span v-else class="emoji">{{ emoji }}</span>
    </div>
    
    <div class="base-empty__text">{{ text }}</div>
    
    <div v-if="description" class="base-empty__description">
      {{ description }}
    </div>

    <div v-if="$slots.action" class="base-empty__action">
      <slot name="action" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Component } from 'vue'

interface Props {
  icon?: Component
  emoji?: string
  text?: string
  description?: string
  size?: 'small' | 'default' | 'large'
}

const props = withDefaults(defineProps<Props>(), {
  emoji: '📭',
  text: '暂无数据',
  size: 'default'
})

const iconSize = computed(() => {
  const sizeMap = {
    small: 60,
    default: 80,
    large: 120
  }
  return sizeMap[props.size]
})
</script>

<style scoped lang="scss">
.base-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #909399;

  &--small {
    padding: 40px 20px;
    
    .base-empty__icon {
      font-size: 3rem;
    }
  }

  &--large {
    padding: 80px 20px;
    
    .base-empty__icon {
      font-size: 7rem;
    }
  }

  &__icon {
    font-size: 5rem;
    margin-bottom: 16px;
    opacity: 0.6;
    animation: float 3s ease-in-out infinite;

    .emoji {
      display: block;
    }
  }

  &__text {
    font-size: 1.1rem;
    color: #606266;
    margin-bottom: 8px;
    font-weight: 500;
  }

  &__description {
    font-size: 0.9rem;
    color: #909399;
    margin-bottom: 24px;
    text-align: center;
    max-width: 400px;
    line-height: 1.6;
  }

  &__action {
    margin-top: 16px;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}
</style>
