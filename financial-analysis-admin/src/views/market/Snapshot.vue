<template>
  <PageShell>
    <template #title>公司概况查询</template>
    <template #subtitle>
      <span v-if="!hasSearched">输入股票代码、名称或行业进行搜索</span>
      <span v-else>共找到 {{ searchResult.total }} 家公司</span>
    </template>
    <template #actions>
      <el-button v-if="showDetail" @click="backToList" :icon="ArrowLeft">返回列表</el-button>
    </template>

    <!-- 详情页 -->
    <div v-if="showDetail" class="detail-view">
      <el-skeleton :rows="15" animated v-if="detailLoading" />
      <el-alert v-if="detailErrorMsg" :title="detailErrorMsg" type="error" show-icon :closable="false" />
      <el-empty v-if="detailNotFound" description="未找到该公司详细信息" />

      <div v-if="profile" class="company-profile">
        <!-- 公司头部：始终显示 -->
        <CompanyHeader :companyName="profile.company_name" :englishName="profile.english_name" :stockCode="profile.a_stock_code" />
        
        <!-- 关键指标卡片 -->
        <el-row :gutter="16" class="metrics-row">
          <el-col :xs="12" :sm="8" :md="6">
            <el-card class="metric-card" shadow="hover">
              <div class="metric-content">
                <div class="metric-label">注册资本</div>
                <div class="metric-value highlight">{{ formatCapital(profile.registered_capital) }}</div>
              </div>
            </el-card>
          </el-col>
          <el-col :xs="12" :sm="8" :md="6">
            <el-card class="metric-card" shadow="hover">
              <div class="metric-content">
                <div class="metric-label">所属行业</div>
                <div class="metric-value industry">{{ profile.eastmoney_industry || profile.regulatory_industry || '-' }}</div>
              </div>
            </el-card>
          </el-col>
          <el-col :xs="12" :sm="8" :md="6">
            <el-card class="metric-card" shadow="hover">
              <div class="metric-content">
                <div class="metric-label">所在地区</div>
                <div class="metric-value">{{ profile.region || '-' }}</div>
              </div>
            </el-card>
          </el-col>
          <el-col :xs="12" :sm="8" :md="6">
            <el-card class="metric-card" shadow="hover">
              <div class="metric-content">
                <div class="metric-label">董事长</div>
                <div class="metric-value">{{ profile.chairman || '-' }}</div>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <!-- 标签页内容 -->
        <el-tabs v-model="activeTab" type="card" class="detail-tabs">
          <el-tab-pane label="基本信息" name="info">
            <CompanyInfoTable :profile="profile" />
          </el-tab-pane>
          
          <el-tab-pane label="股票走势" name="kline">
            <CompanyKLine v-if="profile.stock_code || profile.a_stock_code" :stockCode="profile.stock_code || profile.a_stock_code" />
          </el-tab-pane>
          
          <el-tab-pane label="财务指标" name="financial">
            <FinancialMetrics 
              v-if="profile.stock_code || profile.a_stock_code" 
              :stockCode="profile.stock_code || profile.a_stock_code"
              :stockName="profile.a_stock_abbr || profile.company_name"
            />
          </el-tab-pane>
          
          <el-tab-pane label="经营范围" name="business">
            <el-card class="business-scope-card">
              <div class="business-content">
                <h4>经营范围</h4>
                <p>{{ profile.business_scope || '暂无数据' }}</p>
              </div>
            </el-card>
          </el-tab-pane>
          
          <el-tab-pane label="管理层" name="intro">
              <ManagementTeam :profile="profile" />
          </el-tab-pane>

          <el-tab-pane label="发行相关" name="issuance">
            <IssueInfo :profile="profile" :issuance="profile && profile.issuance" />
          </el-tab-pane>

          <el-tab-pane label="参股控股" name="shareholdings">
            <Shareholdings :profile="profile" :shareholdings="profile && profile.shareholdings" />
          </el-tab-pane>

        </el-tabs>
      </div>
    </div>

    <!-- 列表页 -->
    <div v-else class="list-view">
      <!-- 搜索 + 行业筛选 -->
      <div class="search-filter-container">
        <div class="main-search-bar">
          <el-input
            v-model="searchQuery"
            placeholder="输入搜索内容"
            size="large"
            clearable
            @keyup.enter="doSearchList"
            class="search-input"
          >
            <template #append>
              <el-button @click="doSearchList" :loading="loading" type="primary" :icon="Search">搜索</el-button>
            </template>
          </el-input>
        </div>

        <div class="industry-filter-panel">
          <div class="panel-header">
            <span>勾选分类标签精确查询</span>
            <el-radio-group v-model="industryMatchMode" size="small" style="margin-left: 16px;">
              <el-radio-button label="any">满足任一标签</el-radio-button>
              <el-radio-button label="all">满足全部标签</el-radio-button>
            </el-radio-group>
          </div>
          <div class="panel-body">
            <div v-for="group in industryGroups" :key="group.name" class="industry-group">
              <div class="group-title">{{ group.name }}</div>
              <div class="tags-container">
                <el-checkbox-group v-model="selectedIndustries" @change="onIndustryChange">
                  <el-checkbox v-for="tag in group.tags" :key="tag" :label="tag" border class="tag-checkbox">
                    {{ tag }}
                  </el-checkbox>
                </el-checkbox-group>
              </div>
            </div>
          </div>
        </div>

        <!-- 高级筛选面板 -->
        <div class="advanced-filter-panel">
          <div class="panel-header">
            <span>🔍 高级筛选条件</span>
            <el-button text size="small" @click="resetAdvancedFilters">重置筛选</el-button>
          </div>
          <div class="panel-body advanced-filters">
            <div class="filter-row">
              <!-- 注册资本范围 -->
              <div class="filter-item">
                <label class="filter-label">注册资本</label>
                <div class="filter-input-group">
                  <el-input-number
                    v-model="advancedFilters.minCapital"
                    :min="0"
                    :step="1000000"
                    placeholder="最小值"
                    size="small"
                    style="width: 130px"
                    controls-position="right"
                  />
                  <span class="separator">至</span>
                  <el-input-number
                    v-model="advancedFilters.maxCapital"
                    :min="0"
                    :step="1000000"
                    placeholder="最大值"
                    size="small"
                    style="width: 130px"
                    controls-position="right"
                  />
                  <el-select v-model="advancedFilters.capitalUnit" size="small" style="width: 80px">
                    <el-option label="元" value="1" />
                    <el-option label="万元" value="10000" />
                    <el-option label="亿元" value="100000000" />
                  </el-select>
                </div>
              </div>

              <!-- 所在地区 -->
              <div class="filter-item">
                <label class="filter-label">所在地区</label>
                <el-select
                  v-model="advancedFilters.region"
                  placeholder="选择省份/城市"
                  clearable
                  size="small"
                  style="width: 150px"
                >
                  <el-option label="全部" value="" />
                  <el-option label="北京" value="北京" />
                  <el-option label="上海" value="上海" />
                  <el-option label="广东" value="广东" />
                  <el-option label="深圳" value="深圳" />
                  <el-option label="浙江" value="浙江" />
                  <el-option label="江苏" value="江苏" />
                  <el-option label="四川" value="四川" />
                  <el-option label="湖北" value="湖北" />
                  <el-option label="福建" value="福建" />
                  <el-option label="山东" value="山东" />
                </el-select>
              </div>

              <!-- 精准搜索按钮 -->
              <div class="filter-item">
                <label class="filter-label">&nbsp;</label>
                <el-button 
                  type="primary"
                  size="small"
                  @click="doExactSearch"
                  style="width: 120px"
                >
                  🎯 精准搜索
                </el-button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 搜索结果 -->
      <div v-if="hasSearched" class="search-results">
        <el-skeleton :rows="10" animated v-if="loading" />
        <el-alert v-if="errorMsg" :title="errorMsg" type="error" show-icon :closable="false" />

        <div v-if="!loading && !errorMsg && searchResult.data.length > 0">
          <div class="sort-bar">
            <el-select v-model="selectedSort" placeholder="排序方式" size="small" @change="onSortChange">
              <el-option label="默认" value="default" />
              <el-option label="股票代码 ↑" value="code_asc" />
              <el-option label="股票代码 ↓" value="code_desc" />
              <el-option label="注册资本 ↓（从大到小）" value="capital_desc" />
              <el-option label="注册资本 ↑（从小到大）" value="capital_asc" />
            </el-select>
          </div>
          <el-table :data="sortedData" stripe @row-click="handleRowClick" class="result-table">
            <el-table-column prop="stock_code" label="股票代码" width="120" sortable>
              <template #default="{ row }">
                <span class="code-text">{{ row.stock_code }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="a_stock_abbr" label="股票简称" width="120" sortable />
            <el-table-column prop="company_name" label="公司名称" min-width="200" sortable show-overflow-tooltip />
            <el-table-column prop="security_category" label="证券类型" width="120" sortable>
              <template #default="{ row }">
                <el-tag size="small" type="success" class="badge-text">{{ row.security_category }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="chairman" label="董事长" width="120" sortable show-overflow-tooltip>
              <template #default="{ row }">
                <span class="person-text">{{ row.chairman }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="legal_representative" label="法人" width="120" sortable show-overflow-tooltip>
              <template #default="{ row }">
                <span class="person-text">{{ row.legal_representative }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="region" label="区域" width="100" sortable />
            <el-table-column prop="registered_capital" label="注册资本(元)" width="150" align="right" sortable>
              <template #default="{ row }">
                <span class="highlight">{{ formatCapital(row.registered_capital) }}</span>
              </template>
            </el-table-column>
          </el-table>

          <el-pagination
            v-if="searchResult.total > 0"
            background
            layout="total, sizes, prev, pager, next, jumper"
            :total="searchResult.total"
            :current-page="currentPage"
            :page-size="pageSize"
            :page-sizes="[20, 50, 100, 200]"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
            class="pagination-bar"
          />
        </div>

        <el-empty v-if="!loading && !errorMsg && searchResult.data.length === 0" description="没有找到符合条件的公司" />
      </div>

      <!-- 初始欢迎页 -->
      <div v-if="!hasSearched" class="welcome-container">
        <div class="welcome-content">
          <div class="welcome-icon">🏢</div>
          <h2 class="welcome-title">公司概况查询</h2>
          <p class="welcome-text">通过股票代码、公司名称或行业标签，快速查找A股上市公司的详细资料。</p>
        </div>
      </div>
    </div>
  </PageShell>
</template>

<script setup lang="ts">
import { ref, watch, computed } from 'vue'
import { Search, ArrowLeft } from '@element-plus/icons-vue'
import PageShell from '@/components/PageShell.vue'
import CompanyHeader from '@/components/company/CompanyHeader.vue'
import CompanyInfoTable from '@/components/company/CompanyInfoTable.vue'
import CompanyKLine from '@/components/company/CompanyKLine.vue'
import FinancialMetrics from '@/components/FinancialMetrics.vue'
import IssueInfo from '@/components/company/IssueInfo.vue'
import Shareholdings from '@/components/company/Shareholdings.vue'
import ManagementTeam from '@/components/company/ManagementTeam.vue'
import { searchCompanies, getCompanyProfile } from '@/api/stock'

// (MOCK_PROFILE removed) 

const searchQuery = ref('')
const loading = ref(false)
const errorMsg = ref('')
const hasSearched = ref(false)
const searchResult = ref<any>({ data: [], total: 0, page: 1, page_size: 50, total_pages: 0 })
const currentPage = ref(1)
const pageSize = ref(50)

const selectedIndustries = ref<string[]>([])
const industryMatchMode = ref<'any' | 'all'>('any') // 行业标签匹配模式

// 高级筛选条件
const advancedFilters = ref({
  minCapital: null as number | null,
  maxCapital: null as number | null,
  capitalUnit: '100000000', // 默认单位：亿元
  region: '',
  searchMode: 'fuzzy' as 'fuzzy' | 'exact'
})

const industryGroups = [
  { name: '金融', tags: ['银行', '证券', '保险', '信托', '投资', '金融服务'] },
  { name: '科技', tags: ['软件', '互联网', '电子', '通信', '计算机', '信息技术', '半导体'] },
  { name: '医药生物', tags: ['医药', '生物', '制药', '医疗', '医疗器械', '中药'] },
  { name: '食品饮料', tags: ['食品', '饮料', '白酒', '啤酒', '乳制品', '调味品', '农产品'] },
  { name: '新能源', tags: ['新能源', '风能', '电池', '储能', '太阳能'] },
  { name: '汽车', tags: ['汽车', '汽车零部件', '商用车', '乘用车'] },
  { name: '房地产', tags: ['房地产', '地产', '物业', '建筑', '装饰', '园林'] },
  { name: '制造业', tags: ['机械', '设备', '钢铁', '化工', '建材', '有色金属', '电气'] }
]

watch(selectedIndustries, () => {}, { deep: true })

function onIndustryChange() { doSearchList() }

// 精准搜索
function doExactSearch() {
  advancedFilters.value.searchMode = 'exact'
  doSearchList()
}

// 排序相关
const selectedSort = ref('default')

function onSortChange() {
  // 目前排序在客户端计算属性中自动生效，这里保留回调以便未来扩展
}

// 将注册资本（可能带单位）解析为数字，便于排序；解析失败返回 0
function parseCapitalToNumber(value: string | number | undefined): number {
  if (value === null || value === undefined) return 0
  if (typeof value === 'number') return isFinite(value) ? value : 0
  let s = String(value).trim()
  if (!s) return 0
  // 常见中文单位处理
  try {
    if (s.includes('亿')) {
      const n = parseFloat(s.replace(/[^0-9.\-]/g, ''))
      return isNaN(n) ? 0 : n * 100000000
    }
    if (s.includes('万')) {
      const n = parseFloat(s.replace(/[^0-9.\-]/g, ''))
      return isNaN(n) ? 0 : n * 10000
    }
    // 移除普通格式化字符，如逗号、空格和单位后缀
    s = s.replace(/[,\s\u00A0]/g, '')
    // 移除可能的中文/字母单位
    s = s.replace(/[a-zA-Z一-龥%￥¥元]/g, '')
    const n = parseFloat(s)
    return isNaN(n) ? 0 : n
  } catch (e) {
    return 0
  }
}

// 根据所选排序方式对当前页数据进行排序（只影响当前拿到的 page 数据）
const sortedData = computed(() => {
  const data = Array.isArray(searchResult.value?.data) ? [...searchResult.value.data] : []
  const mode = selectedSort.value
  if (mode === 'default') return data

  if (mode === 'code_asc' || mode === 'code_desc') {
    data.sort((a: any, b: any) => {
      const A = String(a?.stock_code || '').padStart(20, '0')
      const B = String(b?.stock_code || '').padStart(20, '0')
      if (A < B) return mode === 'code_asc' ? -1 : 1
      if (A > B) return mode === 'code_asc' ? 1 : -1
      return 0
    })
    return data
  }

  if (mode === 'capital_desc' || mode === 'capital_asc') {
    data.sort((a: any, b: any) => {
      const A = parseCapitalToNumber(a?.registered_capital)
      const B = parseCapitalToNumber(b?.registered_capital)
      if (A < B) return mode === 'capital_asc' ? -1 : 1
      if (A > B) return mode === 'capital_asc' ? 1 : -1
      return 0
    })
    return data
  }

  return data
})

const showDetail = ref(false)
const detailLoading = ref(false)
const profile = ref<any | null>(null)
const detailErrorMsg = ref('')
const detailNotFound = ref(false)
const activeTab = ref('info') // 默认显示基本信息标签页

function formatCapital(value: string | number | undefined) {
  if (value === null || value === undefined) return '-'
  const strValue = String(value)
  if (strValue.includes('亿') || strValue.includes('万') || strValue.includes('元')) return strValue
  const num = Number(value)
  if (isNaN(num)) return '-'
  if (num >= 100000000) return (num / 100000000).toFixed(2) + ' 亿元'
  if (num >= 10000) return (num / 10000).toFixed(2) + ' 万元'
  return num.toFixed(2) + ' 元'
}

// 重置高级筛选条件
function resetAdvancedFilters() {
  advancedFilters.value = {
    minCapital: null,
    maxCapital: null,
    capitalUnit: '100000000',
    region: '',
    searchMode: 'fuzzy'
  }
}

async function doSearchList() {
  if (!searchQuery.value && selectedIndustries.value.length === 0) {
    errorMsg.value = '请输入搜索关键词或选择行业标签'
    return
  }
  loading.value = true
  errorMsg.value = ''
  hasSearched.value = true
  try {
    const industryParam = selectedIndustries.value.join(',')
    
    // 构建高级筛选参数
    const params: any = {
      q: searchQuery.value || '',
      page: currentPage.value,
      page_size: pageSize.value,
      industry: industryParam || undefined,
      industry_match_mode: industryMatchMode.value,
      search_mode: advancedFilters.value.searchMode
    }
    
    // 注册资本范围
    if (advancedFilters.value.minCapital !== null) {
      params.min_capital = advancedFilters.value.minCapital * Number(advancedFilters.value.capitalUnit)
    }
    if (advancedFilters.value.maxCapital !== null) {
      params.max_capital = advancedFilters.value.maxCapital * Number(advancedFilters.value.capitalUnit)
    }
    
    // 地区筛选
    if (advancedFilters.value.region) {
      params.region = advancedFilters.value.region
    }
    
    const res = await searchCompanies(params)
    if ((res as any).status === 'ok') searchResult.value = res
    else errorMsg.value = (res as any).message || '搜索失败'
  } catch (e: any) {
    errorMsg.value = e.response?.data?.detail || e.message || '网络错误'
  } finally {
    loading.value = false
  }
}

function handleSizeChange(newSize: number) { pageSize.value = newSize; currentPage.value = 1; doSearchList() }
function handlePageChange(newPage: number) { currentPage.value = newPage; doSearchList() }
function handleRowClick(row: any) { if (row?.stock_code) viewDetail(row.stock_code) }

async function viewDetail(stockCode: string) {
  showDetail.value = true
  detailLoading.value = true
  detailErrorMsg.value = ''
  detailNotFound.value = false
  profile.value = null
  try {
    const res = await getCompanyProfile(stockCode)
    if ((res as any).status === 'ok' && (res as any).data) profile.value = (res as any).data
    else detailNotFound.value = true
    // 开发模式：注入示例数据以便本地演示（不会提交任何后端）
    // 开发模式不再注入 MOCK_PROFILE，真实后端数据为准
    // 归一化一些常见的字段名，确保子组件总能拿到数组类型的 shareholdings / issuance
    try {
      if (profile.value) {
        const p: any = profile.value
        p.shareholdings = p.shareholdings || p.investments || p.investments_list || p.shareholding_list || []
        p.issuance = p.issuance || p.issue_records || p.issuance_records || p.issuing || []
        if (!Array.isArray(p.shareholdings)) p.shareholdings = p.shareholdings ? [p.shareholdings] : []
        if (!Array.isArray(p.issuance)) p.issuance = p.issuance ? [p.issuance] : []
        
        // 如果顶层没有 issuing_authority，尝试从 issuance 第一个记录中推断（如 sponsor_institution / issuing_institution /issuer_name）
        try {
          if (!p.issuing_authority && p.issuance && p.issuance.length > 0) {
            const first = p.issuance[0]
            p.issuing_authority = p.issuing_authority || first.sponsor_institution || first.issuing_institution || first.issuer_name || null
          }
        } catch(e) {
          /* ignore */
        }
        // 强制深拷贝一次以触发 Vue 的响应式更新（保险）
        try {
          profile.value = JSON.parse(JSON.stringify(p))
        } catch (err) {
          profile.value = p
        }
      }
    } catch (err) {
      // 不阻塞用户展示
    }
  } catch (e: any) {
    detailErrorMsg.value = e.response?.data?.detail || e.message || '加载详细信息失败'
  } finally {
    detailLoading.value = false
  }
}

function backToList() { showDetail.value = false; profile.value = null }
</script>

<style scoped>
/* 搜索/列表及通用样式 */
.search-filter-container { background: #ffffff; padding: 24px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.08); margin-bottom: 24px }
.main-search-bar { max-width: 800px; margin: 0 auto 24px auto }
.search-input :deep(.el-input-group__append .el-button) { border-radius: 0 6px 6px 0 }
.industry-filter-panel { border: 1px solid #e4e7ed; border-radius: 8px; margin-bottom: 16px }
.panel-header { background-color: #f5f7fa; padding: 12px 16px; font-weight: 600; color: #303133; border-bottom: 1px solid #e4e7ed; border-radius: 8px 8px 0 0; display: flex; justify-content: space-between; align-items: center }
.panel-body { padding: 16px; display: flex; gap: 16px; flex-wrap: nowrap; justify-content: space-between; overflow-x: auto }
.industry-group { flex: 1 1 0; min-width: 140px; max-width: 160px }
.group-title { font-weight: 500; color: #606266; margin-bottom: 10px; padding: 6px 4px; border-left: 3px solid var(--primary-color); background-color: #f0f2f5; border-radius: 4px; text-align: center; font-size: 14px; white-space: nowrap }

/* 高级筛选面板 */
.advanced-filter-panel {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  background: linear-gradient(to bottom, #fafbfc, #ffffff);
}

.advanced-filter-panel .panel-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  border-bottom: none;
}

.advanced-filter-panel .panel-header .el-button {
  color: #ffffff;
}

.advanced-filter-panel .panel-header .el-button:hover {
  color: #ffd700;
}

.advanced-filters {
  padding: 20px;
}

.filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: flex-end;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-label {
  font-size: 13px;
  font-weight: 500;
  color: #606266;
}

.filter-input-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-input-group .separator {
  color: #909399;
  font-size: 13px;
  padding: 0 4px;
}

.tags-container .el-checkbox-group { display:flex; flex-direction:column; gap:6px; align-items: center }
.tag-checkbox.el-checkbox { margin-right:0; width:100% }
.tag-checkbox :deep(.el-checkbox__label) { font-size:13px }
.tag-checkbox.is-bordered { border-radius:4px }
.search-results { margin-top:24px }
.result-table { cursor:pointer }
.pagination-bar { margin-top:24px; justify-content:flex-end }
.welcome-container { display:flex; justify-content:center; align-items:center; text-align:center; padding:80px 20px; background:linear-gradient(to bottom,#ffffff,#f7f9fc); border-radius:12px }
.welcome-title { font-size:2rem; font-weight:700; color:var(--text-primary); margin-bottom:16px }
.welcome-text { font-size:1.1rem; color:var(--text-secondary); line-height:1.7 }
.detail-view { animation:fadeIn 0.3s ease }
.company-profile { margin-bottom:18px }

/* 关键指标卡片 */
.metrics-row {
  margin: 20px 0;
}

.metric-card {
  margin-bottom: 16px;
  transition: transform 0.2s;
}

.metric-card:hover {
  transform: translateY(-2px);
}

.metric-content {
  text-align: center;
  padding: 8px 0;
}

.metric-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 8px;
}

.metric-value {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.metric-value.highlight {
  color: #cf1322;
}
 
.metric-value.industry {
  color: #409EFF;
}

/* 标签页样式 */
.detail-tabs {
  margin-top: 20px;
}

.detail-tabs :deep(.el-tabs__header) {
  margin-bottom: 20px;
}

.detail-tabs :deep(.el-tabs__item) {
  font-size: 15px;
  padding: 0 24px;
  height: 44px;
  line-height: 44px;
}

/* 业务范围卡片 */
.business-scope-card, .intro-card {
  background: #ffffff;
}

.business-content, .intro-content {
  padding: 8px;
}

.business-content h4, .intro-content h4 {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e4e7ed;
}

.business-content p, .intro-content p {
  font-size: 14px;
  line-height: 1.8;
  color: #606266;
  text-align: justify;
}

.intro-details {
  margin-top: 16px;
}

.detail-item {
  margin-bottom: 12px;
  font-size: 14px;
  line-height: 1.8;
}

.sub-info-card {
  background: transparent;
  border: none;
  padding: 0;
}

.sub-info-grid .detail-item .label { font-weight: 600; color: #606266 }
.sub-info-grid .detail-item .value { color: #303133 }

.detail-item .label {
  color: #909399;
  font-weight: 500;
}

.detail-item .value {
  color: #303133;
  margin-left: 4px;
}

.code-text { color:#1890ff; font-family:'Consolas','Monaco',monospace }
.badge-text { color:#67C23A; font-weight:500 }
.person-text { color:#333 }
.highlight { color:#cf1322; font-weight:600 }

/* 排序控件样式：限制宽度并靠右显示，不占据整行 */
.sort-bar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 12px;
  width: 10%;
  margin-left: auto;
  align-items: center;
}
.sort-bar :deep(.el-select) {
  min-width: 180px;
  max-width: 100%;
  width: 100%;
}

/* 窄屏回退为全宽，保证可用性 */
@media (max-width: 900px) {
  .sort-bar { width: 100%; margin-left: 0; justify-content: flex-start }
}
</style>
