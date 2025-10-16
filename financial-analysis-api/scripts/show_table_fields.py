#!/usr/bin/env python3
"""查看stock_basic_info表的所有字段"""
import sys
from sqlalchemy import text
from app.core.database import SessionLocal

def show_fields():
    db = SessionLocal()
    try:
        sql = text("DESCRIBE stock_basic_info")
        result = db.execute(sql).fetchall()
        print("字段名                          类型                   是否为空")
        print("="*70)
        for row in result:
            print(f'{row[0]:30} {row[1]:20} {row[2]:10}')
    finally:
        db.close()

if __name__ == '__main__':
    show_fields()
