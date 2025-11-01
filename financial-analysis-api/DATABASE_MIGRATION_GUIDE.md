# 数据库迁移指南

## 📋 概述

本项目使用 **Alembic** 进行数据库版本控制和迁移管理。已经配置好完整的迁移系统，可以方便地进行数据库的升级、降级和版本管理。

## 🚀 快速开始

### 1️⃣ 首次部署（新数据库）

如果是全新的数据库，直接运行升级命令即可：

```bash
# 进入 API 目录
cd financial-analysis-api

# 升级数据库到最新版本
python migrate.py upgrade
```

这会自动创建所有表结构。

### 2️⃣ 已有数据库（首次使用迁移系统）

如果数据库已经存在（通过 `Base.metadata.create_all()` 创建），需要先标记当前版本：

```bash
# 标记数据库为最新版本（不执行迁移）
python migrate.py stamp head
```

### 3️⃣ 修改模型后创建迁移

当你修改了 `app/models/` 下的任何模型后：

```bash
# 1. 自动生成迁移文件
python migrate.py create "描述你的修改"

# 2. 应用迁移
python migrate.py upgrade
```

示例：
```bash
python migrate.py create "添加用户头像字段"
python migrate.py upgrade
```

## 📚 完整命令列表

### 创建迁移
```bash
# 自动检测模型变化并创建迁移文件
python migrate.py create "迁移描述"

# 示例
python migrate.py create "添加股票收藏表"
python migrate.py create "修改用户表字段"
```

### 升级数据库
```bash
# 升级到最新版本
python migrate.py upgrade

# 升级到指定版本
python migrate.py upgrade 4f3b2c1a9d3e
```

### 降级数据库
```bash
# 降级到上一个版本
python migrate.py downgrade

# 降级到指定版本
python migrate.py downgrade 4f3b2c1a9d3e

# 降级到初始状态
python migrate.py downgrade base
```

### 查看状态
```bash
# 查看当前数据库版本
python migrate.py current

# 查看所有迁移历史
python migrate.py history
```

### 标记版本
```bash
# 标记当前数据库为最新版本（不执行SQL）
python migrate.py stamp head

# 标记为指定版本
python migrate.py stamp 4f3b2c1a9d3e
```

### 帮助信息
```bash
# 显示帮助信息
python migrate.py help
```

## 🎯 常用场景

### 场景1：添加新表

1. 在 `app/models/` 创建新的模型文件，例如 `stock_favorite.py`：
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base

class StockFavorite(Base):
    __tablename__ = "stock_favorites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    stock_code = Column(String(20), nullable=False)
    stock_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
```

2. 在 `alembic/env.py` 中导入新模型：
```python
from app.models.user import User
from app.models.stock_favorite import StockFavorite  # 添加这行
```

3. 创建并应用迁移：
```bash
python migrate.py create "添加股票收藏表"
python migrate.py upgrade
```

### 场景2：修改现有表字段

1. 修改模型文件，例如在 `User` 模型添加字段：
```python
class User(Base):
    # ... 其他字段
    bio = Column(Text, nullable=True)  # 新增个人简介字段
```

2. 创建并应用迁移：
```bash
python migrate.py create "用户表添加个人简介字段"
python migrate.py upgrade
```

### 场景3：数据库迁移到新服务器

1. 在新服务器上配置 `.env` 文件

2. 部署代码

3. 运行迁移：
```bash
python migrate.py upgrade
```

### 场景4：回滚错误的迁移

```bash
# 回滚到上一个版本
python migrate.py downgrade

# 或回滚到指定版本
python migrate.py history  # 查看历史，找到目标版本号
python migrate.py downgrade 4f3b2c1a9d3e
```

### 场景5：团队协作时更新数据库

当其他开发者提交了新的迁移文件：

```bash
# 1. 拉取最新代码
git pull

# 2. 应用新的迁移
python migrate.py upgrade
```

## ⚙️ 配置说明

### 环境变量（.env）

数据库连接信息从 `.env` 文件读取：

```bash
DATABASE_USER=root
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=financial_analysis_db
```

### 迁移文件位置

- 迁移脚本：`alembic/versions/`
- 配置文件：`alembic.ini`
- 环境配置：`alembic/env.py`

### 模型文件

所有模型必须：
1. 继承 `Base`
2. 定义 `__tablename__`
3. 在 `alembic/env.py` 中导入

## 🔧 高级用法

### 直接使用 Alembic 命令

如果需要更精细的控制，可以直接使用 Alembic：

```bash
# 创建空白迁移文件（手动编写）
alembic revision -m "描述"

# 查看当前版本
alembic current

# 查看迁移历史（详细）
alembic history --verbose

# 升级时显示 SQL（不执行）
alembic upgrade head --sql

# 降级时显示 SQL（不执行）
alembic downgrade -1 --sql
```

### 生成 SQL 脚本（用于审核）

```bash
# 生成升级 SQL
alembic upgrade head --sql > upgrade.sql

# 生成降级 SQL
alembic downgrade -1 --sql > downgrade.sql
```

## ⚠️ 注意事项

### 1. 备份数据
在执行降级操作前，务必备份数据库：
```bash
mysqldump -u root -p financial_analysis_db > backup.sql
```

### 2. 生产环境迁移
生产环境建议先在测试环境验证：
```bash
# 测试环境
python migrate.py upgrade

# 确认无误后，再在生产环境执行
python migrate.py upgrade
```

### 3. 迁移文件版本控制
- ✅ 将迁移文件提交到 Git
- ✅ 团队成员保持迁移顺序一致
- ❌ 不要删除已应用的迁移文件

### 4. 冲突解决
如果多人同时创建迁移导致冲突：
```bash
# 查看分支
python migrate.py history

# 手动合并或重新创建迁移
alembic merge -m "合并迁移分支" <revision1> <revision2>
```

### 5. 数据迁移
如果需要在迁移中操作数据，编辑生成的迁移文件：

```python
def upgrade():
    # 结构变更
    op.add_column('users', sa.Column('status', sa.String(20)))
    
    # 数据迁移
    connection = op.get_bind()
    connection.execute(
        text("UPDATE users SET status = 'active' WHERE status IS NULL")
    )

def downgrade():
    op.drop_column('users', 'status')
```

## 🐛 常见问题

### Q1: `ModuleNotFoundError: No module named 'app'`
**解决**：确保在项目根目录运行命令，或检查 Python 路径。

### Q2: 数据库版本不一致
**解决**：
```bash
# 查看当前版本
python migrate.py current

# 标记为正确版本
python migrate.py stamp <correct_revision>
```

### Q3: 迁移文件生成为空
**解决**：
1. 检查模型是否在 `alembic/env.py` 中导入
2. 确认模型继承了 `Base`
3. 检查数据库是否已经是最新状态

### Q4: 无法连接数据库
**解决**：
1. 检查 `.env` 配置
2. 确认数据库服务已启动
3. 验证用户权限

## 📖 参考资源

- [Alembic 官方文档](https://alembic.sqlalchemy.org/)
- [SQLAlchemy 文档](https://www.sqlalchemy.org/)
- [MySQL 数据类型](https://dev.mysql.com/doc/refman/8.0/en/data-types.html)

## 🎯 最佳实践

1. **描述性命名**：迁移描述要清晰明确
   ```bash
   ✅ python migrate.py create "用户表添加邮箱验证字段"
   ❌ python migrate.py create "update"
   ```

2. **小步迭代**：一次迁移只做一件事
   ```bash
   ✅ 分别创建：添加字段、修改索引、数据迁移
   ❌ 一次性完成所有修改
   ```

3. **测试验证**：每次迁移后验证功能
   ```bash
   python migrate.py upgrade
   python main.py  # 启动服务测试
   ```

4. **版本管理**：保持迁移历史清晰
   ```bash
   # 定期查看迁移历史
   python migrate.py history
   ```

5. **文档记录**：重要迁移添加注释
   ```python
   """添加用户角色表
   
   - 创建 roles 表
   - 添加用户角色关联
   - 迁移现有用户数据
   
   Revision ID: abc123
   """
   ```

---

**最后更新**: 2025-11-01  
**适用版本**: Alembic 1.x + SQLAlchemy 2.x
