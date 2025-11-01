#!/usr/bin/env python3
"""
Test calling stock_service.get_company_profile directly for a given stock code.
"""
import sys
from pathlib import Path
script_path = Path(__file__).resolve()
backend_root = script_path.parent.parent
if str(backend_root) not in sys.path:
    sys.path.insert(0, str(backend_root))

try:
    from app.core.database import engine
    from app.services import stock_service
except Exception as e:
    print('Import error:', e)
    sys.exit(2)

code = sys.argv[1] if len(sys.argv) > 1 else 'SH600050'
print('Querying company profile for', code)
with engine.connect() as conn:
    prof = stock_service.get_company_profile(conn, code)
    import json
    print(json.dumps(prof, ensure_ascii=False, default=str, indent=2))
