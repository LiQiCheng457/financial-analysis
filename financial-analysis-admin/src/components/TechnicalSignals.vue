<template>
  <div class="technical-signals-panel">
    <!-- 综合建议卡片 -->
    <el-card class="advice-card" shadow="hover" v-if="advice">
      <template #header>
        <div class="card-header">
          <span>💡 综合交易建议</span>
          <el-tag :type="getAdviceTagType(advice.signal_type)" size="large">
            {{ advice.rating }}
          </el-tag>
        </div>
      </template>

      <div class="advice-content">
        <!-- 评分指示器 -->
        <div class="score-section">
          <div class="score-bar-container">
            <div class="score-labels">
              <span>强烈卖出</span>
              <span>卖出</span>
              <span>中性</span>
              <span>买入</span>
              <span>强烈买入</span>
            </div>
            <div class="score-bar">
              <div 
                class="score-indicator" 
                :style="{ left: `${advice.score}%` }"
                :class="getScoreColorClass(advice.score)"
              >
                <div class="score-value">{{ advice.score }}</div>
              </div>
            </div>
            <div class="score-sections">
              <div class="section danger"></div>
              <div class="section warning"></div>
              <div class="section info"></div>
              <div class="section success"></div>
              <div class="section primary"></div>
            </div>
          </div>
        </div>

        <!-- 建议说明 -->
        <el-alert 
          :type="getAdviceAlertType(advice.signal_type)" 
          :closable="false"
          class="advice-alert"
        >
          <template #title>
            <strong>{{ advice.advice }}</strong>
          </template>
        </el-alert>

        <!-- 统计信息 -->
        <div class="stats-row">
          <div class="stat-item">
            <div class="stat-label">买入信号</div>
            <div class="stat-value buy">{{ advice.buy_signals }}</div>
          </div>
          <div class="stat-item">
            <div class="stat-label">卖出信号</div>
            <div class="stat-value sell">{{ advice.sell_signals }}</div>
          </div>
          <div class="stat-item" v-if="advice.stop_loss">
            <div class="stat-label">建议止损</div>
            <div class="stat-value">{{ advice.stop_loss }}</div>
          </div>
          <div class="stat-item" v-if="advice.target_price">
            <div class="stat-label">目标价位</div>
            <div class="stat-value">{{ advice.target_price }}</div>
          </div>
        </div>

        <!-- 理由列表 -->
        <div class="reasons-section" v-if="advice.reasons && advice.reasons.length > 0">
          <div class="reasons-title">主要理由：</div>
          <ul class="reasons-list">
            <li v-for="(reason, index) in advice.reasons" :key="index">
              {{ reason }}
            </li>
          </ul>
        </div>
      </div>
    </el-card>

    <!-- 信号列表 -->
    <el-card class="signals-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <span>🎯 技术信号检测</span>
          <el-tag type="info">共 {{ signals.length }} 个信号</el-tag>
        </div>
      </template>

      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="5" animated />
      </div>

      <el-empty v-else-if="signals.length === 0" description="暂无检测到技术信号" />

      <el-timeline v-else>
        <el-timeline-item 
          v-for="(signal, index) in signals" 
          :key="index"
          :timestamp="formatDate(signal.date)"
          :color="getSignalColor(signal.type)"
          :icon="getSignalIcon(signal.type)"
        >
          <el-card class="signal-item" shadow="hover">
            <div class="signal-header">
              <div class="signal-title">
                <el-tag 
                  :type="signal.type === 'buy' ? 'success' : 'danger'"
                  size="large"
                >
                  {{ signal.indicator }}
                </el-tag>
                <span class="signal-name">{{ signal.name }}</span>
              </div>
              <div class="signal-strength">
                <span class="strength-label">强度</span>
                <el-rate 
                  v-model="signal.strength" 
                  disabled 
                  show-score 
                  :max="5"
                  score-template="{value}"
                />
              </div>
            </div>

            <div class="signal-description">
              {{ signal.description }}
            </div>

            <div class="signal-details" v-if="signal.price">
              <span class="detail-item">
                <span class="detail-label">价格：</span>
                <span class="detail-value">{{ signal.price }}</span>
              </span>
            </div>

            <!-- 详细数据（可展开） -->
            <el-collapse accordion v-if="signal.details">
              <el-collapse-item title="查看详细数据" name="details">
                <div class="details-content">
                  <div 
                    v-for="(value, key) in signal.details" 
                    :key="key"
                    class="detail-row"
                  >
                    <span class="key">{{ key }}:</span>
                    <span class="value">{{ formatValue(value) }}</span>
                  </div>
                </div>
              </el-collapse-item>
            </el-collapse>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </el-card>
  </div>
</template>

<script setup lang="ts">
// 移除未使用的 computed 导入
import { ArrowUp, ArrowDown } from '@element-plus/icons-vue'
import dayjs from 'dayjs'

interface SignalDetails {
  [key: string]: number | null
}

interface Signal {
  date: string
  type: 'buy' | 'sell'
  indicator: string
  name: string
  description: string
  strength: number
  price?: number
  details?: SignalDetails
}

interface Advice {
  signal_type: string
  score: number
  rating: string
  advice: string
  reasons: string[]
  stop_loss: number | null
  target_price: number | null
  buy_signals: number
  sell_signals: number
}

// Props - 使用 withDefaults 提供默认值以避免必需属性警告
// 注意：props 在模板中被隐式使用（Vue 3 setup 语法糖），不需要显式引用
defineProps<{
  signals: Signal[]
  advice: Advice | null
  loading?: boolean
}>()

// 格式化日期
const formatDate = (dateStr: string) => {
  return dayjs(dateStr).format('YYYY-MM-DD HH:mm')
}

// 格式化数值
const formatValue = (value: number | null) => {
  if (value === null || value === undefined) return '-'
  return typeof value === 'number' ? value.toFixed(2) : value
}

// 获取信号颜色
const getSignalColor = (type: string) => {
  return type === 'buy' ? '#67C23A' : '#F56C6C'
}

// 获取信号图标
const getSignalIcon = (type: string) => {
  return type === 'buy' ? ArrowUp : ArrowDown
}

// 获取建议标签类型
const getAdviceTagType = (signalType: string) => {
  const typeMap: Record<string, any> = {
    'strong_buy': 'success',
    'buy': 'success',
    'neutral': 'info',
    'sell': 'warning',
    'strong_sell': 'danger'
  }
  return typeMap[signalType] || 'info'
}

// 获取建议Alert类型
const getAdviceAlertType = (signalType: string) => {
  const typeMap: Record<string, any> = {
    'strong_buy': 'success',
    'buy': 'success',
    'neutral': 'info',
    'sell': 'warning',
    'strong_sell': 'error'
  }
  return typeMap[signalType] || 'info'
}

// 获取评分颜色类名
const getScoreColorClass = (score: number) => {
  if (score >= 70) return 'score-buy'
  if (score >= 55) return 'score-light-buy'
  if (score >= 45) return 'score-neutral'
  if (score >= 30) return 'score-light-sell'
  return 'score-sell'
}
</script>

<style scoped>
.technical-signals-panel {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: 600;
}

/* 综合建议卡片 */
.advice-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
}

.advice-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 评分区域 */
.score-section {
  padding: 20px 0;
}

.score-bar-container {
  position: relative;
}

.score-labels {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  font-size: 12px;
  color: #909399;
}

.score-bar {
  position: relative;
  height: 40px;
  margin-bottom: 4px;
}

.score-sections {
  display: flex;
  height: 40px;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}

.score-sections .section {
  flex: 1;
}

.score-sections .section.danger {
  background: linear-gradient(to right, #f56c6c, #e65555);
}

.score-sections .section.warning {
  background: linear-gradient(to right, #e65555, #f0a040);
}

.score-sections .section.info {
  background: linear-gradient(to right, #f0a040, #90c040);
}

.score-sections .section.success {
  background: linear-gradient(to right, #90c040, #67c23a);
}

.score-sections .section.primary {
  background: linear-gradient(to right, #67c23a, #409eff);
}

.score-indicator {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 10;
  transition: left 0.3s ease;
}

.score-value {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: white;
  border: 3px solid;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.score-indicator.score-sell .score-value {
  border-color: #f56c6c;
  color: #f56c6c;
}

.score-indicator.score-light-sell .score-value {
  border-color: #e6a23c;
  color: #e6a23c;
}

.score-indicator.score-neutral .score-value {
  border-color: #909399;
  color: #909399;
}

.score-indicator.score-light-buy .score-value {
  border-color: #67c23a;
  color: #67c23a;
}

.score-indicator.score-buy .score-value {
  border-color: #409eff;
  color: #409eff;
}

.advice-alert {
  margin: 12px 0;
}

.advice-alert :deep(.el-alert__title) {
  font-size: 15px;
  line-height: 1.6;
}

/* 统计行 */
.stats-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 16px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  font-size: 13px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.stat-value.buy {
  color: #67c23a;
}

.stat-value.sell {
  color: #f56c6c;
}

/* 理由区域 */
.reasons-section {
  padding: 16px;
  background: #fff9e6;
  border-left: 4px solid #e6a23c;
  border-radius: 4px;
}

.reasons-title {
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
}

.reasons-list {
  margin: 0;
  padding-left: 24px;
  line-height: 1.8;
  color: #606266;
}

.reasons-list li {
  margin-bottom: 8px;
}

/* 信号列表 */
.signals-card {
  flex: 1;
}

.loading-container {
  padding: 20px;
}

.signal-item {
  margin-bottom: 0;
}

.signal-item :deep(.el-card__body) {
  padding: 16px;
}

.signal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.signal-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.signal-name {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.signal-strength {
  display: flex;
  align-items: center;
  gap: 8px;
}

.strength-label {
  font-size: 13px;
  color: #909399;
}

.signal-description {
  color: #606266;
  line-height: 1.6;
  margin-bottom: 12px;
}

.signal-details {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #909399;
  padding-top: 12px;
  border-top: 1px solid #e4e7ed;
}

.detail-item {
  display: flex;
  gap: 4px;
}

.detail-label {
  color: #909399;
}

.detail-value {
  color: #303133;
  font-weight: 500;
}

.details-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 4px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
}

.detail-row .key {
  color: #909399;
  font-weight: 500;
}

.detail-row .value {
  color: #303133;
  font-family: 'Consolas', 'Monaco', monospace;
}
</style>
