<template>
  <div class="strategy-metrics">
    <el-skeleton :rows="2" animated v-if="loading" />
    <div v-else class="metrics-grid">
      <div class="metric-card total-return">
        <div class="metric-icon">📊</div>
        <div class="metric-content">
          <div class="metric-label">总收益率</div>
          <div class="metric-value">{{ metrics.totalReturn }}%</div>
          <div class="metric-desc">策略期间累计收益</div>
        </div>
      </div>

      <div class="metric-card annual-return">
        <div class="metric-icon">📈</div>
        <div class="metric-content">
          <div class="metric-label">年化收益</div>
          <div class="metric-value">{{ metrics.annualReturn }}%</div>
          <div class="metric-desc">年化后的收益率</div>
        </div>
      </div>

      <div class="metric-card sharpe-ratio">
        <div class="metric-icon">⚖️</div>
        <div class="metric-content">
          <div class="metric-label">夏普比率</div>
          <div class="metric-value">{{ metrics.sharpeRatio }}</div>
          <div class="metric-desc">风险调整后收益</div>
          <el-tag v-if="metrics.sharpeRatio >= 1.5" type="success" size="small" effect="dark">
            优秀
          </el-tag>
        </div>
      </div>

      <div class="metric-card max-drawdown">
        <div class="metric-icon">📉</div>
        <div class="metric-content">
          <div class="metric-label">最大回撤</div>
          <div class="metric-value danger">{{ metrics.maxDrawdown }}%</div>
          <div class="metric-desc">最大亏损幅度</div>
        </div>
      </div>

      <div class="metric-card trading-info">
        <div class="metric-icon">🔄</div>
        <div class="metric-content">
          <div class="metric-label">交易信息</div>
          <div class="metric-stats">
            <div class="stat-item">
              <span class="stat-label">交易次数：</span>
              <span class="stat-value">{{ metrics.totalTrades }}</span>
            </div>
            <div class="stat-item">
              <span class="stat-label">回测天数：</span>
              <span class="stat-value">{{ metrics.tradingDays }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="metric-card performance-badge">
        <div class="badge-content">
          <div class="badge-icon">🏆</div>
          <div class="badge-text">
            <div class="badge-title">策略评级</div>
            <div class="badge-rating">{{ getPerformanceRating() }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Metrics {
  totalReturn: number
  annualReturn: number
  sharpeRatio: number
  maxDrawdown: number
  tradingDays: number
  totalTrades: number
}

interface Props {
  metrics: Metrics
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false
})

const getPerformanceRating = () => {
  const { annualReturn, sharpeRatio } = props.metrics
  
  if (annualReturn >= 15 && sharpeRatio >= 1.5) {
    return '卓越 ⭐⭐⭐⭐⭐'
  } else if (annualReturn >= 10 && sharpeRatio >= 1.2) {
    return '优秀 ⭐⭐⭐⭐'
  } else if (annualReturn >= 5 && sharpeRatio >= 1.0) {
    return '良好 ⭐⭐⭐'
  } else {
    return '一般 ⭐⭐'
  }
}
</script>

<style scoped lang="scss">
.strategy-metrics {
  margin: 20px 0;

  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;

    .metric-card {
      background: white;
      border-radius: 12px;
      padding: 24px;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
      transition: all 0.3s;
      position: relative;
      overflow: hidden;

      &::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
      }

      &:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
      }

      &.total-return {
        --gradient-start: #667eea;
        --gradient-end: #764ba2;
      }

      &.annual-return {
        --gradient-start: #f093fb;
        --gradient-end: #f5576c;
      }

      &.sharpe-ratio {
        --gradient-start: #4facfe;
        --gradient-end: #00f2fe;
      }

      &.max-drawdown {
        --gradient-start: #fa709a;
        --gradient-end: #fee140;
      }

      &.trading-info {
        --gradient-start: #30cfd0;
        --gradient-end: #330867;
      }

      &.performance-badge {
        --gradient-start: #ffd89b;
        --gradient-end: #19547b;
        display: flex;
        align-items: center;
        justify-content: center;
      }

      .metric-icon {
        font-size: 48px;
        margin-bottom: 12px;
        display: inline-block;
      }

      .metric-content {
        .metric-label {
          font-size: 14px;
          color: #909399;
          margin-bottom: 8px;
        }

        .metric-value {
          font-size: 36px;
          font-weight: 700;
          color: #303133;
          margin-bottom: 8px;
          line-height: 1;

          &.danger {
            color: #f56c6c;
          }
        }

        .metric-desc {
          font-size: 12px;
          color: #c0c4cc;
          margin-bottom: 8px;
        }

        .metric-stats {
          margin-top: 12px;

          .stat-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #f0f0f0;

            &:last-child {
              border-bottom: none;
            }

            .stat-label {
              font-size: 14px;
              color: #909399;
            }

            .stat-value {
              font-size: 16px;
              font-weight: 600;
              color: #303133;
            }
          }
        }
      }

      .badge-content {
        display: flex;
        align-items: center;
        gap: 16px;

        .badge-icon {
          font-size: 64px;
        }

        .badge-text {
          .badge-title {
            font-size: 14px;
            color: #909399;
            margin-bottom: 8px;
          }

          .badge-rating {
            font-size: 24px;
            font-weight: 700;
            color: #303133;
          }
        }
      }
    }
  }

  @media (max-width: 768px) {
    .metrics-grid {
      grid-template-columns: 1fr;
    }
  }
}
</style>
