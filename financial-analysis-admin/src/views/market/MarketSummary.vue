<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>上海证券交易所 - 每日概况
            <small v-if="formattedQueryDate" style="margin-left:8px;color:#909399;font-size:12px">({{ formattedQueryDate }} 查询)</small>
          </span>
          <span v-if="actualDate" class="actual-date-tip">
            数据日期: {{ formattedActualDate }}
            <el-tooltip v-if="isHoliday" content="您选择的日期为休市日，已自动为您展示前一交易日的数据。" placement="top">
              <el-icon><QuestionFilled /></el-icon>
            </el-tooltip>
          </span>
        </div>
      </template>

      <el-form :inline="true" @submit.prevent="fetchSummaryData">
        <el-form-item label="查询日期">
          <el-date-picker
            v-model="queryDate"
            type="date"
            placeholder="选择日期"
            format="YYYY-MM-DD"
            value-format="YYYYMMDD"
            :disabled-date="disabledDate"
            style="width: 150px;"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchSummaryData" :loading="loading">查询</el-button>
        </el-form-item>
      </el-form>

      <el-table
        v-if="summaryData.length > 0"
        :data="summaryData"
        v-loading="loading"
        border
        stripe
        style="width: 100%"
      >
        <!-- 后端返回的字段示例在 tmp_logs 中为: "单日情况", "股票", "主板A", "主板B", "科创板", "股票回购" -->
        <el-table-column prop="单日情况" label="单日情况" width="180" />
        <el-table-column prop="股票" label="股票" />
        <el-table-column prop="主板A" label="主板A" />
        <el-table-column prop="主板B" label="主板B" />
        <el-table-column prop="科创板" label="科创板" />
        <el-table-column prop="股票回购" label="股票回购" />
      </el-table>
      <el-empty v-else-if="!loading" :description="emptyText" />

    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { getSseDailySummary, getTradeDates } from '@/api/stock'
import { ElMessage } from 'element-plus'
import { QuestionFilled } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

const queryDate = ref('')
const actualDate = ref('')
const summaryData = ref<any[]>([])
const loading = ref(false)
const tradeDates = ref<Set<string>>(new Set())
const emptyText = ref('请选择日期进行查询')

const isHoliday = computed(() => !!(queryDate.value && summaryDataHoliday.value))
const formattedActualDate = computed(() => actualDate.value ? dayjs(actualDate.value, 'YYYYMMDD').format('YYYY-MM-DD') : '')
const summaryDataHoliday = ref(false)

// 日期选择器中禁用非交易日
const disabledDate = (time: Date) => {
  if (tradeDates.value.size === 0) {
    return false // 如果交易日历还没加载好，暂时不禁用任何日期
  }
  const dateStr = dayjs(time).format('YYYYMMDD')
  return !tradeDates.value.has(dateStr)
}

const formattedQueryDate = computed(() => queryDate.value ? dayjs(queryDate.value, 'YYYYMMDD').format('YYYY-MM-DD') : '')

const fetchTradeDates = async () => {
  try {
    const dates = await getTradeDates()
    tradeDates.value = new Set(dates)
    // 设置默认查询日期为最近的一个交易日 (不晚于今天)
    if (dates.length > 0) {
      const today = dayjs().format('YYYYMMDD')
      // 找到最后一个 <= today 的交易日
      const candidate = dates.slice().reverse().find(d => d <= today) || dates[dates.length - 1]
      queryDate.value = candidate
      fetchSummaryData() // 加载默认数据
    }
  } catch (error) {
    ElMessage.error('获取交易日历失败')
  }
}

const fetchSummaryData = async () => {
  if (!queryDate.value) {
    ElMessage.warning('请选择查询日期')
    return
  }
  loading.value = true
  emptyText.value = '正在加载...'
  try {
    const res = await getSseDailySummary(queryDate.value)
    // res expected: { date, data, holiday, message }
    if (!res) {
      ElMessage.error('接口返回异常')
      summaryData.value = []
      summaryDataHoliday.value = false
      actualDate.value = ''
    } else if (res.holiday) {
      // holiday: true -> notify and clear data
      summaryData.value = []
      summaryDataHoliday.value = true
      actualDate.value = res.date
      emptyText.value = res.message || `${res.date} 为休市日`
      ElMessage.info(emptyText.value)
    } else {
      summaryData.value = res.data || []
      summaryDataHoliday.value = false
      actualDate.value = res.date
      if (!summaryData.value || summaryData.value.length === 0) {
        emptyText.value = res.message || '暂无数据'
      }
    }
  } catch (error) {
    ElMessage.error('请求失败，请检查网络或联系管理员')
    summaryData.value = []
    emptyText.value = '请求失败'
    console.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchTradeDates()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.actual-date-tip {
  font-size: 14px;
  color: #909399;
  display: flex;
  align-items: center;
}
.actual-date-tip .el-icon {
  margin-left: 5px;
  cursor: pointer;
}
</style>
