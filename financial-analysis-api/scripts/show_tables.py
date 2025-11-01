"""
查看数据库中的所有表
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from sqlalchemy import text

def show_tables():
    """显示所有表"""
    db = SessionLocal()
    try:
        result = db.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        
        print("=" * 60)
        print("数据库中的所有表:")
        print("=" * 60)
        for table in tables:
            print(f"  - {table}")
        
        if tables:
            print("\n" + "=" * 60)
            print("查看第一个表的结构:")
            print("=" * 60)
            first_table = tables[0]
            result = db.execute(text(f"DESCRIBE {first_table}"))
            for row in result:
                print(f"  {row[0]}: {row[1]}")
        
    finally:
        db.close()

if __name__ == "__main__":
    show_tables()
