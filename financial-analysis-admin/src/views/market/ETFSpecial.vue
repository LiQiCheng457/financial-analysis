<template>
  <div class="etf-special-page">
    <el-card class="header-card">
      <div class="page-header">
        <div class="header-left">
          <h2 class="page-title">📊 ETF专题</h2>
          <p class="page-subtitle">交易型开放式指数基金分析</p>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="refreshData">
            <el-icon><RefreshRight /></el-icon>
            刷新数据
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- ETF市场概览 -->
    <el-row :gutter="20" class="overview-section">
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">ETF总数</div>
              <div class="stat-value">{{ overview.totalCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%)">
              <el-icon><Money /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">总市值（亿元）</div>
              <div class="stat-value">{{ overview.totalMarketCap }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)">
              <el-icon><CaretTop /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">上涨数量</div>
              <div class="stat-value rising">{{ overview.risingCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%)">
              <el-icon><CaretBottom /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-label">下跌数量</div>
              <div class="stat-value falling">{{ overview.fallingCount }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- ETF分类导航 -->
    <el-card class="category-card">
      <div class="category-header">
        <h3>ETF分类</h3>
      </div>
      <el-radio-group v-model="selectedCategory" class="category-group" @change="onCategoryChange">
        <el-radio-button label="all">全部</el-radio-button>
        <el-radio-button label="stock">股票型</el-radio-button>
        <el-radio-button label="bond">债券型</el-radio-button>
        <el-radio-button label="commodity">商品型</el-radio-button>
        <el-radio-button label="currency">货币型</el-radio-button>
        <el-radio-button label="cross-border">跨境型</el-radio-button>
      </el-radio-group>
    </el-card>

    <!-- ETF列表 -->
    <el-card class="list-card">
      <div class="search-bar">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索ETF代码或名称"
          clearable
          @clear="onSearch"
          @keyup.enter="onSearch"
          style="width: 300px"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="onSearch">搜索</el-button>
      </div>

      <el-table
        :data="etfList"
        stripe
        style="width: 100%"
        :loading="loading"
        @row-click="handleRowClick"
      >
        <el-table-column prop="code" label="代码" width="120" align="center" />
        <el-table-column prop="name" label="名称" min-width="200">
          <template #default="{ row }">
            <div class="etf-name">
              <span class="name-text">{{ row.name }}</span>
              <el-tag v-if="row.isNew" type="danger" size="small">新</el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="price" label="最新价" width="120" align="right">
          <template #default="{ row }">
            <span :class="getPriceClass(row.change)">{{ row.price }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="change" label="涨跌幅" width="120" align="right">
          <template #default="{ row }">
            <span :class="getPriceClass(row.change)">
              {{ row.change > 0 ? '+' : '' }}{{ row.change }}%
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="volume" label="成交量（万手）" width="140" align="right" />
        <el-table-column prop="amount" label="成交额（亿元）" width="140" align="right" />
        <el-table-column prop="netValue" label="单位净值" width="120" align="right" />
        <el-table-column prop="category" label="类型" width="100" align="center">
          <template #default="{ row }">
            <el-tag :type="getCategoryType(row.category)" size="small">
              {{ getCategoryLabel(row.category) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click.stop="viewDetail(row)">
              详情
            </el-button>
            <el-button type="success" link size="small" @click.stop="addToWatchlist(row)">
              自选
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-bar">
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next, jumper"
          background
          @current-change="onPageChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 数据定义
const overview = ref({
  totalCount: 856,
  totalMarketCap: '12,856.32',
  risingCount: 523,
  fallingCount: 298
})

const selectedCategory = ref('all')
const searchKeyword = ref('')
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(856)

// 模拟ETF数据
const etfList = ref([
  {
    code: '510300',
    name: '沪深300ETF',
    price: 4.523,
    change: 1.25,
    volume: 1256.8,
    amount: 56.78,
    netValue: 4.5231,
    category: 'stock',
    isNew: false
  },
  {
    code: '510500',
    name: '中证500ETF',
    price: 6.234,
    change: -0.85,
    volume: 987.5,
    amount: 61.45,
    netValue: 6.2341,
    category: 'stock',
    isNew: false
  },
  {
    code: '159915',
    name: '创业板ETF',
    price: 2.145,
    change: 2.15,
    volume: 2345.6,
    amount: 50.32,
    netValue: 2.1452,
    category: 'stock',
    isNew: false
  },
  {
    code: '511010',
    name: '国债ETF',
    price: 101.23,
    change: 0.12,
    volume: 234.5,
    amount: 23.74,
    netValue: 101.2300,
    category: 'bond',
    isNew: false
  },
  {
    code: '518880',
    name: '黄金ETF',
    price: 4.567,
    change: 0.67,
    volume: 567.8,
    amount: 25.93,
    netValue: 4.5670,
    category: 'commodity',
    isNew: false
  },
  {
    code: '159920',
    name: '恒生ETF',
    price: 1.234,
    change: -1.45,
    volume: 456.7,
    amount: 5.64,
    netValue: 1.2340,
    category: 'cross-border',
    isNew: false
  },
  {
    code: '511990',
    name: '货币基金ETF',
    price: 100.05,
    change: 0.01,
    volume: 123.4,
    amount: 12.35,
    netValue: 100.0500,
    category: 'currency',
    isNew: false
  },
  {
    code: '515050',
    name: '5G ETF',
    price: 0.987,
    change: 3.25,
    volume: 3456.7,
    amount: 34.12,
    netValue: 0.9870,
    category: 'stock',
    isNew: true
  }
])

// 方法
const refreshData = () => {
  loading.value = true
  ElMessage.info('正在刷新数据...')
  setTimeout(() => {
    loading.value = false
    ElMessage.success('数据刷新成功')
  }, 1000)
}

const onCategoryChange = () => {
  currentPage.value = 1
  // 这里应该调用API获取对应分类的ETF数据
  ElMessage.info(`切换到: ${getCategoryLabel(selectedCategory.value)}`)
}

const onSearch = () => {
  currentPage.value = 1
  if (searchKeyword.value) {
    ElMessage.info(`搜索: ${searchKeyword.value}`)
  }
}

const onPageChange = (page: number) => {
  currentPage.value = page
  // 这里应该调用API获取对应页的数据
}

const handleRowClick = (row: any) => {
  console.log('点击行:', row)
}

const viewDetail = (row: any) => {
  ElMessage.info(`查看 ${row.name} 详情`)
  // 这里可以跳转到详情页或打开详情对话框
}

const addToWatchlist = (row: any) => {
  ElMessage.success(`已添加 ${row.name} 到自选`)
  // 这里应该调用API添加到自选
}

const getPriceClass = (change: number) => {
  if (change > 0) return 'price-up'
  if (change < 0) return 'price-down'
  return 'price-flat'
}

const getCategoryType = (category: string) => {
  const types: Record<string, any> = {
    stock: 'primary',
    bond: 'success',
    commodity: 'warning',
    currency: 'info',
    'cross-border': 'danger'
  }
  return types[category] || 'info'
}

const getCategoryLabel = (category: string) => {
  const labels: Record<string, string> = {
    all: '全部',
    stock: '股票型',
    bond: '债券型',
    commodity: '商品型',
    currency: '货币型',
    'cross-border': '跨境型'
  }
  return labels[category] || category
}

onMounted(() => {
  // 初始化数据
})
</script>

<style scoped>
.etf-special-page {
  padding: 20px;
}

/* 头部卡片 */
.header-card {
  margin-bottom: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  flex: 1;
}

.page-title {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.page-subtitle {
  margin: 8px 0 0 0;
  font-size: 14px;
  color: #909399;
}

/* 概览统计卡片 */
.overview-section {
  margin-bottom: 20px;
}

.stat-card {
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: white;
}

.stat-info {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.stat-value.rising {
  color: #f56c6c;
}

.stat-value.falling {
  color: #67c23a;
}

/* 分类卡片 */
.category-card {
  margin-bottom: 20px;
}

.category-header {
  margin-bottom: 16px;
}

.category-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.category-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

/* 列表卡片 */
.list-card {
  margin-bottom: 20px;
}

.search-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

/* ETF名称 */
.etf-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.name-text {
  font-weight: 500;
}

/* 价格颜色 */
.price-up {
  color: #f56c6c;
  font-weight: 500;
}

.price-down {
  color: #67c23a;
  font-weight: 500;
}

.price-flat {
  color: #909399;
}

/* 分页 */
.pagination-bar {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* 响应式 */
@media (max-width: 768px) {
  .etf-special-page {
    padding: 12px;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .search-bar {
    flex-direction: column;
  }

  .search-bar .el-input {
    width: 100% !important;
  }
}
</style>
