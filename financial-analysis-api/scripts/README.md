# 股票历史数据管理脚本 / Historical Data Scripts

本目录包含用于导入和自动更新股票历史日线数据（OHLCV）的辅助脚本。

This folder contains helper scripts for importing and automatically updating historical daily OHLCV data into the project's `stock_daily_data` table.

## 📁 文件说明 / Files

| 文件 | 说明 | Description |
|------|------|-------------|
| `import_historical.py` | 历史数据导入工具（CSV/Excel） | Simple CLI for importing CSV/Excel files |
| `auto_update.py` | 自动更新工具（Tushare API） | Automatic updater with scheduler |

## 🔧 环境变量配置 / Environment Variables

### 必需配置 / Required

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DATABASE_HOST` | 数据库主机 | `localhost` |
| `DATABASE_USER` | 数据库用户名 | `root` |
| `DATABASE_PASSWORD` | 数据库密码 | *(空)* |
| `DATABASE_NAME` | 数据库名称 | `financial_analysis_db` |
| `TUSHARE_TOKEN` | Tushare Pro Token（注册获取）| *(必填)* |

### 可选配置 / Optional

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `ENABLE_AUTO_UPDATE` | 启用自动更新（1=启用）| `0` |
| `AUTO_UPDATE_TIME` | 每天更新时间（HH:MM）| `20:00` |
| `AUTO_UPDATE_ON_STARTUP` | 启动时立即更新（1=是）| `0` |
| `DATABASE_CHARSET` | 数据库字符集 | `utf8mb4` |

## 📖 使用示例 / Examples

### 1️⃣ 导入历史数据（CSV/Excel）

```powershell
# PowerShell
$env:DATABASE_HOST='localhost'
$env:DATABASE_USER='root'
$env:DATABASE_PASSWORD='your_password'
$env:DATABASE_NAME='financial_analysis_db'

python scripts/import_historical.py --file data/000001.csv --ts-code 000001.SZ
```

```bash
# Bash
export DATABASE_HOST=localhost
export DATABASE_USER=root
export DATABASE_PASSWORD=your_password
export DATABASE_NAME=financial_analysis_db

python scripts/import_historical.py --file data/000001.csv --ts-code 000001.SZ
```

### 2️⃣ 立即执行一次更新（Tushare API）

适用场景：测试、手动触发、首次增量更新

```powershell
# PowerShell
$env:TUSHARE_TOKEN='your_tushare_token'
python scripts/auto_update.py --run-once
```

```bash
# Bash
export TUSHARE_TOKEN=your_tushare_token
python scripts/auto_update.py --run-once
```

### 3️⃣ 启动定时调度器（独立运行）

适用场景：不启动 FastAPI 服务，但需要定时更新

```powershell
# PowerShell - 每天 20:00 自动更新
$env:TUSHARE_TOKEN='your_token'
python scripts/auto_update.py --run-scheduler --time 20:00
```

```bash
# Bash
export TUSHARE_TOKEN=your_token
python scripts/auto_update.py --run-scheduler --time 20:00
```

### 4️⃣ 集成到 FastAPI 服务（推荐）

在 `.env` 文件中配置：

```bash
ENABLE_AUTO_UPDATE=1
TUSHARE_TOKEN=your_tushare_token
AUTO_UPDATE_TIME=20:00
AUTO_UPDATE_ON_STARTUP=1  # 可选：启动时立即更新
```

然后正常启动服务：

```bash
python main.py
# 或
uvicorn main:app --reload
```

服务启动后：
- ✅ 如果 `AUTO_UPDATE_ON_STARTUP=1`，会在后台线程立即执行一次更新
- ✅ 定时调度器会在每天 `AUTO_UPDATE_TIME` 自动执行更新
- ✅ 休市日自动跳过更新

### 5️⃣ 更新单只股票（调试用）

```bash
python scripts/auto_update.py --stock SH600000
```

## 🚀 快速开始 / Quick Start

### 首次部署流程

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量（复制模板并编辑）
cp .env.example .env
# 编辑 .env，填入数据库配置和 TUSHARE_TOKEN

# 3. 导入历史数据（一次性，可能需要几小时）
python scripts/import_historical.py

# 4. 配置自动更新
# 在 .env 中设置：
#   ENABLE_AUTO_UPDATE=1
#   AUTO_UPDATE_ON_STARTUP=1

# 5. 启动服务
python main.py

# 6. 验证自动更新
tail -f logs/stock_data_update.log
```

## 🎯 功能特性 / Features

### 自动更新功能 (auto_update.py)

- ✅ **交易日智能判断**：通过 Tushare 交易日历 API 判断是否交易日，休市日自动跳过
- ✅ **增量更新**：从数据库最新日期的下一天开始，避免重复插入
- ✅ **全覆盖**：自动更新所有约 4500+ 只股票
- ✅ **API 限制保护**：每次请求延迟 0.12 秒，避免触发 Tushare 频率限制（500 次/分钟）
- ✅ **详细日志**：所有操作记录在 `logs/stock_data_update.log`
- ✅ **进度显示**：每 100 只股票显示一次进度和预计剩余时间
- ✅ **统计信息**：成功/失败/跳过数量、新增记录数、总耗时等

### 数据导入功能 (import_historical.py)

- ✅ 支持 CSV、Excel 格式
- ✅ 自动处理日期格式
- ✅ 批量插入优化
- ✅ 错误处理和日志记录

## 📊 日志说明 / Logging

### 日志位置

```
logs/stock_data_update.log
```

### 日志内容示例

```
[2024-01-15 20:00:00] INFO: 今天是交易日，开始更新股票数据
[2024-01-15 20:00:00] INFO: 从数据库获取到 4532 只股票
[2024-01-15 20:00:00] INFO: ============================================================
[2024-01-15 20:00:00] INFO: 开始批量更新 4532 只股票的历史行情数据
[2024-01-15 20:02:00] INFO: 进度: 100/4532 (2.2%) | 成功: 95 | 失败: 2 | 跳过: 3 | 预计剩余: 89.5分钟
...
[2024-01-15 21:35:27] INFO: 批量更新完成
[2024-01-15 21:35:27] INFO: 总股票数: 4532
[2024-01-15 21:35:27] INFO: 成功更新: 4510 只
[2024-01-15 21:35:27] INFO: 失败: 15 只
[2024-01-15 21:35:27] INFO: 跳过（无新数据）: 7 只
[2024-01-15 21:35:27] INFO: 新增记录: 4510 条
[2024-01-15 21:35:27] INFO: 总耗时: 95.4 分钟
```

## ⚠️ 注意事项 / Notes

### 生产环境部署

- **多实例部署**：建议将定时调度器作为单独进程运行（systemd、Windows Task Scheduler、CronJob 等），避免多个实例重复执行
- **安全性**：不要在代码中硬编码密码和 Token，使用环境变量或密钥管理工具
- **监控**：定期检查日志文件，确认更新是否正常
- **备份**：定期备份 `stock_daily_data` 表

### API 限制说明

Tushare API 限制（基础积分）：
- 每分钟最多 500 次调用
- 每次最多返回 6000 条数据
- Daily 接口每天 15-16 点入库数据

建议更新时间：**20:00 之后**

### 预期耗时

- **单只股票**：约 0.12-0.15 秒
- **全量更新（4500+ 只）**：约 9-15 分钟（日常增量）
- **首次导入历史数据**：可能需要几小时（取决于数据范围）

## 🔍 故障排查 / Troubleshooting

### Token 无效

```
错误：token 无效
解决：
1. 检查 .env 中的 TUSHARE_TOKEN 是否正确
2. 访问 https://tushare.pro/ 确认 Token 状态
3. 确认 Token 有足够积分
```

### 数据库连接失败

```
错误：无法连接数据库
解决：
1. 检查数据库服务是否启动
2. 验证 .env 中的数据库配置
3. 测试连接：mysql -h localhost -u root -p
```

### API 频率限制

```
错误：抱歉，您每分钟最多访问该接口 500 次
解决：
- 系统已自动添加延迟保护（0.12 秒/次）
- 如仍触发限制，可增大延迟值
```

### 定时任务未执行

```
检查步骤：
1. 确认 ENABLE_AUTO_UPDATE=1
2. 查看启动日志是否有 "自动更新调度已启动"
3. 检查系统时间是否正确
4. 查看日志文件是否有执行记录
```

## 📚 更多文档 / Documentation

详细使用文档请参考：

- [自动更新功能使用文档](../docs/自动更新功能使用文档.md) - 完整的配置、使用、故障排查指南
- [项目完成情况报告](../docs/项目完成情况报告.md) - 项目整体功能说明

## 🔗 相关链接 / Links

- [Tushare Pro 官网](https://tushare.pro/)
- [Tushare Pro API 文档](https://tushare.pro/document/2)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)

---

**最后更新**：2024-01-15  
**版本**：1.0
