"""
数据库迁移示例：添加股票收藏功能

这个示例演示如何：
1. 创建新的模型
2. 生成迁移文件
3. 应用迁移
"""

# ============================================
# 步骤 1: 创建新模型
# ============================================
# 文件: app/models/stock_favorite.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from datetime import datetime
from app.core.database import Base

class StockFavorite(Base):
    """股票收藏表"""
    __tablename__ = "stock_favorites"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True, comment="收藏ID")
    
    # 用户关联
    user_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="用户ID"
    )
    
    # 股票信息
    stock_code = Column(String(20), nullable=False, comment="股票代码")
    stock_name = Column(String(100), nullable=False, comment="股票名称")
    
    # 分组标签
    group_name = Column(String(50), nullable=True, comment="分组名称")
    tags = Column(String(200), nullable=True, comment="标签（逗号分隔）")
    
    # 备注
    note = Column(String(500), nullable=True, comment="备注")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.now, comment="添加时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 复合索引
    __table_args__ = (
        Index('idx_user_stock', 'user_id', 'stock_code', unique=True),  # 防止重复收藏
        Index('idx_user_group', 'user_id', 'group_name'),  # 按分组查询
        {'comment': '股票收藏表'}
    )


# ============================================
# 步骤 2: 在 env.py 中导入模型
# ============================================
# 文件: alembic/env.py
# 在导入部分添加：

"""
from app.models.user import User
from app.models.stock_favorite import StockFavorite  # 添加这行
"""


# ============================================
# 步骤 3: 创建迁移
# ============================================
# 在终端执行：

"""
cd financial-analysis-api
python migrate.py create "添加股票收藏表"
"""

# 这会生成类似的迁移文件：
# alembic/versions/xxxxx_add_stock_favorites.py


# ============================================
# 步骤 4: 检查生成的迁移文件
# ============================================
# 生成的迁移文件示例：

"""
\"""添加股票收藏表

Revision ID: abc123def456
Revises: 4f3b2c1a9d3e
Create Date: 2025-11-01 10:00:00.000000
\"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'abc123def456'
down_revision = '4f3b2c1a9d3e'
branch_labels = None
depends_on = None


def upgrade():
    # 创建股票收藏表
    op.create_table(
        'stock_favorites',
        sa.Column('id', sa.Integer(), nullable=False, comment='收藏ID'),
        sa.Column('user_id', sa.Integer(), nullable=False, comment='用户ID'),
        sa.Column('stock_code', sa.String(length=20), nullable=False, comment='股票代码'),
        sa.Column('stock_name', sa.String(length=100), nullable=False, comment='股票名称'),
        sa.Column('group_name', sa.String(length=50), nullable=True, comment='分组名称'),
        sa.Column('tags', sa.String(length=200), nullable=True, comment='标签'),
        sa.Column('note', sa.String(length=500), nullable=True, comment='备注'),
        sa.Column('created_at', sa.DateTime(), nullable=True, comment='添加时间'),
        sa.Column('updated_at', sa.DateTime(), nullable=True, comment='更新时间'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        comment='股票收藏表'
    )
    
    # 创建索引
    op.create_index('idx_user_stock', 'stock_favorites', ['user_id', 'stock_code'], unique=True)
    op.create_index('idx_user_group', 'stock_favorites', ['user_id', 'group_name'])
    op.create_index(op.f('ix_stock_favorites_id'), 'stock_favorites', ['id'])


def downgrade():
    # 删除索引
    op.drop_index(op.f('ix_stock_favorites_id'), table_name='stock_favorites')
    op.drop_index('idx_user_group', table_name='stock_favorites')
    op.drop_index('idx_user_stock', table_name='stock_favorites')
    
    # 删除表
    op.drop_table('stock_favorites')
"""


# ============================================
# 步骤 5: 应用迁移
# ============================================
# 在终端执行：

"""
python migrate.py upgrade
"""

# 输出示例：
"""
============================================================
📋 升级数据库到 head
============================================================
命令: alembic upgrade head

INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 4f3b2c1a9d3e -> abc123def456, 添加股票收藏表

✅ 升级数据库到 head 完成
"""


# ============================================
# 步骤 6: 验证迁移
# ============================================
# 查看当前版本：

"""
python migrate.py current
"""

# 输出：
"""
INFO  [alembic.runtime.migration] Context impl MySQLImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
abc123def456 (head)
"""


# ============================================
# 步骤 7: 创建对应的 API
# ============================================
# 文件: app/api/stock_favorite.py

"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.stock_favorite import StockFavorite
from app.models.user import User

router = APIRouter(prefix="/favorites", tags=["股票收藏"])

@router.post("/")
def add_favorite(
    stock_code: str,
    stock_name: str,
    group_name: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    \"""添加股票到收藏\"""
    # 检查是否已收藏
    existing = db.query(StockFavorite).filter(
        StockFavorite.user_id == current_user.id,
        StockFavorite.stock_code == stock_code
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="该股票已在收藏中")
    
    # 创建收藏
    favorite = StockFavorite(
        user_id=current_user.id,
        stock_code=stock_code,
        stock_name=stock_name,
        group_name=group_name
    )
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    
    return {"message": "添加成功", "data": favorite}

@router.get("/")
def list_favorites(
    group_name: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    \"""获取收藏列表\"""
    query = db.query(StockFavorite).filter(
        StockFavorite.user_id == current_user.id
    )
    
    if group_name:
        query = query.filter(StockFavorite.group_name == group_name)
    
    favorites = query.order_by(StockFavorite.created_at.desc()).all()
    return {"data": favorites}

@router.delete("/{favorite_id}")
def remove_favorite(
    favorite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    \"""删除收藏\"""
    favorite = db.query(StockFavorite).filter(
        StockFavorite.id == favorite_id,
        StockFavorite.user_id == current_user.id
    ).first()
    
    if not favorite:
        raise HTTPException(status_code=404, detail="收藏不存在")
    
    db.delete(favorite)
    db.commit()
    
    return {"message": "删除成功"}
"""


# ============================================
# 总结：完整流程
# ============================================

"""
1. 创建模型文件
   └─> app/models/stock_favorite.py

2. 在 env.py 导入模型
   └─> alembic/env.py

3. 生成迁移
   └─> python migrate.py create "添加股票收藏表"

4. 检查迁移文件
   └─> alembic/versions/xxxxx_add_stock_favorites.py

5. 应用迁移
   └─> python migrate.py upgrade

6. 验证
   └─> python migrate.py current

7. 创建 API
   └─> app/api/stock_favorite.py

8. 测试
   └─> 启动服务并测试 API
"""


# ============================================
# 回滚示例（如果需要）
# ============================================

"""
# 回滚到上一个版本
python migrate.py downgrade

# 或回滚到指定版本
python migrate.py downgrade 4f3b2c1a9d3e

# 这会删除 stock_favorites 表
"""


# ============================================
# 数据迁移示例（高级）
# ============================================

"""
如果需要在迁移中处理数据，可以编辑迁移文件：

def upgrade():
    # 1. 创建表
    op.create_table(...)
    
    # 2. 迁移数据（如果需要）
    from sqlalchemy.sql import table, column
    from sqlalchemy import String, Integer
    
    # 定义临时表结构
    old_favorites = table('old_favorites',
        column('id', Integer),
        column('user_id', Integer),
        column('stock_code', String),
    )
    
    new_favorites = table('stock_favorites',
        column('id', Integer),
        column('user_id', Integer),
        column('stock_code', String),
        column('stock_name', String),
    )
    
    # 执行数据迁移
    connection = op.get_bind()
    
    # 查询旧数据
    old_data = connection.execute(
        select([old_favorites.c.id, old_favorites.c.user_id, old_favorites.c.stock_code])
    ).fetchall()
    
    # 插入新表
    for row in old_data:
        connection.execute(
            new_favorites.insert().values(
                id=row.id,
                user_id=row.user_id,
                stock_code=row.stock_code,
                stock_name='待补充'  # 默认值
            )
        )
"""
