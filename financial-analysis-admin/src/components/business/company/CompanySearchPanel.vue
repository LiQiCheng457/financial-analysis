<template>
  <div class="company-search-panel">
    <!-- 搜索栏 -->
    <div class="search-bar">
      <el-input
        v-model="searchQuery"
        :placeholder="placeholder"
        :prefix-icon="Search"
        clearable
        size="large"
        class="search-input"
        @input="handleSearch"
        @clear="handleClear"
      >
        <template #append>
          <el-button :icon="Search" @click="handleSearchClick">搜索</el-button>
        </template>
      </el-input>
    </div>

    <!-- 行业标签 -->
    <div v-if="showIndustryTags" class="industry-tags">
      <div class="tags-header">
        <span class="tags-title">
          <el-icon><Collection /></el-icon>
          行业筛选
        </span>
        <el-button
          v-if="selectedIndustries.length > 0"
          text
          type="primary"
          @click="clearIndustries"
        >
          清空筛选
        </el-button>
      </div>

      <div class="tags-groups">
        <div
          v-for="group in industryGroups"
          :key="group.name"
          class="tag-group"
        >
          <div class="group-name" :style="{ color: group.color }">
            {{ group.name }}
          </div>
          <div class="group-tags">
            <el-checkbox-group v-model="selectedIndustries">
              <el-checkbox
                v-for="tag in group.tags"
                :key="tag"
                :label="tag"
                :style="{ '--tag-color': group.color }"
                class="industry-tag"
              >
                {{ tag }}
              </el-checkbox>
            </el-checkbox-group>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { Search, Collection } from '@element-plus/icons-vue'
import { useDebounceFn } from '@vueuse/core'

interface IndustryGroup {
  name: string
  color: string
  tags: string[]
}

interface Props {
  placeholder?: string
  showIndustryTags?: boolean
  industryGroups?: IndustryGroup[]
  debounceTime?: number
}

interface Emits {
  (e: 'search', query: string, industries: string[]): void
  (e: 'clear'): void
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: '请输入股票代码、公司名称...',
  showIndustryTags: true,
  debounceTime: 300
})

const emit = defineEmits<Emits>()

const searchQuery = ref('')
const selectedIndustries = ref<string[]>([])

// 监听行业标签变化，自动更新搜索框
watch(selectedIndustries, (newVal) => {
  if (newVal.length > 0) {
    searchQuery.value = newVal.join('+')
  }
}, { deep: true })

// 防抖搜索
const handleSearch = useDebounceFn(() => {
  // 如果搜索框内容和标签一致，则清空搜索框，只用标签
  const tagStr = selectedIndustries.value.join('+')
  const query = searchQuery.value === tagStr ? '' : searchQuery.value
  emit('search', query, selectedIndustries.value)
}, props.debounceTime)

const handleSearchClick = () => {
  const tagStr = selectedIndustries.value.join('+')
  const query = searchQuery.value === tagStr ? '' : searchQuery.value
  emit('search', query, selectedIndustries.value)
}

const handleClear = () => {
  searchQuery.value = ''
  selectedIndustries.value = []
  emit('clear')
}

const clearIndustries = () => {
  selectedIndustries.value = []
  searchQuery.value = ''
}
</script>

<style scoped lang="scss">
.company-search-panel {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.search-bar {
  margin-bottom: 24px;

  .search-input {
    :deep(.el-input__wrapper) {
      padding: 12px 16px;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
      transition: all 0.3s;

      &:hover {
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.2);
      }
    }
  }
}

.industry-tags {
  .tags-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 2px solid #f0f0f0;

    .tags-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 1.1rem;
      font-weight: 600;
      color: #2c3e50;
    }
  }

  .tags-groups {
    .tag-group {
      margin-bottom: 20px;

      &:last-child {
        margin-bottom: 0;
      }

      .group-name {
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 10px;
        padding-left: 12px;
        border-left: 3px solid currentColor;
      }

      .group-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;

        .industry-tag {
          :deep(.el-checkbox__label) {
            padding: 6px 12px;
            border-radius: 6px;
            background: rgba(0, 0, 0, 0.02);
            transition: all 0.3s;
          }

          :deep(.el-checkbox__input.is-checked + .el-checkbox__label) {
            background: var(--tag-color);
            color: white;
          }

          &:hover {
            :deep(.el-checkbox__label) {
              background: rgba(0, 0, 0, 0.05);
            }
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .company-search-panel {
    padding: 16px;
  }

  .tags-groups {
    .tag-group {
      .group-tags {
        gap: 6px;

        .industry-tag {
          :deep(.el-checkbox__label) {
            padding: 4px 10px;
            font-size: 0.85rem;
          }
        }
      }
    }
  }
}
</style>
