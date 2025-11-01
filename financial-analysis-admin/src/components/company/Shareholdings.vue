<template>
  <div class="shareholdings">
    <el-card v-if="items && items.length > 0" shadow="hover">
      <template #header>
        <div class="card-head">
          <div class="title">参股控股</div>
          <div class="meta">共 {{ items.length }} 条</div>
        </div>
      </template>

      <el-table :data="items" stripe size="small" style="width:100%">
        <el-table-column prop="enterprise_name" label="参股控股企业" min-width="260" />
        <el-table-column prop="registered_capital" label="注册资本" width="160">
          <template #default="{ row }">{{ formatCapital(row.registered_capital) }}</template>
        </el-table-column>
        <el-table-column prop="group_holding_ratio" label="集团持股比例" width="140">
          <template #default="{ row }">{{ formatPercent(row.group_holding_ratio) }}</template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-empty v-else description="暂无参股/控股信息" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ profile?: any, shareholdings?: any[] }>()

const items = computed(() => {
  // prefer explicit shareholdings prop when provided
  if (Array.isArray(props.shareholdings)) return props.shareholdings.slice()
  const p = props.profile || {}
  // Common possible keys for shareholding lists
  const list = p.shareholdings || p.investments_list || p.investments || p.holdings || []
  if (!Array.isArray(list)) return []
  // try to sort by group_holding_ratio (numeric desc) when possible
  function parsePercentToNumber(x: any) {
    if (x === null || x === undefined) return NaN
    const s = String(x).trim()
    if (s === '' || s === '--') return NaN
    if (s.endsWith('%')) {
      const n = parseFloat(s.replace('%', '').replace(/,/g, ''))
      return isNaN(n) ? NaN : n
    }
    // may be decimal like 0.5
    const n = Number(s)
    if (!isNaN(n) && Math.abs(n) <= 1) return n * 100
    return isNaN(n) ? NaN : n
  }

  const cloned = list.slice()
  cloned.sort((a: any, b: any) => {
    const A = parsePercentToNumber(a?.group_holding_ratio)
    const B = parsePercentToNumber(b?.group_holding_ratio)
    if (isNaN(A) && isNaN(B)) return 0
    if (isNaN(A)) return 1
    if (isNaN(B)) return -1
    return B - A
  })
  return cloned
})

function formatCapital(value: any) {
  if (value === null || value === undefined) return '-'
  const s = String(value)
  // if already contains 中文单位, return as-is
  if (/[亿万元]/.test(s)) return s
  const n = Number(String(value).replace(/[ ,]/g, ''))
  if (isNaN(n)) return s
  if (Math.abs(n) >= 100000000) return (n / 100000000).toFixed(3).replace(/\.0+$/, '') + ' 亿元'
  if (Math.abs(n) >= 10000) return (n / 10000).toFixed(2).replace(/\.0+$/, '') + ' 万元'
  return n.toFixed(2).replace(/\.0+$/, '') + ' 元'
}

function formatPercent(v: any) {
  if (v === null || v === undefined || v === '') return '-'
  // if already a string with %
  const s = String(v).trim()
  if (s.endsWith('%')) return s
  const n = Number(s)
  if (isNaN(n)) return s
  // if value looks like a ratio (0~1), convert to percent
  if (Math.abs(n) <= 1) return (n * 100).toFixed(2).replace(/\.0+$/, '') + '%'
  return n.toFixed(2).replace(/\.0+$/, '') + '%'
}
</script>

<style scoped>
.shareholdings .card-head { display:flex; justify-content:space-between; align-items:center }
.shareholdings .card-head .title { font-size:18px; font-weight:700 }
.shareholdings .card-head .meta { color:var(--text-secondary); font-size:14px }
.shareholdings .summary-row { padding: 14px 0 8px }
.summary-item .label { font-size:13px; color:#909399 }
.summary-item .value { font-weight:700; font-size:16px; margin-top:6px }
.shareholdings { padding: 8px 0 }
.shareholdings .el-table td { font-size:14px }
.shareholdings .el-table .registered_capital { font-weight:700; font-size:15px }
</style>
