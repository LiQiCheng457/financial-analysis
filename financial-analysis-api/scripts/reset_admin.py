#!/usr/bin/env python3
"""
Interactive script to create or reset the admin user password.
Usage:
  python scripts/reset_admin.py

This script uses the application's AuthService so password hashing is consistent.
"""
import getpass
from dotenv import load_dotenv
import os
import sys

load_dotenv()

# bring app context pieces
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from app.core.database import SessionLocal
from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate


def prompt(prompt_text, default=None):
    if default:
        res = input(f"{prompt_text} [{default}]: ")
        return res.strip() or default
    else:
        return input(f"{prompt_text}: ").strip()


def main():
    print("管理员创建/重置脚本")
    username = prompt("输入用户名", "admin")
    db = SessionLocal()
    try:
        user = AuthService.get_user_by_username(db, username=username)
        if user:
            print(f"用户 {username} 已存在。你可以选择重置密码。")
            while True:
                pwd = getpass.getpass("请输入新密码: ")
                pwd2 = getpass.getpass("请再次输入新密码: ")
                if pwd != pwd2:
                    print("两次输入不一致，请重试。")
                    continue
                if len(pwd) < 6:
                    print("密码长度至少 6 位，请重试。")
                    continue
                break
            updated = AuthService.update_user_password(db, username=username, new_password=pwd)
            if updated:
                print(f"用户 {username} 的密码已重置。")
            else:
                print(f"无法重置用户 {username} 的密码（用户不存在或操作失败）。")
        else:
            print(f"用户 {username} 不存在，准备创建。")
            while True:
                pwd = getpass.getpass("请输入密码: ")
                pwd2 = getpass.getpass("请再次输入密码: ")
                if pwd != pwd2:
                    print("两次输入不一致，请重试。")
                    continue
                if len(pwd) < 6:
                    print("密码长度至少 6 位，请重试。")
                    continue
                break
            role = prompt("请输入角色 (admin/user)", "admin")
            new_user = UserCreate(username=username, password=pwd)
            created = AuthService.create_user(db=db, user=new_user)
            # 如果模型支持 role 字段且需要设置为 admin，手动更新
            if created and getattr(created, 'role', None) != role:
                created.role = role
                db.add(created)
                db.commit()
                db.refresh(created)
            print(f"用户 {username} 已创建，角色: {role}")
    except Exception as e:
        print("操作失败:", e)
    finally:
        db.close()


if __name__ == '__main__':
    main()
