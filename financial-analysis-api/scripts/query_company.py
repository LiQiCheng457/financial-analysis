#!/usr/bin/env python3
"""
Standalone helper to query `stock_basic_info` for a given stock code or company name.

Usage:
  cd financial-analysis-api
  python scripts/query_company.py SZ000001

The script uses the same SQLAlchemy SessionLocal defined in `app.core.database`.
"""
import sys
import json
from sqlalchemy import text

try:
    # import SessionLocal from project
    from app.core.database import SessionLocal
except Exception as e:
    print(f"Failed to import SessionLocal from app.core.database: {e}")
    sys.exit(2)


def find_company(q: str):
    db = SessionLocal()
    try:
        # 1) exact match on stock_code
        sql = text(
            """
            SELECT stock_code, company_name, english_name, a_stock_code, security_category,
                   listing_exchange, legal_representative, chairman, website,
                   registered_capital, company_intro, business_scope
            FROM stock_basic_info
            WHERE stock_code = :q
            LIMIT 1
            """
        )
        r = db.execute(sql, {"q": q}).mappings().fetchone()
        if r:
            return dict(r)

        # 2) fuzzy match on company_name / a_stock_code / a_stock_abbr
        likeq = f"%{q}%"
        sql2 = text(
            """
            SELECT stock_code, company_name, english_name, a_stock_code, security_category,
                   listing_exchange, legal_representative, chairman, website,
                   registered_capital, company_intro, business_scope
            FROM stock_basic_info
            WHERE company_name LIKE :likeq OR a_stock_code LIKE :likeq OR a_stock_abbr LIKE :likeq
            LIMIT 1
            """
        )
        r2 = db.execute(sql2, {"likeq": likeq}).mappings().fetchone()
        if r2:
            return dict(r2)

        return None
    finally:
        db.close()


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/query_company.py <stock_code_or_name>")
        sys.exit(1)

    q = sys.argv[1].strip()
    if not q:
        print("empty query")
        sys.exit(1)

    try:
        res = find_company(q)
        if res:
            print(json.dumps({"status": "ok", "data": res}, ensure_ascii=False, indent=2))
            sys.exit(0)
        else:
            print(json.dumps({"status": "not_found", "message": f"暂无 {q} 公司数据"}, ensure_ascii=False, indent=2))
            sys.exit(0)
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        sys.exit(3)


if __name__ == '__main__':
    main()
