# 重构进度追踪

**开始日期：** 2025-01-16  
**更新日期：** 2025-01-16

---

## 📊 总体进度

- **完成度：** 5%
- **预计完成：** 8 weeks
- **当前阶段：** 阶段 1 - 前端组件拆分

---

## ✅ 已完成

### 阶段 1：前端基础架构 (5%)

#### Composables（组合式 API）
- [x] `useSearch.ts` - 搜索功能封装（防抖、加载状态）
- [x] `usePagination.ts` - 分页功能封装（页码管理、数据加载）
- [x] `useForm.ts` - 表单功能封装（验证、提交、重置）
- [x] `useStock.ts` - 股票相关功能（搜索、历史、实时）

#### 原子组件
- [x] `BaseCard.vue` - 基础卡片组件（3种变体）
- [x] `BaseEmpty.vue` - 空状态组件（3种尺寸）

#### 业务组件
- [x] `CompanySearchPanel.vue` - 公司搜索面板（搜索栏 + 行业标签）

---

## 🚧 进行中

### 阶段 1：前端组件拆分 (继续)

#### 待创建 Composables
- [ ] `useCompany.ts` - 公司相关功能
- [ ] `useChart.ts` - 图表相关功能
- [ ] `useTable.ts` - 表格相关功能
- [ ] `useAuth.ts` - 认证相关功能
- [ ] `useUser.ts` - 用户相关功能
- [ ] `useDebounce.ts` - 防抖节流工具

#### 待创建原子组件
- [ ] `BaseButton.vue` - 基础按钮
- [ ] `BaseInput.vue` - 基础输入框
- [ ] `BaseTag.vue` - 基础标签
- [ ] `BaseBadge.vue` - 基础徽章
- [ ] `BaseLoading.vue` - 加载状态
- [ ] `BaseDialog.vue` - 基础对话框

#### 待创建业务组件
- [ ] `CompanyInfoTable.vue` - 公司信息表格
- [ ] `CompanyDetailCard.vue` - 公司详情卡片
- [ ] `CompanyIndustryTags.vue` - 行业标签组件
- [ ] `StockSearchBar.vue` - 股票搜索栏
- [ ] `StockTable.vue` - 股票列表表格
- [ ] `KLineChart.vue` - K线图
- [ ] `LineChart.vue` - 折线图

#### 待重构大型组件
- [ ] `Snapshot.vue` -> `market/snapshot/index.vue` + 子组件
- [ ] `Profile.vue` -> `user/profile/index.vue` + 子组件
- [ ] `KLine.vue` -> `market/kline/index.vue` + 子组件

---

## 📅 后续阶段

### 阶段 2：前端视图重构 (0%)
- [ ] 重构视图目录结构
- [ ] 拆分大型视图文件
- [ ] 统一使用 index.vue 入口

### 阶段 3：前端类型系统 (0%)
- [ ] 定义 API 接口类型
- [ ] 定义模型类型
- [ ] 定义 Store 类型

### 阶段 4：后端 API 重构 (0%)
- [ ] 按模块拆分 API 路由
- [ ] 实现 v1 版本 API
- [ ] 添加 API 版本控制

### 阶段 5：后端 Service 重构 (0%)
- [ ] 拆分 stock_service.py
- [ ] 创建模块化服务
- [ ] 实现缓存层

### 阶段 6：后端模型重构 (0%)
- [ ] 按模块组织模型
- [ ] 拆分大型模型文件

### 阶段 7：测试与优化 (0%)
- [ ] 单元测试
- [ ] 集成测试
- [ ] 性能测试

---

## 📝 重要笔记

### 设计原则
1. **单一职责**：每个组件/函数只做一件事
2. **可复用性**：优先创建可复用的通用组件
3. **类型安全**：全面使用 TypeScript 类型定义
4. **性能优先**：使用懒加载、虚拟滚动、缓存等优化手段

### 命名规范
- **组件文件**：PascalCase（如 `CompanySearchPanel.vue`）
- **工具文件**：camelCase（如 `formatDate.ts`）
- **视图文件**：统一使用 `index.vue`
- **变量/函数**：camelCase
- **常量**：UPPER_SNAKE_CASE
- **类型/接口**：PascalCase

### 技术债务
- ⚠️ `Snapshot.vue` 超过 1000 行，急需重构
- ⚠️ 缺少统一的错误处理机制
- ⚠️ 部分组件缺少类型定义
- ⚠️ 样式代码重复率高

---

## 🎯 下一步行动

### 优先级 1（本周）
1. 完成剩余 Composables（useCompany, useChart, useTable）
2. 创建常用原子组件（BaseButton, BaseInput, BaseTag）
3. 重构 Snapshot.vue（拆分为 3-4 个子组件）

### 优先级 2（下周）
1. 重构 Profile.vue（拆分为 4 个 Tab 组件）
2. 重构 KLine.vue（拆分图表工具栏和指标面板）
3. 创建通用业务组件（DataTable, FilterPanel）

### 优先级 3（后续）
1. 重构后端 API 路由
2. 拆分后端 Service 层
3. 编写单元测试

---

**维护者：** 开发团队  
**最后更新：** 2025-01-16
