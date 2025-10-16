"""检查stock_basic_info表结构"""
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))

with engine.connect() as conn:
    result = conn.execute(text('DESCRIBE stock_basic_info'))
    print("字段名                          类型                   是否为空")
    print("="*70)
    for row in result:
        print(f'{row[0]:30} {row[1]:20} {row[2]:10}')
