#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
用户表字段迁移脚本
添加 nickname, phone, email, signature, created_at 字段
"""
import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库连接信息
DB_CONFIG = {
    'host': os.getenv('DATABASE_HOST', 'localhost'),
    'user': os.getenv('DATABASE_USER', 'root'),
    'password': os.getenv('DATABASE_PASSWORD', ''),
    'database': os.getenv('DATABASE_NAME', 'financial_analysis_db'),
    'charset': 'utf8mb4'
}

# SQL语句列表
SQL_STATEMENTS = [
    "ALTER TABLE users ADD COLUMN nickname VARCHAR(100) DEFAULT NULL COMMENT '昵称'",
    "ALTER TABLE users ADD COLUMN phone VARCHAR(20) DEFAULT NULL COMMENT '手机号'",
    "ALTER TABLE users ADD COLUMN email VARCHAR(100) DEFAULT NULL COMMENT '邮箱'",
    "ALTER TABLE users ADD COLUMN signature VARCHAR(200) DEFAULT NULL COMMENT '个性签名'",
    "ALTER TABLE users ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间'",
]

def main():
    try:
        print("连接数据库...")
        conn = pymysql.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("开始执行迁移...")
        for sql in SQL_STATEMENTS:
            try:
                print(f"执行: {sql}")
                cursor.execute(sql)
                print("✓ 成功")
            except pymysql.err.OperationalError as e:
                if "Duplicate column name" in str(e):
                    print(f"⚠ 字段已存在，跳过")
                else:
                    raise
        
        conn.commit()
        print("\n✅ 数据库迁移完成！")
        
        # 验证结果
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        print("\n当前users表结构:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
