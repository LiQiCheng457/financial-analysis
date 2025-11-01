#!/usr/bin/env python
"""
数据库迁移管理脚本
提供便捷的数据库迁移命令
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd: list[str], description: str):
    """运行命令并处理错误"""
    print(f"\n{'='*60}")
    print(f"📋 {description}")
    print(f"{'='*60}")
    print(f"命令: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    if result.returncode != 0:
        print(f"\n❌ 错误: {description} 失败")
        sys.exit(1)
    print(f"\n✅ {description} 完成")
    return result

def init():
    """初始化数据库迁移（仅首次使用）"""
    print("\n⚠️  警告: 此命令会重新初始化 Alembic")
    print("如果已经存在迁移文件，请不要执行此操作")
    confirm = input("确认继续? (yes/no): ")
    if confirm.lower() != 'yes':
        print("操作已取消")
        return
    
    run_command(
        ["alembic", "init", "alembic"],
        "初始化 Alembic"
    )

def create(message: str = None):
    """创建新的迁移文件"""
    if not message:
        message = input("请输入迁移描述: ")
    
    run_command(
        ["alembic", "revision", "--autogenerate", "-m", message],
        f"创建迁移: {message}"
    )

def upgrade(revision: str = "head"):
    """升级数据库到指定版本"""
    run_command(
        ["alembic", "upgrade", revision],
        f"升级数据库到 {revision}"
    )

def downgrade(revision: str = "-1"):
    """降级数据库到指定版本"""
    print("\n⚠️  警告: 此操作会回滚数据库更改")
    confirm = input(f"确认降级到版本 {revision}? (yes/no): ")
    if confirm.lower() != 'yes':
        print("操作已取消")
        return
    
    run_command(
        ["alembic", "downgrade", revision],
        f"降级数据库到 {revision}"
    )

def history():
    """查看迁移历史"""
    run_command(
        ["alembic", "history", "--verbose"],
        "查看迁移历史"
    )

def current():
    """查看当前数据库版本"""
    run_command(
        ["alembic", "current"],
        "查看当前数据库版本"
    )

def stamp(revision: str = "head"):
    """标记数据库版本（不执行迁移）"""
    print("\n⚠️  警告: 此操作会标记数据库版本但不会执行迁移SQL")
    print("通常用于已存在的数据库或手动迁移后")
    confirm = input(f"确认标记版本为 {revision}? (yes/no): ")
    if confirm.lower() != 'yes':
        print("操作已取消")
        return
    
    run_command(
        ["alembic", "stamp", revision],
        f"标记数据库版本为 {revision}"
    )

def show_help():
    """显示帮助信息"""
    help_text = """
╔════════════════════════════════════════════════════════════════╗
║              数据库迁移管理工具 - 使用指南                      ║
╚════════════════════════════════════════════════════════════════╝

📚 命令列表:

  python migrate.py create [描述]
      创建新的迁移文件（自动检测模型变化）
      示例: python migrate.py create "添加用户表"

  python migrate.py upgrade [版本]
      升级数据库到指定版本（默认: head 最新版本）
      示例: python migrate.py upgrade
      示例: python migrate.py upgrade 4f3b2c1a9d3e

  python migrate.py downgrade [版本]
      降级数据库到指定版本（默认: -1 上一个版本）
      示例: python migrate.py downgrade
      示例: python migrate.py downgrade base

  python migrate.py history
      查看所有迁移历史记录

  python migrate.py current
      查看当前数据库版本

  python migrate.py stamp [版本]
      标记数据库版本（不执行迁移，用于已存在的数据库）
      示例: python migrate.py stamp head

  python migrate.py help
      显示此帮助信息

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📖 常用场景:

  1️⃣  首次部署（新数据库）:
      python migrate.py upgrade

  2️⃣  修改了模型后创建迁移:
      python migrate.py create "描述修改内容"
      python migrate.py upgrade

  3️⃣  已有数据库，首次使用迁移系统:
      python migrate.py stamp head

  4️⃣  回滚到上一个版本:
      python migrate.py downgrade

  5️⃣  查看迁移状态:
      python migrate.py current
      python migrate.py history

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️  配置说明:
  - 数据库连接从 .env 文件读取
  - 迁移文件保存在 alembic/versions/ 目录
  - 自动检测 app/models/ 下的所有模型

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    print(help_text)

def main():
    """主函数"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    try:
        if command == "create":
            message = sys.argv[2] if len(sys.argv) > 2 else None
            create(message)
        
        elif command == "upgrade":
            revision = sys.argv[2] if len(sys.argv) > 2 else "head"
            upgrade(revision)
        
        elif command == "downgrade":
            revision = sys.argv[2] if len(sys.argv) > 2 else "-1"
            downgrade(revision)
        
        elif command == "history":
            history()
        
        elif command == "current":
            current()
        
        elif command == "stamp":
            revision = sys.argv[2] if len(sys.argv) > 2 else "head"
            stamp(revision)
        
        elif command == "help":
            show_help()
        
        else:
            print(f"\n❌ 未知命令: {command}")
            print("运行 'python migrate.py help' 查看帮助\n")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  操作已取消")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
