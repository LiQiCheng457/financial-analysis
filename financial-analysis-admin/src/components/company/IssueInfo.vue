<template>
  <div class="issue-info">
    <el-card v-if="records && records.length > 0" shadow="hover">
      <template #header>
        <div class="card-head">
          <div class="title">发行相关</div>
        </div>
      </template>

      <div class="issue-grid-wrap">
        <div v-for="(r, idx) in records" :key="r.id || idx" class="issuance-card">
          <table class="issue-grid">
            <tbody>
              <tr>
                <th>保荐机构</th>
                <td>{{ field(r, ['sponsor_institution','sponsor_institution']) || '-' }}</td>
                <th>主承销商</th>
                <td>{{ field(r, ['main_underwriter','main_underwriter']) || '-' }}</td>
              </tr>
              <tr>
                <th>成立日期</th>
                <td>{{ formatDate(field(r, ['establishment_date','establishment_date'])) }}</td>
                <th>上市日期</th>
                <td>{{ formatDate(field(r, ['listing_date','listing_date'])) }}</td>
              </tr>
              <tr>
                <th>发行市盈率(倍)</th>
                <td>{{ field(r, ['issue_pe_ratio','issue_pe_ratio']) || '-' }}</td>
                <th>网上发行日期</th>
                <td>{{ formatDate(field(r, ['online_issue_date','online_issue_date'])) }}</td>
              </tr>
              <tr>
                <th>发行方式</th>
                <td>{{ field(r, ['issue_method','issue_method']) || '-' }}</td>
                <th>每股面值(元)</th>
                <td>{{ field(r, ['face_value_per_share','face_value_per_share']) || '-' }}</td>
              </tr>
              <tr>
                <th>发行量</th>
                <td>{{ formatNumber(field(r, ['issue_quantity','issue_quantity'])) }}</td>
                <th>每股发行价(元)</th>
                <td>{{ formatNumber(field(r, ['issue_price_per_share','issue_price_per_share'])) }}</td>
              </tr>
              <tr>
                <th>发行费用(元)</th>
                <td>{{ formatMoney(field(r, ['issue_cost','issue_cost'])) }}</td>
                <th>发行总市值(元)</th>
                <td>{{ formatMoney(field(r, ['total_issue_market_value','total_issue_market_value'])) }}</td>
              </tr>
              <tr>
                <th>募集资金净额(元)</th>
                <td>{{ formatMoney(field(r, ['net_funds_raised','net_funds_raised'])) }}</td>
                <th>首日开盘价(元)</th>
                <td>{{ formatNumber(field(r, ['first_day_open_price','first_day_open_price'])) }}</td>
              </tr>
              <tr>
                <th>首日收盘价(元)</th>
                <td>{{ formatNumber(field(r, ['first_day_close_price','first_day_close_price'])) }}</td>
                <th>首日最高价(元)</th>
                <td>{{ formatNumber(field(r, ['first_day_high_price','first_day_high_price'])) }}</td>
              </tr>
              <tr>
                <th>首日换手率</th>
                <td>{{ formatPercent(field(r, ['first_day_turnover_rate','first_day_turnover_rate'])) }}</td>
                <th>定价中签率</th>
                <td>{{ formatPercent(field(r, ['pricing_lottery_rate','pricing_lottery_rate'])) }}</td>
              </tr>
              <tr>
                <th>网下配售中签率</th>
                <td>{{ formatPercent(field(r, ['offline_allotment_lottery_rate','offline_allotment_lottery_rate'])) }}</td>
                <th>备注</th>
                <td>{{ field(r, ['remarks','remarks']) || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </el-card>

    <el-empty v-else description="暂无发行信息" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ profile?: any, issuance?: any[] }>()

const authority = computed(() => {
  // prefer explicit top-level profile field, otherwise try first issuance record's sponsor
  if (props.profile && props.profile.issuing_authority) return props.profile.issuing_authority
  if (Array.isArray(props.issuance) && props.issuance.length > 0) return props.issuance[0].sponsor_institution || props.issuance[0].issuing_institution || null
  const p = props.profile || {}
  return p.issuing_authority || p.issuing_authority || null
})

const records = computed(() => {
  // prefer explicit issuance prop when provided (avoids ambiguity)
  if (Array.isArray(props.issuance)) return props.issuance
  const p = props.profile || {}
  // Common possible keys for issuance records
  const list = p.issue_records || p.issuance_records || p.issuance || p.issuing || []
  if (!Array.isArray(list)) return []
  return list
})

// no-op: old single-record helper removed

function field(obj: any, keys: string[] | string) {
  if (!obj) return undefined
  const ks = Array.isArray(keys) ? keys : [keys]
  for (const k of ks) {
    if (k in obj && obj[k] !== undefined && obj[k] !== null && String(obj[k]).trim() !== '') return obj[k]
  }
  return undefined
}

function formatDate(v: any) {
  if (!v) return '-'
  const s = String(v).trim()
  // try to parse YYYY-MM-DD or YYYYMMDD
  if (/^\d{8}$/.test(s)) return s.slice(0,4) + '-' + s.slice(4,6) + '-' + s.slice(6,8)
  return s
}

function formatNumber(v: any) {
  if (v === null || v === undefined || v === '') return '-'
  const n = Number(String(v).replace(/[, ]/g, ''))
  if (isNaN(n)) return String(v)
  // if integer-like, show without decimals
  if (Number.isInteger(n)) return n.toLocaleString()
  return n.toFixed(2)
}

function formatPercent(v: any) {
  if (v === null || v === undefined || v === '') return '-'
  const s = String(v).trim()
  if (s.endsWith('%')) return s
  const n = Number(s)
  if (isNaN(n)) return s
  if (Math.abs(n) <= 1) return (n * 100).toFixed(2).replace(/\.0+$/, '') + '%'
  return n.toFixed(2).replace(/\.0+$/, '') + '%'
}

function formatMoney(v: any) {
  if (v === null || v === undefined || v === '') return '-'
  const n = Number(v)
  if (isNaN(n) || n === 0) return n === 0 ? '0' : '-'
  // 简单显示：大于亿显示 x.x 亿元，>万显示 x.x 万元，否则元
  if (Math.abs(n) >= 100000000) return (n / 100000000).toFixed(2) + ' 亿元'
  if (Math.abs(n) >= 10000) return (n / 10000).toFixed(2) + ' 万元'
  return n.toFixed(2) + ' 元'
}
</script>

<style scoped>
.issue-info .card-head { display:flex; justify-content:space-between; align-items:center }
.issue-info .card-head .title { font-size:18px; font-weight:700 }
.issue-info .card-head .meta { color:var(--text-secondary); font-size:14px }
.issue-grid-wrap { padding: 6px 0 }
.issue-grid { width:100%; border-collapse:collapse; table-layout:fixed }
.issue-grid th, .issue-grid td { padding:8px 10px; border:1px solid #ebeff2; vertical-align:middle }
.issue-grid th { width:180px; background:#f5f7fa; color:#666; font-weight:600; text-align:left }
.issue-grid td { color:#333 }
.issue-info .card-head { padding-bottom:6px }

.issuance-card { margin-bottom:12px; border:1px solid #e8eef6; border-radius:6px; overflow:hidden }
.issuance-header { background: linear-gradient(#f6fbff,#f2f9ff); padding:8px 12px; font-weight:600; color:#2c6fb5 }
.issuance-header .small { font-weight:400; color:#666; margin-left:8px; font-size:12px }

.issuer-line { padding:8px 0; color:#606266 }
.issuer-line strong { color:#303133; margin-left:8px }
</style>
