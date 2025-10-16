<template>
  <div class="home">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="gradient-text">智能证券分析系统</span>
        </h1>
        <p class="hero-subtitle">实时行情 · 数据分析 · 智能决策</p>
        <div class="hero-stats">
          <div class="stat-card">
            <div class="stat-icon">📈</div>
            <div class="stat-value">4000+</div>
            <div class="stat-label">A股</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">💹</div>
            <div class="stat-value">实时</div>
            <div class="stat-label">行情数据</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">🎯</div>
            <div class="stat-value">智能</div>
            <div class="stat-label">分析工具</div>
          </div>
        </div>
      </div>
    </div>

    <div class="quick-access">
      <h2 class="section-title">
        <span class="title-icon">⚡</span>
        快速入口
      </h2>
      <div class="access-grid">
        <router-link to="/market/summary" class="access-card">
          <div class="card-icon">📊</div>
          <div class="card-title">市场概况</div>
          <div class="card-desc">查看上交所每日交易概况</div>
        </router-link>
        <router-link to="/market/snapshot" class="access-card">
          <div class="card-icon">🏢</div>
          <div class="card-title">公司概况</div>
          <div class="card-desc">查询上市公司基本信息</div>
        </router-link>
        <router-link to="/market/kline" class="access-card">
          <div class="card-icon">📉</div>
          <div class="card-title">K线图表</div>
          <div class="card-desc">技术分析与走势预测</div>
        </router-link>
        <router-link to="/stock/history" class="access-card">
          <div class="card-icon">📈</div>
          <div class="card-title">历史行情</div>
          <div class="card-desc">查看个股历史数据</div>
        </router-link>
      </div>
    </div>

    <div class="chart-section">
      <h2 class="section-title">
        <span class="title-icon">📊</span>
        实时行情展示
      </h2>
      <stock-chart />
    </div>
  </div>
</template>

<script lang="ts" setup>
import StockChart from '@/components/StockChart.vue'
</script>

<style scoped>
.home {
  animation: fadeIn 0.4s ease;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 60px 40px;
  margin-bottom: 32px;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  border-radius: 50%;
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  color: white;
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 16px;
}

.gradient-text {
  background: linear-gradient(90deg, #fff 0%, rgba(255, 255, 255, 0.8) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 40px;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 32px;
  flex-wrap: wrap;
}

.stat-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 24px 32px;
  min-width: 140px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-4px);
}

.stat-icon {
  font-size: 2rem;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.9;
}

.quick-access {
  margin-bottom: 32px;
}

.section-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.title-icon {
  font-size: 1.5rem;
}

.access-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.access-card {
  background: linear-gradient(to bottom, #ffffff 0%, #fafbfc 100%);
  border-radius: 12px;
  padding: 28px 24px;
  text-align: center;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  text-decoration: none;
  color: inherit;
  border: 1px solid rgba(102, 126, 234, 0.1);
}

.access-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
  border-color: rgba(102, 126, 234, 0.3);
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
}

.card-desc {
  font-size: 0.9rem;
  color: #5a6c7d;
  line-height: 1.5;
}

.chart-section {
  background: white;
  border-radius: 16px;
  padding: 28px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .hero-section {
    padding: 40px 24px;
  }
  
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-stats {
    gap: 16px;
  }
  
  .stat-card {
    padding: 16px 20px;
    min-width: 100px;
  }
  
  .access-grid {
    grid-template-columns: 1fr;
  }
}
</style>
