# 前端代码规范文档

## 📁 目录结构规范

```
src/
├── api/              # API 接口层
│   ├── stock.ts      # 股票相关接口
│   ├── user.ts       # 用户相关接口
│   └── admin.ts      # 管理相关接口
├── assets/           # 静态资源
├── components/       # 组件
│   ├── atomic/       # 原子组件（基础UI）
│   ├── business/     # 业务组件
│   └── ...           # 其他通用组件
├── composables/      # 组合式函数（Hooks）
├── layout/           # 布局组件
├── router/           # 路由配置
├── store/            # 状态管理
├── styles/           # 全局样式
├── types/            # TypeScript 类型定义
├── utils/            # 工具函数
├── views/            # 页面视图
├── App.vue           # 根组件
└── main.ts           # 入口文件
```

## 📝 命名规范

### 1. 文件命名

- **组件文件**: 使用 PascalCase (大驼峰)
  - 示例: `StockChart.vue`, `UserProfile.vue`
  
- **工具/API 文件**: 使用 camelCase (小驼峰)
  - 示例: `request.ts`, `formatDate.ts`
  
- **类型定义文件**: 使用 camelCase
  - 示例: `stock.ts`, `user.ts`

### 2. 组件命名

- 组件名必须使用多个单词（避免与 HTML 元素冲突）
- 使用 PascalCase
- 示例: `PageShell`, `StockSearch`, `TechnicalChart`

### 3. 变量/函数命名

- **变量**: camelCase
  ```typescript
  const userName = 'John'
  const stockList = []
  ```

- **常量**: UPPER_SNAKE_CASE
  ```typescript
  const API_BASE_URL = '/api'
  const MAX_RETRY_COUNT = 3
  ```

- **函数**: camelCase，使用动词开头
  ```typescript
  const getUserInfo = () => {}
  const formatDate = () => {}
  ```

- **布尔变量**: is/has/can 开头
  ```typescript
  const isLoading = ref(false)
  const hasPermission = computed(() => true)
  ```

## 🎨 Vue 组件规范

### 1. 组件结构顺序

```vue
<template>
  <!-- 模板内容 -->
</template>

<script setup lang="ts">
// 1. 导入
import { ref, computed, onMounted } from 'vue'
import type { ComponentType } from '@/types'

// 2. Props 定义
interface Props {
  title?: string
  data: ComponentType[]
}
const props = withDefaults(defineProps<Props>(), {
  title: '默认标题'
})

// 3. Emits 定义
interface Emits {
  (e: 'update', value: string): void
  (e: 'delete', id: number): void
}
const emit = defineEmits<Emits>()

// 4. 响应式数据
const loading = ref(false)
const list = ref<ComponentType[]>([])

// 5. 计算属性
const filteredList = computed(() => {
  return list.value.filter(item => item.active)
})

// 6. 方法
const fetchData = async () => {
  loading.value = true
  // ...
  loading.value = false
}

// 7. 生命周期
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
/* 样式 */
</style>
```

### 2. Props 规范

```typescript
// ✅ 推荐：使用 TypeScript 接口定义
interface Props {
  title?: string
  count: number
  items: Array<{ id: number; name: string }>
}

const props = withDefaults(defineProps<Props>(), {
  title: '默认标题'
})

// ❌ 不推荐：使用运行时声明
const props = defineProps({
  title: String,
  count: Number
})
```

### 3. Emits 规范

```typescript
// ✅ 推荐：使用 TypeScript 定义
interface Emits {
  (e: 'update:modelValue', value: string): void
  (e: 'submit', data: FormData): void
}

const emit = defineEmits<Emits>()

// ❌ 不推荐：数组形式
const emit = defineEmits(['update:modelValue', 'submit'])
```

### 4. 模板规范

```vue
<!-- ✅ 推荐：属性过多时换行 -->
<el-button
  type="primary"
  :loading="loading"
  @click="handleSubmit"
>
  提交
</el-button>

<!-- ✅ 推荐：使用自闭合标签 -->
<StockChart :data="chartData" />
<el-input v-model="query" />

<!-- ❌ 不推荐：不自闭合 -->
<StockChart :data="chartData"></StockChart>
<el-input v-model="query"></el-input>

<!-- ✅ 推荐：v-for 必须带 key -->
<div v-for="item in items" :key="item.id">
  {{ item.name }}
</div>

<!-- ✅ 推荐：v-if 与 v-for 不同时使用 -->
<template v-if="showList">
  <div v-for="item in items" :key="item.id">
    {{ item.name }}
  </div>
</template>
```

## 📦 API 层规范

### 1. API 函数定义

```typescript
// stock.ts

import request from '@/utils/request'
import type { StockInfo, StockHistoryData } from '@/types'

/**
 * 获取股票历史数据
 * @param params 查询参数
 */
export interface GetStockHistoryParams {
  code: string
  start_date?: string
  end_date?: string
  adjust?: '' | 'qfq' | 'hfq'
}

export const getStockHistory = (params: GetStockHistoryParams) => {
  return request<StockHistoryData[]>({
    url: '/stocks/history',
    method: 'get',
    params
  })
}
```

### 2. 统一导出

```typescript
// api/index.ts

export * from './stock'
export * from './user'
export * from './admin'
```

## 🗂️ Store 规范

```typescript
import { defineStore } from 'pinia'
import type { User } from '@/types'

interface AuthState {
  token: string | null
  user: User | null
}

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    token: localStorage.getItem('token'),
    user: null
  }),

  getters: {
    isAuthenticated: (state): boolean => !!state.token,
    isAdmin: (state): boolean => state.user?.role === 'admin'
  },

  actions: {
    async login (credentials: LoginCredentials) {
      // ...
    },

    logout () {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    }
  }
})
```

## 🎯 TypeScript 规范

### 1. 类型定义

```typescript
// ✅ 推荐：使用 interface
interface User {
  id: number
  name: string
  email?: string
}

// ✅ 推荐：使用 type 定义联合类型
type Status = 'pending' | 'success' | 'error'

// ✅ 推荐：泛型使用
const fetchData = <T>(url: string): Promise<T> => {
  return request<T>({ url, method: 'get' })
}
```

### 2. 避免 any

```typescript
// ❌ 不推荐
const data: any = {}

// ✅ 推荐：使用具体类型
const data: Record<string, unknown> = {}

// ✅ 推荐：使用泛型
const data: T = {}
```

## 🎨 样式规范

### 1. 使用 scoped

```vue
<style scoped>
/* 组件内样式，避免污染全局 */
.container {
  padding: 20px;
}
</style>
```

### 2. BEM 命名

```vue
<template>
  <div class="stock-chart">
    <div class="stock-chart__header">
      <h3 class="stock-chart__title">标题</h3>
    </div>
    <div class="stock-chart__body">
      <!-- 内容 -->
    </div>
  </div>
</template>

<style scoped>
.stock-chart {
  /* 块 */
}

.stock-chart__header {
  /* 元素 */
}

.stock-chart__title {
  /* 元素 */
}

.stock-chart--large {
  /* 修饰符 */
}
</style>
```

### 3. CSS 变量

```css
/* styles/variables.css */
:root {
  --primary-color: #409eff;
  --success-color: #67c23a;
  --warning-color: #e6a23c;
  --danger-color: #f56c6c;
  --text-primary: #303133;
  --text-regular: #606266;
  --border-color: #dcdfe6;
  --border-radius: 4px;
}
```

## 📋 注释规范

### 1. 函数注释

```typescript
/**
 * 获取股票历史数据
 * @param code 股票代码
 * @param startDate 开始日期
 * @param endDate 结束日期
 * @returns 股票历史数据数组
 */
export const getStockHistory = (
  code: string,
  startDate: string,
  endDate: string
): Promise<StockHistoryData[]> => {
  // ...
}
```

### 2. 组件注释

```vue
<template>
  <!-- 股票搜索组件 - 支持代码和名称搜索 -->
  <el-autocomplete
    v-model="query"
    :fetch-suggestions="handleSearch"
  />
</template>
```

### 3. TODO 注释

```typescript
// TODO: 需要优化查询性能
// FIXME: 修复日期格式化问题
// NOTE: 注意这里的边界情况
```

## ✅ 代码检查

### 1. ESLint

```bash
# 检查代码
pnpm run lint

# 自动修复
pnpm run lint --fix
```

### 2. Prettier

```bash
# 格式化代码
pnpm run format
```

### 3. TypeScript

```bash
# 类型检查
vue-tsc --noEmit
```

## 🚀 最佳实践

### 1. 组合式函数 (Composables)

```typescript
// composables/useStockData.ts

import { ref, onMounted } from 'vue'
import { getStockHistory } from '@/api'
import type { StockHistoryData } from '@/types'

export const useStockData = (code: string) => {
  const loading = ref(false)
  const data = ref<StockHistoryData[]>([])
  const error = ref<string | null>(null)

  const fetchData = async () => {
    loading.value = true
    error.value = null

    try {
      data.value = await getStockHistory({ code })
    } catch (e) {
      error.value = e instanceof Error ? e.message : '获取数据失败'
    } finally {
      loading.value = false
    }
  }

  onMounted(() => {
    fetchData()
  })

  return {
    loading,
    data,
    error,
    fetchData
  }
}
```

### 2. 错误处理

```typescript
// ✅ 推荐：统一错误处理
try {
  const result = await apiCall()
  // 处理成功
} catch (error) {
  if (error instanceof Error) {
    ElMessage.error(error.message)
  } else {
    ElMessage.error('操作失败')
  }
}

// ✅ 推荐：使用 finally 清理
try {
  loading.value = true
  await apiCall()
} catch (error) {
  handleError(error)
} finally {
  loading.value = false
}
```

### 3. 性能优化

```typescript
// ✅ 推荐：使用 computed 缓存计算结果
const filteredList = computed(() => {
  return list.value.filter(item => item.active)
})

// ✅ 推荐：使用 v-show 而非 v-if（频繁切换时）
<div v-show="isVisible">内容</div>

// ✅ 推荐：列表使用虚拟滚动（大数据量）
<el-table-v2 :data="largeList" />
```

## 📚 参考资源

- [Vue 3 官方文档](https://cn.vuejs.org/)
- [Vue 风格指南](https://cn.vuejs.org/style-guide/)
- [TypeScript 官方文档](https://www.typescriptlang.org/)
- [Element Plus 组件库](https://element-plus.org/)
- [ESLint 规则](https://eslint.org/docs/rules/)
- [Prettier 配置](https://prettier.io/docs/en/options.html)
