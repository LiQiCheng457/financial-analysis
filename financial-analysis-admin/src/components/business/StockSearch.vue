<template>
  <div class="stock-search-wrapper">
    <el-autocomplete
      v-model="searchText"
      :fetch-suggestions="querySearch"
      :placeholder="placeholder"
      :clearable="true"
      :trigger-on-focus="showOnFocus"
      value-key="display"
      @select="handleSelect"
      @clear="handleClear"
      :size="size"
      class="stock-search-input"
    >
      <template #prefix>
        <el-icon><Search /></el-icon>
      </template>
      
      <template #default="{ item }">
        <div class="stock-suggestion-item">
          <div class="stock-info">
            <span class="stock-code">{{ item.code }}</span>
            <span class="stock-name">{{ item.name }}</span>
            <el-tag 
              v-if="item.market" 
              size="small" 
              class="market-tag"
              :type="getMarketTagType(item.market)"
            >
              {{ item.market }}
            </el-tag>
          </div>
          <div class="stock-meta">
            <el-icon v-if="item.isFavorite" color="#f59e0b"><StarFilled /></el-icon>
            <span v-if="item.isHistory" class="history-indicator">
              <el-icon><Clock /></el-icon>
            </span>
          </div>
        </div>
      </template>
    </el-autocomplete>
    
    <!-- 快捷操作按钮（可选） -->
    <div v-if="showActions" class="search-actions">
      <el-button 
        v-if="showFavorites" 
        :icon="Star" 
        circle 
        size="small"
        @click="showFavoritesPanel = true"
        title="自选股"
      />
      <el-button 
        v-if="showHistory" 
        :icon="Clock" 
        circle 
        size="small"
        @click="showHistoryPanel = true"
        title="搜索历史"
      />
    </div>

    <!-- 自选股面板 -->
    <el-drawer
      v-model="showFavoritesPanel"
      title="自选股列表"
      :size="400"
    >
      <div class="favorites-list">
        <el-empty v-if="favoritesList.length === 0" description="暂无自选股" />
        <div 
          v-for="stock in favoritesList" 
          :key="stock.code"
          class="favorite-item"
          @click="selectFavorite(stock)"
        >
          <div class="favorite-info">
            <span class="code">{{ stock.code }}</span>
            <span class="name">{{ stock.name }}</span>
          </div>
          <el-button 
            :icon="Delete" 
            text 
            size="small"
            @click.stop="removeFavorite(stock.code)"
          />
        </div>
      </div>
    </el-drawer>

    <!-- 搜索历史面板 -->
    <el-drawer
      v-model="showHistoryPanel"
      title="搜索历史"
      :size="400"
    >
      <div class="history-list">
        <div class="history-header">
          <span>最近搜索</span>
          <el-button 
            text 
            size="small"
            @click="clearHistory"
          >
            清空历史
          </el-button>
        </div>
        <el-empty v-if="searchHistory.length === 0" description="暂无搜索历史" />
        <div 
          v-for="(stock, index) in searchHistory" 
          :key="index"
          class="history-item"
          @click="selectHistory(stock)"
        >
          <div class="history-info">
            <span class="code">{{ stock.code }}</span>
            <span class="name">{{ stock.name }}</span>
          </div>
          <span class="time">{{ formatTime(stock.timestamp) }}</span>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Search, Star, StarFilled, Clock, Delete } from '@element-plus/icons-vue'
import { searchHistoryManager } from '@/utils/searchHistory'
import type { PropType } from 'vue'

// 定义股票信息接口
interface StockInfo {
  code: string
  name: string
  market?: string
  pinyin?: string
  isFavorite?: boolean
  isHistory?: boolean
  display?: string
  timestamp?: number
}

// Props
const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '输入股票代码或名称搜索'
  },
  size: {
    type: String as PropType<'large' | 'default' | 'small'>,
    default: 'default'
  },
  showFavorites: {
    type: Boolean,
    default: true
  },
  showHistory: {
    type: Boolean,
    default: true
  },
  showActions: {
    type: Boolean,
    default: false
  },
  showOnFocus: {
    type: Boolean,
    default: true
  }
})

// Emits
const emit = defineEmits(['update:modelValue', 'select', 'clear'])

// 响应式数据
const searchText = ref(props.modelValue)
const showFavoritesPanel = ref(false)
const showHistoryPanel = ref(false)
const searchHistory = ref<StockInfo[]>([])
const favoritesList = ref<StockInfo[]>([])

// 模拟股票数据库（实际应该从后端获取）
const stockDatabase: StockInfo[] = [
  // 沪市主板
  { code: '600000', name: '浦发银行', market: '上交所', pinyin: 'pfyh' },
  { code: '600004', name: '白云机场', market: '上交所', pinyin: 'byjc' },
  { code: '600009', name: '上海机场', market: '上交所', pinyin: 'shjc' },
  { code: '600016', name: '民生银行', market: '上交所', pinyin: 'msyh' },
  { code: '600019', name: '宝钢股份', market: '上交所', pinyin: 'bggf' },
  { code: '600028', name: '中国石化', market: '上交所', pinyin: 'zgsh' },
  { code: '600030', name: '中信证券', market: '上交所', pinyin: 'zxzq' },
  { code: '600036', name: '招商银行', market: '上交所', pinyin: 'zsyh' },
  { code: '600048', name: '保利发展', market: '上交所', pinyin: 'blfz' },
  { code: '600050', name: '中国联通', market: '上交所', pinyin: 'zglt' },
  { code: '600104', name: '上汽集团', market: '上交所', pinyin: 'sqjt' },
  { code: '600309', name: '万华化学', market: '上交所', pinyin: 'whhx' },
  { code: '600519', name: '贵州茅台', market: '上交所', pinyin: 'gzmt' },
  { code: '600887', name: '伊利股份', market: '上交所', pinyin: 'ylgf' },
  { code: '601318', name: '中国平安', market: '上交所', pinyin: 'zgpa' },
  { code: '601398', name: '工商银行', market: '上交所', pinyin: 'gsyh' },
  { code: '601857', name: '中国石油', market: '上交所', pinyin: 'zgsy' },
  { code: '601888', name: '中国中免', market: '上交所', pinyin: 'zgzm' },
  { code: '601899', name: '紫金矿业', market: '上交所', pinyin: 'zjky' },
  { code: '601939', name: '建设银行', market: '上交所', pinyin: 'jsyh' },
  { code: '601988', name: '中国银行', market: '上交所', pinyin: 'zgyh' },
  { code: '603259', name: '药明康德', market: '上交所', pinyin: 'ymkd' },
  { code: '603288', name: '海天味业', market: '上交所', pinyin: 'htwy' },
  { code: '603501', name: '韦尔股份', market: '上交所', pinyin: 'wegf' },
  
  // 深市主板
  { code: '000001', name: '平安银行', market: '深交所', pinyin: 'payh' },
  { code: '000002', name: '万科A', market: '深交所', pinyin: 'wk' },
  { code: '000063', name: '中兴通讯', market: '深交所', pinyin: 'zxtx' },
  { code: '000100', name: 'TCL科技', market: '深交所', pinyin: 'tclkj' },
  { code: '000333', name: '美的集团', market: '深交所', pinyin: 'mdjt' },
  { code: '000338', name: '潍柴动力', market: '深交所', pinyin: 'wcdl' },
  { code: '000568', name: '泸州老窖', market: '深交所', pinyin: 'lzlj' },
  { code: '000651', name: '格力电器', market: '深交所', pinyin: 'gldq' },
  { code: '000858', name: '五粮液', market: '深交所', pinyin: 'wly' },
  { code: '000876', name: '新希望', market: '深交所', pinyin: 'xxw' },
  { code: '002008', name: '大族激光', market: '深交所', pinyin: 'dzjg' },
  { code: '002027', name: '分众传媒', market: '深交所', pinyin: 'fzcm' },
  { code: '002142', name: '宁波银行', market: '深交所', pinyin: 'nbyh' },
  { code: '002230', name: '科大讯飞', market: '深交所', pinyin: 'kdxf' },
  { code: '002271', name: '东方雨虹', market: '深交所', pinyin: 'dfyh' },
  { code: '002352', name: '顺丰控股', market: '深交所', pinyin: 'sfkg' },
  { code: '002415', name: '海康威视', market: '深交所', pinyin: 'hkws' },
  { code: '002594', name: '比亚迪', market: '深交所', pinyin: 'byd' },
  { code: '002714', name: '牧原股份', market: '深交所', pinyin: 'mygf' },
  { code: '002475', name: '立讯精密', market: '深交所', pinyin: 'lxjm' },
  
  // 创业板
  { code: '300014', name: '亿纬锂能', market: '创业板', pinyin: 'ywln' },
  { code: '300015', name: '爱尔眼科', market: '创业板', pinyin: 'aeyk' },
  { code: '300059', name: '东方财富', market: '创业板', pinyin: 'dfcf' },
  { code: '300122', name: '智飞生物', market: '创业板', pinyin: 'zfsw' },
  { code: '300142', name: '沃森生物', market: '创业板', pinyin: 'wssw' },
  { code: '300347', name: '泰格医药', market: '创业板', pinyin: 'tgyy' },
  { code: '300408', name: '三环集团', market: '创业板', pinyin: 'shjt' },
  { code: '300433', name: '蓝思科技', market: '创业板', pinyin: 'lskj' },
  { code: '300498', name: '温氏股份', market: '创业板', pinyin: 'wsgf' },
  { code: '300750', name: '宁德时代', market: '创业板', pinyin: 'ndsd' },
  { code: '300760', name: '迈瑞医疗', market: '创业板', pinyin: 'mryl' },
  
  // 科创板
  { code: '688009', name: '中国通号', market: '科创板', pinyin: 'zgth' },
  { code: '688012', name: '中微公司', market: '科创板', pinyin: 'zwgs' },
  { code: '688041', name: '海光信息', market: '科创板', pinyin: 'hgxx' },
  { code: '688111', name: '金山办公', market: '科创板', pinyin: 'jsbg' },
  { code: '688126', name: '沪硅产业', market: '科创板', pinyin: 'hgcy' },
  { code: '688223', name: '晶科能源', market: '科创板', pinyin: 'jkny' },
  { code: '688256', name: '寒武纪', market: '科创板', pinyin: 'hwj' },
  { code: '688303', name: '大全能源', market: '科创板', pinyin: 'dqny' },
  { code: '688396', name: '华润微', market: '科创板', pinyin: 'hrw' },
  { code: '688599', name: '天合光能', market: '科创板', pinyin: 'thgn' },
]

// 搜索建议函数
const querySearch = (queryString: string, callback: (results: StockInfo[]) => void) => {
  if (!queryString) {
    // 无输入时，显示搜索历史和自选股
    const suggestions: StockInfo[] = []
    
    // 添加自选股（最多5个）
    if (props.showFavorites) {
      const favorites = favoritesList.value.slice(0, 5).map(item => ({
        ...item,
        isFavorite: true,
        display: `${item.code} ${item.name}`
      }))
      suggestions.push(...favorites)
    }
    
    // 添加搜索历史（最多5个）
    if (props.showHistory) {
      const history = searchHistory.value.slice(0, 5).map(item => ({
        ...item,
        isHistory: true,
        display: `${item.code} ${item.name}`
      }))
      suggestions.push(...history)
    }
    
    callback(suggestions)
    return
  }

  // 有输入时，进行搜索
  const query = queryString.toLowerCase().trim()
  const results = stockDatabase.filter(stock => {
    return (
      stock.code.toLowerCase().includes(query) ||
      stock.name.toLowerCase().includes(query) ||
      (stock.pinyin && stock.pinyin.toLowerCase().includes(query))
    )
  })

  // 标记是否为自选股
  const markedResults = results.map(stock => ({
    ...stock,
    isFavorite: favoritesList.value.some(fav => fav.code === stock.code),
    display: `${stock.code} ${stock.name}`
  }))

  callback(markedResults.slice(0, 20)) // 最多返回20条结果
}

// 处理选择
const handleSelect = (item: StockInfo) => {
  searchText.value = item.code
  emit('update:modelValue', item.code)
  emit('select', item)
  
  // 添加到搜索历史
  searchHistoryManager.add({
    code: item.code,
    name: item.name,
    market: item.market,
    timestamp: Date.now()
  })
  
  // 更新搜索历史显示
  loadSearchHistory()
}

// 处理清空
const handleClear = () => {
  searchText.value = ''
  emit('update:modelValue', '')
  emit('clear')
}

// 获取市场标签类型
const getMarketTagType = (market?: string) => {
  const typeMap: Record<string, any> = {
    '上交所': 'primary',
    '深交所': 'success',
    '创业板': 'warning',
    '科创板': 'danger'
  }
  return typeMap[market || ''] || 'info'
}

// 格式化时间
const formatTime = (timestamp?: number) => {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return `${Math.floor(diff / 86400000)}天前`
}

// 选择历史记录
const selectHistory = (stock: StockInfo) => {
  handleSelect(stock)
  showHistoryPanel.value = false
}

// 清空历史
const clearHistory = () => {
  searchHistoryManager.clear()
  searchHistory.value = []
}

// 加载搜索历史
const loadSearchHistory = () => {
  searchHistory.value = searchHistoryManager.getAll()
}

// 选择自选股
const selectFavorite = (stock: StockInfo) => {
  handleSelect(stock)
  showFavoritesPanel.value = false
}

// 移除自选股
const removeFavorite = (code: string) => {
  // TODO: 实际应该调用自选股管理接口
  favoritesList.value = favoritesList.value.filter(item => item.code !== code)
}

// 加载自选股列表
const loadFavorites = () => {
  // TODO: 从后端或本地存储加载自选股
  // 暂时使用模拟数据
  const savedFavorites = localStorage.getItem('stock_favorites')
  if (savedFavorites) {
    try {
      favoritesList.value = JSON.parse(savedFavorites)
    } catch (e) {
      favoritesList.value = []
    }
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadSearchHistory()
  loadFavorites()
})

// 暴露方法给父组件
defineExpose({
  focus: () => {
    // TODO: 聚焦到输入框
  },
  clear: handleClear
})
</script>

<style scoped>
.stock-search-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stock-search-input {
  flex: 1;
}

.stock-search-input :deep(.el-input__wrapper) {
  transition: all 0.3s;
}

.stock-search-input :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--el-color-primary) inset;
}

.search-actions {
  display: flex;
  gap: 4px;
}

/* 搜索建议项 */
.stock-suggestion-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 4px 0;
}

.stock-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stock-code {
  font-family: 'Consolas', 'Monaco', monospace;
  font-weight: 600;
  color: #1890ff;
  font-size: 13px;
  min-width: 60px;
}

.stock-name {
  color: #303133;
  font-size: 14px;
}

.market-tag {
  margin-left: 4px;
  font-size: 11px;
}

.stock-meta {
  display: flex;
  align-items: center;
  gap: 4px;
}

.history-indicator {
  color: #909399;
  font-size: 14px;
}

/* 自选股列表 */
.favorites-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.favorite-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.favorite-item:hover {
  border-color: var(--el-color-primary);
  background-color: #f0f9ff;
}

.favorite-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.favorite-info .code {
  font-family: 'Consolas', 'Monaco', monospace;
  font-weight: 600;
  color: #1890ff;
  font-size: 14px;
}

.favorite-info .name {
  color: #606266;
  font-size: 13px;
}

/* 搜索历史列表 */
.history-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 0 12px 0;
  border-bottom: 1px solid #e4e7ed;
  margin-bottom: 4px;
}

.history-header span {
  font-weight: 600;
  color: #303133;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.history-item:hover {
  border-color: var(--el-color-primary);
  background-color: #f0f9ff;
}

.history-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.history-info .code {
  font-family: 'Consolas', 'Monaco', monospace;
  font-weight: 600;
  color: #1890ff;
  font-size: 14px;
}

.history-info .name {
  color: #606266;
  font-size: 13px;
}

.time {
  color: #909399;
  font-size: 12px;
}
</style>
