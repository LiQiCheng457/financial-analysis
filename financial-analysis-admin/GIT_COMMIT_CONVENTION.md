# Git 提交规范

## 提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

- **feat**: 新功能
- **fix**: 修复 bug
- **docs**: 文档变更
- **style**: 代码格式（不影响代码运行的变动）
- **refactor**: 重构（既不是新增功能，也不是修改 bug 的代码变动）
- **perf**: 性能优化
- **test**: 增加测试
- **chore**: 构建过程或辅助工具的变动
- **revert**: 回滚

### Scope 范围

- **api**: API 接口层
- **components**: 组件
- **views**: 视图页面
- **store**: 状态管理
- **utils**: 工具函数
- **styles**: 样式
- **types**: 类型定义
- **config**: 配置文件

### 示例

```bash
feat(components): 添加股票搜索组件

- 实现自动补全功能
- 支持搜索历史
- 添加收藏功能

Closes #123
```

```bash
fix(api): 修复股票数据获取失败的问题

修复了在某些情况下 API 请求返回 undefined 的问题
```

```bash
docs(readme): 更新项目文档

更新了安装说明和使用指南
```

```bash
style(components): 统一组件代码格式

使用 ESLint 和 Prettier 格式化代码
```

```bash
refactor(store): 重构用户状态管理

使用 TypeScript 类型定义优化 store
```
