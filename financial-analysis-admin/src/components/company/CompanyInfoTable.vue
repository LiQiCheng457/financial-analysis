<template>
  <div class="profile-title">
    <span class="title-icon">●</span>
    <span class="title-text">基本资料</span>
  </div>

  <div class="info-table">
    <div class="info-row">
      <div class="info-label">A股代码</div>
      <div class="info-value code-text">{{ profile?.a_stock_code || '—' }}</div>
      <div class="info-label">A股简称</div>
      <div class="info-value code-text">{{ profile?.a_stock_abbr || '—' }}</div>
    </div>
    <div class="info-row">
      <div class="info-label">A股扩位简称</div>
      <div class="info-value">{{ profile?.former_name || '—' }}</div>
      <div class="info-label">曾用名</div>
      <div class="info-value">{{ profile?.former_name || '—' }}</div>
    </div>
    <div class="info-row">
      <div class="info-label">证券类别</div>
      <div class="info-value">{{ profile?.security_category || '—' }}</div>
      <div class="info-label">所属东财行业</div>
      <div class="info-value industry-text">{{ profile?.eastmoney_industry || profile?.regulatory_industry || '—' }}</div>
    </div>
    <div class="info-row">
      <div class="info-label">上市交易所</div>
      <div class="info-value">{{ profile?.listing_exchange || '—' }}</div>
      <div class="info-label">所属证监会行业</div>
      <div class="info-value industry-text">{{ profile?.regulatory_industry || '—' }}</div>
    </div>
    <div class="info-row">
      <div class="info-label">发行机关</div>
      <div class="info-value">{{ profile?.issuing_authority || profile?.issuing_authority || '—' }}</div>
      <div class="info-label">（若无则显示发行记录中的保荐机构）</div>
      <div class="info-value">{{ (profile?.issuing_authority || (profile?.issuance && profile.issuance[0] && (profile.issuance[0].sponsor_institution || profile.issuance[0].issuing_institution))) || '—' }}</div>
    </div>
    <div class="info-row">
      <div class="info-label">总经理</div>
      <div class="info-value person-text">{{ profile?.general_manager || '—' }}</div>
      <div class="info-label">法人代表</div>
      <div class="info-value person-text">{{ profile?.legal_representative || '—' }}</div>
    </div>
    <div class="info-row">
      <div class="info-label">董秘</div>
      <div class="info-value person-text">{{ profile?.board_secretary || '—' }}</div>
      <div class="info-label">董事长</div>
      <div class="info-value person-text">{{ profile?.chairman || '—' }}</div>
    </div>
    <div class="info-row">
      <div class="info-label">证券事务代表</div>
      <div class="info-value person-text">{{ profile?.securities_representative || '—' }}</div>
      <div class="info-label">独立董事</div>
      <div class="info-value person-text">{{ profile?.independent_directors || '—' }}</div>
    </div>
    <div class="info-row">
      <div class="info-label">联系电话</div>
      <div class="info-value">{{ profile?.contact_phone || '—' }}</div>
      <div class="info-label">电子信箱</div>
      <div class="info-value">{{ profile?.email || '—' }}</div>
    </div>
    <div class="info-row">
      <div class="info-label">传真</div>
      <div class="info-value">{{ profile?.fax || '—' }}</div>
      <div class="info-label">公司网址</div>
      <div class="info-value">
        <a v-if="profile?.website" :href="formatUrl(profile.website)" target="_blank" rel="noopener noreferrer">{{ profile.website }}</a>
        <span v-else>—</span>
      </div>
    </div>
    <div class="info-row">
      <div class="info-label">办公地址</div>
      <div class="info-value" style="grid-column: 2 / 5;">{{ profile?.office_address || '—' }}</div>
    </div>
    <div class="info-row">
      <div class="info-label">注册地址</div>
      <div class="info-value" style="grid-column: 2 / 5;">{{ profile?.registered_address || '—' }}</div>
    </div>
    <div class="info-row">
      <div class="info-label">区域</div>
      <div class="info-value">{{ profile?.region || '—' }}</div>
      <div class="info-label">邮政编码</div>
      <div class="info-value">{{ profile?.postal_code || '—' }}</div>
    </div>
    <div class="info-row">
      <div class="info-label">注册资本(元)</div>
      <div class="info-value highlight">{{ formatCapital(profile?.registered_capital) }}</div>
      <div class="info-label">工商登记</div>
      <div class="info-value">{{ profile?.business_registration || '—' }}</div>
    </div>
    <div class="info-row">
      <div class="info-label">雇员人数</div>
      <div class="info-value">{{ profile?.employee_count || '—' }}</div>
      <div class="info-label">管理人员人数</div>
      <div class="info-value">{{ profile?.management_count || '—' }}</div>
    </div>
    <div class="info-row">
      <div class="info-label">律师事务所</div>
      <div class="info-value" style="grid-column: 2 / 5;">{{ profile?.law_firm || '—' }}</div>
    </div>
    <div class="info-row">
      <div class="info-label">会计师事务所</div>
      <div class="info-value" style="grid-column: 2 / 5;">{{ profile?.accounting_firm || '—' }}</div>
    </div>
    <div class="info-row full-width">
      <div class="info-label">公司简介</div>
      <div class="info-value" style="grid-column: 2 / 5;">{{ profile?.company_intro || '—' }}</div>
    </div>
    <div class="info-row full-width">
      <div class="info-label">经营范围</div>
      <div class="info-value" style="grid-column: 2 / 5;">{{ profile?.business_scope || '—' }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

defineProps<{
  profile: Record<string, any> | null
}>()

function formatUrl(url?: string) {
  if (!url) return '#'
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  return `http://${url}`
}

function formatCapital(value: string | number | undefined) {
  if (value === null || value === undefined) return '-'
  const strValue = String(value)
  if (strValue.includes('亿') || strValue.includes('万') || strValue.includes('元')) {
    return strValue
  }
  const num = Number(value)
  if (isNaN(num)) return '-'
  if (num >= 100000000) {
    return (num / 100000000).toFixed(2) + ' 亿元'
  }
  if (num >= 10000) {
    return (num / 10000).toFixed(2) + ' 万元'
  }
  return num.toFixed(2) + ' 元'
}
</script>

<style scoped>
.profile-title {
  background: #e8f4ff;
  padding: 10px 16px;
  border-bottom: 1px solid #d0e8f7;
  display: flex;
  align-items: center;
  gap: 8px;
}

.title-icon {
  color: #5ba4d6;
  font-size: 0.8rem;
}

.title-text {
  font-size: 0.95rem;
  font-weight: 600;
  color: #333;
}

.info-table {
  display: block;
}

.info-row {
  display: grid;
  grid-template-columns: 140px 1fr 140px 1fr;
  border-bottom: 1px solid #e5e5e5;
  min-height: 36px;
}

.info-row:last-child {
  border-bottom: none;
}

.info-row.full-width {
  grid-template-columns: 140px 1fr;
}

.info-label {
  background: #f5f5f5;
  padding: 8px 12px;
  font-size: 0.85rem;
  color: #666;
  border-right: 1px solid #e5e5e5;
  display: flex;
  align-items: center;
}

.info-value {
  padding: 8px 12px;
  font-size: 0.85rem;
  color: #333;
  display: flex;
  align-items: center;
  word-break: break-word;
  background: white;
  border-right: 1px solid #e5e5e5;
}

.info-row .info-value:last-child {
  border-right: none;
}

.info-value a {
  color: #1890ff;
  text-decoration: underline;
}

.code-text {
  color: #1890ff;
  font-family: 'Consolas', 'Monaco', monospace;
}

.industry-text {
  color: #d48806;
}

.person-text {
  color: #333;
}

.highlight {
  color: #cf1322;
  font-weight: 600;
}
</style>