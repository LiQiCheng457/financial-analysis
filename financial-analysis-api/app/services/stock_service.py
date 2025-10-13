"""股票数据服务（稳健版）

特性：
- 封装 akshare 的调用，若环境中未安装 akshare 则降级返回空结构，避免抛出 ImportError。
- 提供：get_trade_dates(), get_sse_daily_summary(date_str), get_stock_history_data(...)
- 输出为 JSON-safe（将 numpy/pandas 类型与 NaN/inf 转为 None 或原生 Python 类型）。
"""

try:
    import akshare as ak
except Exception:
    ak = None

import pandas as pd
import numpy as np
import math
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta


def _safe_number(x: Any) -> Any:
    try:
        if x is None:
            return None
        if isinstance(x, (np.integer,)):
            return int(x)
        if isinstance(x, (np.floating,)):
            if np.isnan(x) or np.isinf(x):
                return None
            return float(x)
        if pd.isna(x):
            return None
        return x
    except Exception:
        return None


def _clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    if df is None:
        return pd.DataFrame()
    if isinstance(df, pd.Series):
        df = df.to_frame().T
    df2 = df.copy()
    for col in df2.columns:
        df2[col] = df2[col].apply(_safe_number)
    # format datetime-like columns
    for col in df2.select_dtypes(include=['datetime64[ns]']).columns:
        df2[col] = df2[col].dt.strftime('%Y-%m-%d')
    return df2


def _to_json_safe(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out = []
    for r in records:
        nr = {}
        for k, v in r.items():
            # normalize numpy / pandas scalar types and NaN/inf
            if v is None:
                nr[k] = None
            elif isinstance(v, (np.integer,)):
                nr[k] = int(v)
            elif isinstance(v, (np.floating, float)):
                if np.isnan(v) or np.isinf(v):
                    nr[k] = None
                else:
                    nr[k] = float(v)
            elif isinstance(v, (int, str, bool)):
                nr[k] = v
            else:
                # fallback: stringify complex objects
                try:
                    nr[k] = str(v)
                except Exception:
                    nr[k] = None
        out.append(nr)
    return out


_trade_dates_cache: Optional[List[str]] = None


def _load_trade_dates() -> List[str]:
    global _trade_dates_cache
    if _trade_dates_cache is not None:
        return _trade_dates_cache
    try:
        if ak is None:
            _trade_dates_cache = []
            return _trade_dates_cache
        df = ak.tool_trade_date_hist_sina()
        if df is None or df.empty:
            _trade_dates_cache = []
            return _trade_dates_cache
        if 'trade_date' in df.columns:
            df['trade_date'] = pd.to_datetime(df['trade_date']).dt.strftime('%Y%m%d')
            _trade_dates_cache = df['trade_date'].tolist()
        else:
            col = df.columns[0]
            df[col] = pd.to_datetime(df[col]).dt.strftime('%Y%m%d')
            _trade_dates_cache = df[col].tolist()
        return _trade_dates_cache
    except Exception as e:
        print(f"Error loading trade dates: {e}")
        _trade_dates_cache = []
        return _trade_dates_cache


def get_trade_dates() -> List[str]:
    return _load_trade_dates()


def _is_future_date(d: str) -> bool:
    try:
        return int(d) > int(datetime.now().strftime('%Y%m%d'))
    except Exception:
        return False


def get_trade_dates_with_status() -> List[Dict[str, Any]]:
    """返回带状态的交易日列表：[{date: 'YYYYMMDD', status: 'open'|'holiday'|'future'}]

    注意：status 'open' 表示该日为交易日（理论上有数据），'holiday' 表示非交易日，'future' 表示日期在今天之后。
    """
    dates = _load_trade_dates()
    out: List[Dict[str, Any]] = []
    if not dates:
        return out

    # build a contiguous calendar between min and max available trade date
    try:
        min_d = min(dates)
        max_d = max(dates)
        start_dt = datetime.strptime(min_d, '%Y%m%d')
        end_dt = datetime.strptime(max_d, '%Y%m%d')
    except Exception:
        # fallback: just mark known trade dates
        today = datetime.now().strftime('%Y%m%d')
        for d in dates:
            st = 'open' if d <= today else 'future'
            out.append({'date': d, 'status': st})
        return out

    date_set = set(dates)
    today_dt = datetime.now()
    cur = start_dt
    while cur <= end_dt:
        ds = cur.strftime('%Y%m%d')
        if cur.date() > today_dt.date():
            st = 'future'
        else:
            st = 'open' if ds in date_set else 'holiday'
        out.append({'date': ds, 'status': st})
        cur = cur + timedelta(days=1)

    return out


def get_last_open_date(before: Optional[str] = None) -> Optional[str]:
    """返回最后一个已开市的交易日。若提供 before（YYYYMMDD），则返回 strictly < before 的最后开市日；
    否则返回严格 < today 的最后开市日。如果没有找到则返回 None。
    """
    dates = _load_trade_dates()
    if not dates:
        return None
    pivot = before or datetime.now().strftime('%Y%m%d')
    for d in reversed(dates):
        try:
            if d < pivot:
                return d
        except Exception:
            continue
    return None


def get_sse_daily_summary(date_str: Optional[str] = None) -> Dict[str, Any]:
    """返回上海证券交易所每日概况。

    如果未传入 date_str，则使用交易日历选择最近一次不晚于今天的交易日作为默认查询日期。
    返回结构：{date: str, data: List[Dict], holiday: bool, message: str}
    """
    result: Dict[str, Any] = {"date": date_str or "", "data": [], "holiday": False, "message": ""}

    trade_dates = _load_trade_dates()
    if not trade_dates:
        result['message'] = '无法获取交易日历'
        return result

    # choose default date if none provided: the last open trade date STRICTLY before today
    if not date_str:
        last_open = get_last_open_date()
        if last_open:
            date_str = last_open
            result['date'] = date_str
        else:
            # fallback to latest available
            date_str = trade_dates[-1]
            result['date'] = date_str

    # annotate last_open_date in result for caller convenience
    result['last_open_date'] = get_last_open_date(before=date_str if date_str else None)

    # detect future date
    if _is_future_date(date_str):
        result['message'] = f"{date_str} 为未来日期，尚未开市"
        result['holiday'] = False
        result['status'] = 'future'
        return result

    # if the requested date is not a trade date, mark as holiday and return message
    if date_str not in trade_dates:
        result['holiday'] = True
        result['message'] = f"{date_str} 为休市日"
        result['status'] = 'holiday'
        return result

    # if the requested date is today, do not return data (trading not ended)
    today = datetime.now().strftime('%Y%m%d')
    if date_str == today:
        result['message'] = '今日开市尚未结束，数据未最终确认，请查询上一个已开市日或稍后重试'
        result['status'] = 'today_incomplete'
        result['holiday'] = False
        return result

    # fetch data via akshare if available
    try:
        if ak is None:
            result['message'] = 'akshare 未安装，无法查询'
            return result

        raw = ak.stock_sse_deal_daily(date=date_str)
        if raw is None:
            result['message'] = '查询到空数据，可能交易所尚未统计完成'
            return result

        # coerce to DataFrame if needed and clean
        df = _clean_dataframe(raw if isinstance(raw, (pd.DataFrame, pd.Series)) else pd.DataFrame(raw))
        if df.empty:
            result['message'] = '查询到空数据'
            return result

        # replace any remaining NaN/inf and convert to records
        records = df.to_dict(orient='records')
        result['data'] = _to_json_safe(records)
        result['message'] = '成功'
        result['status'] = 'ok'
        return result
    except Exception as e:
        result['message'] = f'请求数据失败: {e}'
        return result


def _standardize_history_columns(df: pd.DataFrame, code: str) -> pd.DataFrame:
    """简化版列名标准化，输出主要列名为中文，以匹配前端表格字段。"""
    if df is None or df.empty:
        return pd.DataFrame()

    col_map = {}
    for c in df.columns:
        cl = str(c).lower()
        if 'date' in cl or '交易' in cl or '日期' in cl:
            col_map[c] = '日期'
        elif cl in ('open',) or '开盘' in cl:
            col_map[c] = '开盘'
        elif cl in ('close',) or '收盘' in cl:
            col_map[c] = '收盘'
        elif cl in ('high',) or '最高' in cl:
            col_map[c] = '最高'
        elif cl in ('low',) or '最低' in cl:
            col_map[c] = '最低'
        elif 'volume' in cl or '成交量' in cl or cl == 'vol':
            col_map[c] = '成交量'
        elif cl == 'amount' or '成交额' in cl:
            col_map[c] = '成交额'
        elif 'turnover' in cl or '换手率' in cl:
            col_map[c] = '换手率'
        elif 'amplitude' in cl or '振幅' in cl:
            col_map[c] = '振幅'
        elif 'pct' in cl or '涨跌幅' in cl or 'pct_chg' in cl:
            col_map[c] = '涨跌幅'
        elif cl in ('change',) or '涨跌额' in cl:
            col_map[c] = '涨跌额'

    try:
        df = df.rename(columns=col_map)
    except Exception:
        pass

    # 格式化 日期 列
    if '日期' in df.columns:
        try:
            df['日期'] = pd.to_datetime(df['日期']).dt.strftime('%Y-%m-%d')
        except Exception:
            df['日期'] = df['日期'].astype(str)

    if '股票代码' not in df.columns:
        df['股票代码'] = code

    return df


def get_stock_history_data(code: str, start_date: Optional[str] = None, end_date: Optional[str] = None, adjust: str = "", source: str = 'eastmoney') -> List[Dict[str, Any]]:
    """从多个来源获取 A 股历史日线并返回 JSON-safe 的记录列表。

    参数:
    - code: 股票代码(如 '000001' 或 'sh600000')
    - start_date,end_date: YYYYMMDD 格式，可选
    - adjust: '' | 'qfq' | 'hfq'
    - source: 'eastmoney' | 'sina' | 'tencent'（默认 eastmoney）
    """
    try:
        if not code:
            return []

        code_str = str(code)

        # 构造不同源可能需要的符号
        def to_exchange_prefixed(sym: str) -> str:
            s = sym.lower()
            if s.startswith('sh') or s.startswith('sz'):
                return s
            if s.startswith('6'):
                return 'sh' + s
            return 'sz' + s

        sina_symbol = to_exchange_prefixed(code_str)
        tencent_symbol = sina_symbol
        east_symbol = code_str[-6:] if len(code_str) >= 6 else code_str

        if ak is None:
            return []

        df = None
        if source == 'sina':
            if hasattr(ak, 'stock_zh_a_daily'):
                df = ak.stock_zh_a_daily(symbol=sina_symbol, start_date=start_date, end_date=end_date, adjust=adjust)
        elif source == 'tencent':
            if hasattr(ak, 'stock_zh_a_hist_tx'):
                df = ak.stock_zh_a_hist_tx(symbol=tencent_symbol, start_date=start_date, end_date=end_date, adjust=adjust)
        else:
            # eastmoney
            if hasattr(ak, 'stock_zh_a_hist'):
                df = ak.stock_zh_a_hist(symbol=east_symbol, period='daily', start_date=start_date, end_date=end_date, adjust=adjust)

        if df is None or (isinstance(df, pd.DataFrame) and df.empty):
            return []

        # 标准化列并清洗
        if isinstance(df, pd.DataFrame):
            df2 = _standardize_history_columns(df, code_str)
        else:
            try:
                df2 = pd.DataFrame(df)
                df2 = _standardize_history_columns(df2, code_str)
            except Exception:
                return []

        cleaned = _clean_dataframe(df2)
        records = cleaned.to_dict(orient='records')
        return _to_json_safe(records)
    except Exception as e:
        print(f"Error in get_stock_history_data: {e}")
        return []
