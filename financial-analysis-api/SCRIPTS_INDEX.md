# 项目脚本代码清单

## 📋 概述

本项目包含多个 Python 脚本和 Shell 脚本，用于数据库管理、数据导入、自动更新、系统维护等功能。

**统计信息**：
- Python 脚本：19 个
- Shell 脚本：2 个
- 总计：21 个脚本

---

## 🎯 核心脚本（根目录）

### 1. `main.py` - 主服务入口
**位置**: `financial-analysis-api/main.py`  
**用途**: FastAPI 应用主入口，启动 Web 服务  
**运行**: `python main.py` 或 `uvicorn main:app --reload`

**功能**：
- 启动 FastAPI 服务
- 集成自动更新功能（如果启用）
- 提供 API 接口（股票数据、用户管理、技术分析等）

---

### 2. `migrate.py` - 数据库迁移管理 ⭐
**位置**: `financial-analysis-api/migrate.py`  
**用途**: 简化的数据库迁移管理工具（Alembic 包装器）  
**运行**: `python migrate.py [命令]`

**主要命令**：
```bash
python migrate.py help              # 查看帮助
python migrate.py current           # 查看当前版本
python migrate.py create "描述"     # 创建迁移
python migrate.py upgrade           # 应用迁移
python migrate.py downgrade         # 回滚迁移
python migrate.py history           # 查看历史
python migrate.py stamp head        # 标记版本
```

**特点**：
- ✅ 中文提示和交互确认
- ✅ 自动检测模型变化
- ✅ 从 .env 读取数据库配置
- ✅ 支持版本控制和回滚

**文档**: `DATABASE_MIGRATION_GUIDE.md`

---

### 3. `migration_example.py` - 迁移示例
**位置**: `financial-analysis-api/migration_example.py`  
**用途**: 数据库迁移实战示例代码  
**运行**: 仅作为参考，不直接运行

**内容**：
- 如何创建新模型
- 如何生成迁移文件
- 如何应用迁移
- 完整的工作流程示例

---

## 📦 数据管理脚本（scripts/）

### 4. `auto_update.py` - 自动更新股票数据 ⭐⭐⭐
**位置**: `scripts/auto_update.py`  
**用途**: 自动更新股票历史数据（Tushare API）  
**运行**: 
```bash
# 立即执行一次
python scripts/auto_update.py --run-once

# 启动定时调度器
python scripts/auto_update.py --run-scheduler --time 20:00

# 更新单只股票
python scripts/auto_update.py --stock SH600000
```

**功能**：
- ✅ 自动更新 4500+ 只股票数据
- ✅ 交易日智能判断
- ✅ 增量更新（从最新日期开始）
- ✅ API 限制保护（1.5秒/次）
- ✅ 详细日志记录
- ✅ 进度显示和预计时间
- ✅ 可集成到 FastAPI 服务

**配置**（.env）：
```bash
ENABLE_AUTO_UPDATE=1
TUSHARE_TOKEN=your_token
AUTO_UPDATE_TIME=20:00
AUTO_UPDATE_ON_STARTUP=1
```

**日志**: `logs/stock_data_update.log`

---

### 5. `import_historical.py` - 历史数据导入
**位置**: `scripts/import_historical.py`  
**用途**: 从 CSV/Excel 导入历史数据  
**运行**: 
```bash
python scripts/import_historical.py --file data/000001.csv --ts-code 000001.SZ
```

**功能**：
- 支持 CSV、Excel 格式
- 自动处理日期格式
- 批量插入优化
- 错误处理

---

### 6. `fetch_stock_history.py` - 抓取股票历史
**位置**: `scripts/fetch_stock_history.py`  
**用途**: 从 Tushare API 抓取单只股票历史数据  
**运行**: 
```bash
python scripts/fetch_stock_history.py
```

**功能**：
- 抓取指定股票的历史数据
- 保存到数据库

---

## 🔍 查询和检查脚本（scripts/）

### 7. `show_tables.py` - 显示所有表
**位置**: `scripts/show_tables.py`  
**用途**: 列出数据库中所有的表  
**运行**: `python scripts/show_tables.py`

**输出示例**：
```
数据库表列表：
1. users
2. stock_basic_info
3. stock_daily_data
4. alembic_version
```

---

### 8. `show_table_fields.py` - 显示表结构
**位置**: `scripts/show_table_fields.py`  
**用途**: 查看指定表的字段结构  
**运行**: `python scripts/show_table_fields.py`

**功能**：
- 显示字段名、类型、是否可空
- 显示主键、索引信息

---

### 9. `check_table_structure.py` - 检查表结构
**位置**: `scripts/check_table_structure.py`  
**用途**: 检查数据库表结构是否正确  
**运行**: `python scripts/check_table_structure.py`

**检查项**：
- 必需表是否存在
- 字段是否完整
- 索引是否正确

---

### 10. `inspect_stock_tables.py` - 检查股票表
**位置**: `scripts/inspect_stock_tables.py`  
**用途**: 检查股票相关表的数据情况  
**运行**: `python scripts/inspect_stock_tables.py`

**功能**：
- 统计各表记录数
- 检查数据完整性
- 显示样本数据

---

### 11. `query_stock_code.py` - 查询股票代码
**位置**: `scripts/query_stock_code.py`  
**用途**: 根据名称或代码查询股票信息  
**运行**: `python scripts/query_stock_code.py`

**功能**：
- 模糊搜索股票
- 显示基本信息
- 行业分类

---

### 12. `query_company.py` - 查询公司信息
**位置**: `scripts/query_company.py`  
**用途**: 查询公司详细信息  
**运行**: `python scripts/query_company.py`

**功能**：
- 公司基本信息
- 财务指标
- 股东信息

---

### 13. `query_industry_tags.py` - 查询行业标签
**位置**: `scripts/query_industry_tags.py`  
**用途**: 查询和统计行业标签  
**运行**: `python scripts/query_industry_tags.py`

**功能**：
- 列出所有行业标签
- 统计每个行业的股票数量
- 支持按行业筛选

---

### 14. `generate_simplified_tags.py` - 生成简化标签
**位置**: `scripts/generate_simplified_tags.py`  
**用途**: 生成和优化行业标签  
**运行**: `python scripts/generate_simplified_tags.py`

**功能**：
- 简化行业分类
- 生成标签层级
- 数据清洗

---

## 👤 用户管理脚本（scripts/）

### 15. `reset_admin.py` - 重置管理员密码
**位置**: `scripts/reset_admin.py`  
**用途**: 重置管理员账户密码  
**运行**: `python scripts/reset_admin.py`

**功能**：
- 重置 admin 用户密码
- 确保管理员权限
- 安全性验证

**默认密码**: `admin123`（首次登录后建议修改）

---

### 16. `test_profile.py` - 测试用户配置
**位置**: `scripts/test_profile.py`  
**用途**: 测试用户相关功能  
**运行**: `python scripts/test_profile.py`

**功能**：
- 测试用户 API
- 验证权限系统
- 调试用户功能

---

## 💾 备份脚本

### 17. `backup_db.bat` - Windows 数据库备份
**位置**: `financial-analysis-api/backup_db.bat`  
**用途**: Windows 环境下备份数据库  
**运行**: 双击运行或 `backup_db.bat`

**功能**：
- 从 .env 读取数据库配置
- 使用 mysqldump 备份
- 自动生成带时间戳的文件名
- 保存到 backups/ 目录

**备份文件格式**: `backups/financial_analysis_db_20251101_153045.sql`

---

### 18. `backup_db.sh` - Linux/Mac 数据库备份
**位置**: `financial-analysis-api/backup_db.sh`  
**用途**: Linux/Mac 环境下备份数据库  
**运行**: `bash backup_db.sh`

**功能**：
- 从 .env 读取数据库配置
- 使用 mysqldump 备份
- 自动压缩（gzip）
- 自动清理 7 天前的备份
- 保存到 backups/ 目录

**备份文件格式**: `backups/financial_analysis_db_20251101_153045.sql.gz`

---

## 🗄️ 数据库迁移脚本（alembic/）

### 19. `alembic/env.py` - Alembic 环境配置
**位置**: `alembic/env.py`  
**用途**: Alembic 迁移环境配置  
**运行**: 由 Alembic 自动调用

**功能**：
- 配置数据库连接
- 导入所有模型
- 支持离线/在线迁移

---

### 20. `alembic/versions/*.py` - 迁移文件
**位置**: `alembic/versions/`  
**用途**: 数据库迁移版本文件  
**运行**: 由 `migrate.py` 或 `alembic` 执行

**现有迁移**：
- `4f3b2c1a9d3e_add_role_to_users.py` - 添加用户角色字段

---

### 21. `migrations/migrate_user_fields.py` - 用户字段迁移
**位置**: `migrations/migrate_user_fields.py`  
**用途**: 迁移用户表字段（旧版本）  
**运行**: `python migrations/migrate_user_fields.py`

**注意**: 新项目建议使用 Alembic 迁移系统

---

## 📊 脚本分类汇总

### 按功能分类

| 分类 | 脚本数量 | 脚本列表 |
|------|---------|---------|
| **核心服务** | 1 | main.py |
| **数据库迁移** | 3 | migrate.py, migration_example.py, alembic/env.py |
| **数据更新** | 3 | auto_update.py, import_historical.py, fetch_stock_history.py |
| **数据查询** | 5 | query_stock_code.py, query_company.py, query_industry_tags.py, show_tables.py, show_table_fields.py |
| **数据检查** | 3 | check_table_structure.py, inspect_stock_tables.py, generate_simplified_tags.py |
| **用户管理** | 2 | reset_admin.py, test_profile.py |
| **数据备份** | 2 | backup_db.bat, backup_db.sh |
| **其他** | 2 | 迁移版本文件, migrate_user_fields.py |

### 按使用频率分类

**⭐⭐⭐ 高频使用（每天/每周）**：
1. `main.py` - 启动服务
2. `auto_update.py` - 自动更新数据
3. `migrate.py` - 数据库迁移
4. `backup_db.bat/sh` - 数据库备份

**⭐⭐ 中频使用（按需）**：
1. `reset_admin.py` - 密码重置
2. `query_stock_code.py` - 查询股票
3. `check_table_structure.py` - 检查表结构

**⭐ 低频使用（偶尔）**：
1. `import_historical.py` - 导入历史数据（首次部署）
2. `migration_example.py` - 学习参考
3. 其他查询和检查脚本

---

## 🚀 快速使用指南

### 日常开发

```bash
# 1. 启动服务
python main.py

# 2. 查看数据库版本
python migrate.py current

# 3. 修改模型后创建迁移
python migrate.py create "描述修改"
python migrate.py upgrade

# 4. 手动触发数据更新
python scripts/auto_update.py --run-once

# 5. 查看日志
Get-Content logs\stock_data_update.log -Encoding UTF8 -Wait
```

### 首次部署

```bash
# 1. 配置环境变量
# 编辑 .env 文件

# 2. 数据库迁移
python migrate.py upgrade

# 3. 重置管理员密码
python scripts/reset_admin.py

# 4. 导入历史数据（可选）
python scripts/import_historical.py

# 5. 启动服务
python main.py
```

### 生产环境维护

```bash
# 1. 备份数据库
backup_db.bat  # Windows
bash backup_db.sh  # Linux/Mac

# 2. 应用迁移
python migrate.py upgrade

# 3. 检查表结构
python scripts/check_table_structure.py

# 4. 检查数据情况
python scripts/inspect_stock_tables.py

# 5. 重启服务
python main.py
```

---

## 📖 相关文档

| 文档 | 说明 |
|------|------|
| `DATABASE_MIGRATION_GUIDE.md` | 数据库迁移完整指南 |
| `MIGRATION_QUICKSTART.md` | 迁移快速参考 |
| `scripts/README.md` | 数据脚本使用说明 |
| `README.md` | 项目主文档 |

---

## ⚙️ 环境变量配置

所有脚本共享以下环境变量（.env 文件）：

```bash
# 数据库配置
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USER=root
DATABASE_PASSWORD=your_password
DATABASE_NAME=financial_analysis_db

# Tushare 配置
TUSHARE_TOKEN=your_tushare_token

# 自动更新配置
ENABLE_AUTO_UPDATE=1
AUTO_UPDATE_TIME=20:00
AUTO_UPDATE_ON_STARTUP=1
```

---

## 🔧 依赖要求

### Python 包
```
fastapi
uvicorn
sqlalchemy
pymysql
alembic
python-dotenv
tushare
pandas
openpyxl
bcrypt
python-jose
```

### 系统工具
- MySQL 客户端（mysqldump）- 用于备份
- Python 3.8+

---

## 📞 技术支持

如有问题，请查看：
1. 相关文档（上述列表）
2. 脚本内的注释和帮助信息
3. 日志文件（logs/）

---

**最后更新**: 2025-11-01  
**版本**: 1.0.0  
**项目**: 金融分析系统
