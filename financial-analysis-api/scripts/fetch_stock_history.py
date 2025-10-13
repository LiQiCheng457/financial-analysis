"""
脚本：fetch_stock_history.py
用途：独立验证 akshare 的 ak.stock_zh_a_hist 接口并把结果以 JSON 打印到 stdout，便于在本地环境先行验证。
用法示例（PowerShell）：
  conda activate financial-analysis; python .\scripts\fetch_stock_history.py --code 000001 --start 20230101 --end 20231231
  conda activate financial-analysis; python .\scripts\fetch_stock_history.py --code 000001 --adjust qfq
注意：
 - `akshare` 和 `pandas` 需要在当前 Python 环境中已安装（比如通过 `pip install akshare pandas` 或使用项目的 requirements.txt）。
 - 如果不提供 --start/--end，则会让 akshare 使用默认行为。
"""

import argparse
import json
import sys
from typing import Any, Dict, List, Optional

try:
    import akshare as ak
    import pandas as pd
    import numpy as np
except Exception as e:
    print("Missing dependency: please install akshare, pandas, numpy. Error:", e, file=sys.stderr)
    sys.exit(2)


def _safe_value(v: Any) -> Any:
    """Convert numpy/pandas scalar and NaN/inf to JSON-friendly Python types."""
    try:
        if v is None:
            return None
        # pandas NA
        try:
            if pd.isna(v):
                return None
        except Exception:
            pass
        # numpy scalar
        if isinstance(v, (np.integer,)):
            return int(v)
        if isinstance(v, (np.floating,)):
            f = float(v)
            if not np.isfinite(f):
                return None
            return f
        if isinstance(v, (np.bool_)):
            return bool(v)
        # python number/string/bool
        if isinstance(v, (int, float, str, bool)):
            if isinstance(v, float) and not (np.isfinite(v)):
                return None
            return v
        # datetimes -> iso
        if hasattr(v, 'strftime'):
            try:
                return v.strftime('%Y-%m-%d')
            except Exception:
                return str(v)
        # fallback: convert to str
        return str(v)
    except Exception:
        return None


def records_from_df(df: pd.DataFrame, code: str) -> List[Dict[str, Any]]:
    if df is None or df.empty:
        return []
    # normalize date column
    if '日期' in df.columns:
        try:
            df['日期'] = pd.to_datetime(df['日期']).dt.strftime('%Y-%m-%d')
        except Exception:
            df['日期'] = df['日期'].astype(str)
    # ensure 股票代码
    if '股票代码' not in df.columns:
        df['股票代码'] = code
    # convert to records and sanitize
    recs = df.to_dict(orient='records')
    out = []
    for r in recs:
        nr = {}
        for k, v in r.items():
            nr[k] = _safe_value(v)
        out.append(nr)
    return out


def fetch_history(symbol: str, start: Optional[str], end: Optional[str], adjust: Optional[str]) -> List[Dict[str, Any]]:
    # ak.stock_zh_a_hist expects symbol, period, start_date, end_date, adjust
    # adjust: '' (不复权), 'qfq', 'hfq'
    try:
        df = ak.stock_zh_a_hist(symbol=symbol, period='daily', start_date=start, end_date=end, adjust=adjust or "")
    except Exception as e:
        print(f"Error calling ak.stock_zh_a_hist: {e}", file=sys.stderr)
        return []
    # Accept either DataFrame or other structure
    if isinstance(df, pd.DataFrame):
        return records_from_df(df, symbol)
    # if it's a dict/list fallback
    try:
        if isinstance(df, (list, tuple)):
            out = []
            for item in df:
                if isinstance(item, dict):
                    nr = {k: _safe_value(v) for k, v in item.items()}
                    out.append(nr)
                else:
                    out.append({'value': _safe_value(item)})
            return out
    except Exception:
        pass
    return []


def main():
    parser = argparse.ArgumentParser(description='Fetch A-share history via akshare for local verification.')
    parser.add_argument('--code', '--symbol', dest='code', required=True, help='股票代码，例如 000001')
    parser.add_argument('--start', dest='start', required=False, help='开始日期 YYYYMMDD，可选')
    parser.add_argument('--end', dest='end', required=False, help='结束日期 YYYYMMDD，可选')
    parser.add_argument('--adjust', dest='adjust', required=False, default='', help="调整类型: '' 不复权, 'qfq', 'hfq' (可选)")
    args = parser.parse_args()

    recs = fetch_history(symbol=args.code, start=args.start, end=args.end, adjust=args.adjust)
    # print JSON to stdout
    json.dump(recs, sys.stdout, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
