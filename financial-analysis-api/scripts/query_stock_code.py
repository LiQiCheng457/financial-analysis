#!/usr/bin/env python3
"""
Quick DB query to check shareholding/issuer rows for a given stock code.
Usage:
  python query_stock_code.py SH600050
"""
import sys
from pathlib import Path
script_path = Path(__file__).resolve()
backend_root = script_path.parent.parent
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

try:
    from app.core.database import engine
except Exception as e:
    print('无法导入 app.core.database.engine:', e)
    sys.exit(2)

code = sys.argv[1] if len(sys.argv) > 1 else 'SH600050'
variants = [code]
if code.upper().startswith(('SH','SZ')):
    variants.append(code[2:])
else:
    if len(code) == 6 and code.isdigit():
        variants.append('SH' + code)
        variants.append('SZ' + code)

print('Querying variants:', variants)
with engine.connect() as conn:
    for tbl in ('stock_shareholding_info','stock_issuer_info'):
        try:
            q = "SELECT COUNT(1) AS cnt FROM {} WHERE stock_code IN :variants".format(tbl)
            cnt = conn.execute(__import__('sqlalchemy').text(q), {'variants': tuple(variants)}).fetchone()
            print(f"\nTable {tbl} - count result: {cnt}")
            if cnt and cnt[0] > 0:
                q2 = "SELECT * FROM {} WHERE stock_code IN :variants LIMIT 20".format(tbl)
                rows = conn.execute(__import__('sqlalchemy').text(q2), {'variants': tuple(variants)}).mappings().fetchall()
                print(f"Showing up to 20 rows from {tbl}:")
                for i,r in enumerate(rows, start=1):
                    d = dict(r)
                    print(f"{i:02d}: {d}")
            else:
                print(f"No rows found in {tbl} for given code variants.")
        except Exception as e:
            print(f"Error querying {tbl}:", e)
