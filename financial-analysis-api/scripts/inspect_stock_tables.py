#!/usr/bin/env python3
"""
简单的数据库检查脚本 — 用于查看 `stock_shareholding_info` 与 `stock_issuer_info` 表的示例数据与字段

用法:
  python inspect_stock_tables.py [--limit N] [--skip-rows]

它会使用项目中 `app.core.database` 中的 engine 配置（读取 .env 环境变量），并打印每张表的列名和前 N 行的内容（以 dict 形式）。
"""
import argparse
import sys
from pathlib import Path
from sqlalchemy import text

# Ensure the backend package root is on sys.path so `import app` works when running
# this script from the workspace root. The script lives in: <repo>/financial-analysis-api/scripts
# so the backend package root is its parent directory.
script_path = Path(__file__).resolve()
backend_root = script_path.parent.parent
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

try:
    # reuse project's DB engine/session
    from app.core.database import engine
except Exception as e:
    print("无法导入项目的数据库配置，请确保已安装依赖并正确设置环境变量 (.env)。错误:", e)
    sys.exit(2)


def inspect_table(conn, table_name: str, limit: int = 10, skip_rows: bool = False):
    print('\n' + '=' * 80)
    print(f"Inspecting table: {table_name}")
    print('-' * 80)
    try:
        # check existence
        exists_sql = text("SELECT 1 FROM information_schema.tables WHERE table_schema = DATABASE() AND table_name = :t LIMIT 1")
        ex = conn.execute(exists_sql, {"t": table_name}).fetchone()
        if not ex:
            print(f"表 '{table_name}' 不存在于当前数据库。")
            return

        # fetch sample rows
        if not skip_rows:
            q = text(f"SELECT * FROM {table_name} LIMIT :lim")
            rows = conn.execute(q, {"lim": limit}).mappings().fetchall()
            if not rows:
                print(f"表 '{table_name}' 为空（没有数据）。")
                return

            # print columns
            cols = list(rows[0].keys())
            print("Columns:")
            print(', '.join(cols))
            print('\nSample rows:')
            for i, r in enumerate(rows, start=1):
                # convert mapping to normal dict for nicer print
                d = dict(r)
                # shorten long values for display
                d_short = {k: (repr(v)[:200] + '...' if v is not None and len(repr(v)) > 200 else v) for k, v in d.items()}
                print(f"{i:02d}: {d_short}")
        else:
            print("跳过行内容，仅检查表存在性。")

    except Exception as e:
        print(f"检查表 '{table_name}' 时出错: {e}")


def main():
    parser = argparse.ArgumentParser(description="Inspect stock shareholding and issuer tables")
    parser.add_argument('--limit', '-n', type=int, default=10, help='每张表显示的行数')
    parser.add_argument('--skip-rows', action='store_true', help='仅检查表是否存在，跳过显示行')
    parser.add_argument('--tables', '-t', nargs='*', help='要检查的表，默认检查 stock_shareholding_info 和 stock_issuer_info')
    args = parser.parse_args()

    tables = args.tables or ['stock_shareholding_info', 'stock_issuer_info']

    with engine.connect() as conn:
        for tbl in tables:
            inspect_table(conn, tbl, limit=args.limit, skip_rows=args.skip_rows)


if __name__ == '__main__':
    main()
