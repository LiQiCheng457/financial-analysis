<template>
  <div>
    <el-card>
      <template #header>
        <div class="card-header">
          <span>历史行情数据</span>
        </div>
      </template>

      <el-form :inline="true" @submit.prevent="fetchStockData">
        <el-form-item label="股票代码">
          <el-input v-model="stockCode" placeholder="例如: 000001"></el-input>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYYMMDD"
            clearable
          />
        </el-form-item>
        <el-form-item label="调整">
          <el-select v-model="adjust" placeholder="选择调整类型" style="width:160px">
            <el-option label="不复权" value=""></el-option>
            <el-option label="前复权(qfq)" value="qfq"></el-option>
            <el-option label="后复权(hfq)" value="hfq"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="数据源">
          <el-select v-model="source" placeholder="选择数据源" style="width:160px">
            <el-option label="东财 (默认)" value="eastmoney"></el-option>
            <el-option label="新浪" value="sina"></el-option>
            <el-option label="腾讯" value="tencent"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" native-type="submit" :loading="loading">查询</el-button>
        </el-form-item>
      </el-form>

      <el-table :data="stockData" v-loading="loading" border stripe height="600">
        <el-table-column prop="日期" label="日期" width="120"></el-table-column>
        <el-table-column prop="开盘" label="开盘"></el-table-column>
        <el-table-column prop="收盘" label="收盘"></el-table-column>
        <el-table-column prop="最高" label="最高"></el-table-column>
        <el-table-column prop="最低" label="最低"></el-table-column>
        <el-table-column prop="成交量" label="成交量"></el-table-column>
        <el-table-column prop="成交额" label="成交额"></el-table-column>
        <el-table-column prop="振幅" label="振幅"></el-table-column>
        <el-table-column prop="涨跌幅" label="涨跌幅"></el-table-column>
        <el-table-column prop="涨跌额" label="涨跌额"></el-table-column>
        <el-table-column prop="换手率" label="换手率"></el-table-column>
      </el-table>

    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { getStockHistory } from '@/api/stock'
import { ElMessage } from 'element-plus'
import dayjs from 'dayjs'

const stockCode = ref('000001') // 默认查询平安银行
const dateRange = ref<[string, string] | null>(null)
const adjust = ref('')
const source = ref('eastmoney')
// Type for a single record returned by backend
interface StockRecord {
  日期?: string
  股票代码?: string
  开盘?: number | null
  收盘?: number | null
  最高?: number | null
  最低?: number | null
  成交量?: number | null
  成交额?: number | null
  振幅?: number | null
  涨跌幅?: number | null
  涨跌额?: number | null
  换手率?: number | null
  [key: string]: any
}

const stockData = ref<StockRecord[]>([])
const loading = ref(false)
const useMock = ref(false)

const mockData: StockRecord[] = [
  {
    日期: '2023-12-27',
    股票代码: '000001',
    开盘: 9.1,
    收盘: 9.12,
    最高: 9.13,
    最低: 9.02,
    成交量: 641534,
    成交额: 582036660.68,
    振幅: 1.21,
    涨跌幅: 0.22,
    涨跌额: 0.02,
    换手率: 0.33
  },
  {
    日期: '2023-12-28',
    股票代码: '000001',
    开盘: 9.11,
    收盘: 9.45,
    最高: 9.47,
    最低: 9.08,
    成交量: 1661592,
    成交额: 1550256590.59,
    振幅: 4.28,
    涨跌幅: 3.62,
    涨跌额: 0.33,
    换手率: 0.86
  }
  ,
  {
    日期: '2023-12-29',
    股票代码: '000001',
    开盘: 9.42,
    收盘: 9.39,
    最高: 9.48,
    最低: 9.35,
    成交量: 853853,
    成交额: 803196743.82,
    振幅: 1.38,
    涨跌幅: -0.63,
    涨跌额: -0.06,
    换手率: 0.44
  }
]

const fetchStockData = async () => {
  if (!stockCode.value) {
    ElMessage.warning('请输入股票代码')
    return
  }
  loading.value = true
  try {
    if (useMock.value) {
      stockData.value = mockData
      return
    }

    const params = {
      code: stockCode.value,
      start_date: dateRange.value ? dateRange.value[0] : undefined,
      end_date: dateRange.value ? dateRange.value[1] : undefined,
      adjust: adjust.value,
      source: source.value
    }
  // debug: print params to confirm source is being sent
  console.log('fetchStockData params ->', params)
  // getStockHistory returns the data directly (request wrapper returns response.data)
  const data = await getStockHistory(params)
  console.log('fetchStockData response ->', data, 'source=', source.value)
    if (Array.isArray(data)) {
      stockData.value = data
    } else if (data && Array.isArray((data as any).data)) {
      stockData.value = (data as any).data
    } else if (data && (data as any).error) {
      stockData.value = []
      ElMessage.error((data as any).error)
    } else {
      stockData.value = []
      ElMessage.error('未能获取到数据，请检查查询条件或后端状态')
    }
  } catch (error) {
    stockData.value = []
    ElMessage.error('请求失败，请检查网络或联系管理员')
    console.error(error)
  } finally {
    loading.value = false
  }
}

// 组件挂载后自动加载一次默认股票的数据（最近一年）
onMounted(() => {
  const today = dayjs()
  const oneYearAgo = today.subtract(1, 'year')
  dateRange.value = [oneYearAgo.format('YYYYMMDD'), today.format('YYYYMMDD')]
  fetchStockData()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
