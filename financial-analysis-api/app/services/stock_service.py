"""股票数据服务（稳健版）

特性：
- 封装 akshare 的调用，若环境中未安装 akshare 则降级返回空结构，避免抛出 ImportError。
- 提供：get_trade_dates(), get_sse_daily_summary(date_str), get_stock_history_data(...), get_stock_realtime_info(...)
- 输出为 JSON-safe（将 numpy/pandas 类型与 NaN/inf 转为 None 或原生 Python 类型）。
"""

try:
    import akshare as ak
except Exception:
    ak = None

# ensure Optional is available for the module-level annotation
from typing import Optional

# When get_stock_history_data encounters an exception while fetching remote data,
# store the last error message here so API handlers can return a more informative
# response instead of silently returning an empty list.
last_stock_history_error: Optional[str] = None

# Simple in-memory cache for historical data to reduce latency on repeated queries.
# Keyed by (code,start_date,end_date,adjust,source). Values are tuples (ts, records).
# use built-in dict here so annotation doesn't depend on typing imports order
_history_cache: dict = {}
# cache TTL in seconds (default 1 hour)
CACHE_TTL_SECS = 60 * 60
# maximum number of cached entries to keep
CACHE_MAX_ENTRIES = 1000

# fetch retry configuration
# reduce default attempts to avoid excessive warnings; can be tuned
MAX_FETCH_ATTEMPTS = 2
BACKOFF_SECONDS = [0.5, 1.0]

# module logger
import logging
logger = logging.getLogger(__name__)

import pandas as pd
import numpy as np
import math
import traceback
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy import text
import decimal
from app.core.database import engine


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
        # handle percentage strings like '1.23%' or '-0.56%'
        if isinstance(x, str):
            s = x.strip()
            if s == '' or s == '--' or s.lower() == 'nan':
                return None
            # remove thousands separators
            s2 = s.replace(',', '')
            # parentheses for negative numbers: (1.23) -> -1.23
            if s2.startswith('(') and s2.endswith(')'):
                s2 = '-' + s2[1:-1]
            try:
                if s2.endswith('%'):
                    return float(s2.rstrip('%'))
                # try plain float conversion
                return float(s2)
            except Exception:
                # fall through to return original string if not numeric
                pass
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


def get_stock_realtime_info(code: str) -> Dict[str, Any]:
    """获取单个股票的实时行情信息
    
    参数:
    - code: 股票代码（6位数字，如 '000001', '600000'）
    
    返回:
    {
        'status': 'ok' | 'error',
        'message': str,
        'data': { ... } 或 None
    }
    """
    result = {
        'status': 'error',
        'message': '',
        'data': None
    }
    
    try:
        if not code:
            result['message'] = '股票代码不能为空'
            return result
            
        if ak is None:
            result['message'] = 'akshare 未安装，无法查询'
            return result
        
        # 确保股票代码是6位数字
        code_clean = str(code).strip()
        if len(code_clean) < 6:
            code_clean = code_clean.zfill(6)
        
        # 使用 stock_individual_info_em 接口获取单股票实时信息
        df = ak.stock_individual_info_em(symbol=code_clean)
        
        if df is None or df.empty:
            result['message'] = f'未找到股票代码 {code_clean} 的数据'
            return result
        
        # 清洗数据
        cleaned = _clean_dataframe(df)
        records = cleaned.to_dict(orient='records')
        safe_records = _to_json_safe(records)
        
        result['status'] = 'ok'
        result['message'] = '查询成功'
        result['data'] = safe_records[0] if safe_records else None
        
        return result
        
    except Exception as e:
        result['message'] = f'查询失败: {str(e)}'
        print(f"get_stock_realtime_info error: {e}")
        return result


def get_stock_realtime_batch(codes: List[str]) -> Dict[str, Any]:
    """批量获取多个股票的实时行情
    
    参数:
    - codes: 股票代码列表（如 ['000001', '600000', '300750']）
    
    返回:
    {
        'status': 'ok' | 'error',
        'message': str,
        'total': int,
        'data': [{ ... }, ...]
    }
    """
    result = {
        'status': 'error',
        'message': '',
        'total': 0,
        'data': []
    }
    
    try:
        if not codes or len(codes) == 0:
            result['message'] = '股票代码列表不能为空'
            return result
            
        if ak is None:
            result['message'] = 'akshare 未安装，无法查询'
            return result
        
        # 获取所有A股实时数据
        df = ak.stock_zh_a_spot_em()
        
        if df is None or df.empty:
            result['message'] = '获取市场数据失败'
            return result
        
        # 清洗代码列表
        codes_clean = [str(c).strip().zfill(6) if len(str(c).strip()) < 6 else str(c).strip() for c in codes]
        
        # 筛选指定的股票
        filtered = df[df['代码'].isin(codes_clean)]
        
        if filtered.empty:
            result['message'] = f'未找到任何股票数据'
            result['status'] = 'ok'
            return result
        
        # 清洗数据
        cleaned = _clean_dataframe(filtered)
        records = cleaned.to_dict(orient='records')
        safe_records = _to_json_safe(records)
        
        result['status'] = 'ok'
        result['message'] = f'成功获取 {len(safe_records)} 只股票的实时数据'
        result['total'] = len(safe_records)
        result['data'] = safe_records
        
        return result
        
    except Exception as e:
        result['message'] = f'查询失败: {str(e)}'
        print(f"get_stock_realtime_batch error: {e}")
        return result



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
            elif isinstance(v, decimal.Decimal):
                # convert Decimal to float when possible, fallback to string
                try:
                    nr[k] = float(v)
                except Exception:
                    nr[k] = str(v)
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
    """从数据库表 stock_daily_data 中读取历史日线数据并返回 JSON-safe 的记录列表。

    说明：项目中历史数据已统一存为不复权原始数据（unadjusted），因此该函数忽略 adjust/source 参数，
    仅根据 code/日期区间返回存库数据。返回字段会标准化（中文列名）以兼容前端。
    """
    global last_stock_history_error, _history_cache
    last_stock_history_error = None

    # build cache key (still keep lightweight cache)
    try:
        cache_key = f"db|{code}|{start_date or ''}|{end_date or ''}"
        if cache_key in _history_cache:
            ts, cached = _history_cache[cache_key]
            if time.time() - ts < CACHE_TTL_SECS:
                logger.debug("get_stock_history_data (db): cache hit for %s", cache_key)
                return list(cached)
            else:
                _history_cache.pop(cache_key, None)
    except Exception:
        logger.debug("history cache check failed", exc_info=True)

    try:
        if not code:
            return []

        # normalize possible stock_code formats stored in DB
        c = str(code).strip()
        candidates = set()
        # if provided like 'sh600000' or 'SH600000'
        if c.lower().startswith('sh') or c.lower().startswith('sz'):
            candidates.add(c.upper())
            candidates.add(c.lower())
            # also add 6-digit form
            candidates.add(c[-6:])
        else:
            # add prefixed forms and raw
            if c.isdigit() and len(c) == 6:
                candidates.add(c)
                candidates.add('SZ' + c)
                candidates.add('SH' + c)
            else:
                candidates.add(c)

        # prepare date filters
        date_where = ''
        params: Dict[str, Any] = {}
        if start_date:
            # expect YYYYMMDD -> convert to YYYY-MM-DD
            try:
                sd = f"{start_date[:4]}-{start_date[4:6]}-{start_date[6:8]}"
                date_where += " AND trade_date >= :start_date"
                params['start_date'] = sd
            except Exception:
                pass
        if end_date:
            try:
                ed = f"{end_date[:4]}-{end_date[4:6]}-{end_date[6:8]}"
                date_where += " AND trade_date <= :end_date"
                params['end_date'] = ed
            except Exception:
                pass

        # build SQL with candidate matches
        cand_list = list(candidates)
        # use parameterized IN list
        placeholders = ','.join([f":c{i}" for i in range(len(cand_list))])
        for i, val in enumerate(cand_list):
            params[f'c{i}'] = val

        sql = f"""
            SELECT trade_date, open_price, high_price, low_price, close_price, pre_close,
                   change_amount, pct_chg, volume, amount
            FROM stock_daily_data
            WHERE stock_code IN ({placeholders}) {date_where}
            ORDER BY trade_date ASC
        """

        with engine.connect() as conn:
            res = conn.execute(text(sql), params)
            # use mappings() to get dict-like rows (prevents tuple rows that cause dict() failures)
            try:
                rows = res.mappings().fetchall()
            except Exception:
                # fallback to raw fetchall and convert using _mapping if available
                raw_rows = res.fetchall()
                rows = []
                for r in raw_rows:
                    try:
                        # SQLAlchemy Row may expose _mapping
                        rows.append(r._mapping if hasattr(r, '_mapping') else dict(r))
                    except Exception:
                        # last resort: build dict from keys and values
                        try:
                            keys = res.keys()
                            rows.append({k: v for k, v in zip(keys, r)})
                        except Exception:
                            # give up and append empty
                            rows.append({})

        if not rows:
            return []

        # convert to DataFrame for reuse of standardization/cleaning
        df = pd.DataFrame([dict(r) for r in rows])
        # rename DB columns to friendly names so _standardize_history_columns can map them
        # ensure column names include date/open/close/high/low/volume/amount
        rename_map = {
            'trade_date': '日期',
            'open_price': '开盘',
            'high_price': '最高',
            'low_price': '最低',
            'close_price': '收盘',
            'pre_close': '昨收',
            'change_amount': '涨跌额',
            'pct_chg': '涨跌幅',
            'volume': '成交量',
            'amount': '成交额'
        }
        try:
            df = df.rename(columns=rename_map)
        except Exception:
            pass

        # ensure 日期 formatted
        try:
            if '日期' in df.columns:
                df['日期'] = pd.to_datetime(df['日期']).dt.strftime('%Y-%m-%d')
        except Exception:
            df['日期'] = df['日期'].astype(str)

        # run cleaning to normalize numeric types and NaN
        cleaned = _clean_dataframe(df)
        records = cleaned.to_dict(orient='records')

        # cache
        try:
            _history_cache[cache_key] = (time.time(), list(records))
            if len(_history_cache) > CACHE_MAX_ENTRIES:
                oldest = min(_history_cache.items(), key=lambda kv: kv[1][0])[0]
                _history_cache.pop(oldest, None)
        except Exception:
            pass

        return _to_json_safe(records)
    except Exception as e:
        import traceback as _tb
        tb = _tb.format_exc()
        last_stock_history_error = str(e)
        logger.error("Error in get_stock_history_data (db): %s", last_stock_history_error)
        logger.debug("Full traceback:\n%s", tb)
        return []


def search_companies_by_industry(
    db, 
    q: str, 
    page: int = 1, 
    page_size: int = 50, 
    industry: str = None,
    industry_match_mode: str = 'any',
    search_mode: str = 'fuzzy',
    min_capital: float = None,
    max_capital: float = None,
    region: str = None,
    security_types: str = None
) -> Dict[str, Any]:
    """按关键词和/或行业搜索公司列表（支持分页和高级筛选）

    参数:
    - db: 数据库会话
    - q: 搜索关键词（股票代码、公司名称等）
    - page: 页码（从1开始）
    - page_size: 每页数量（默认50）
    - industry: 行业筛选（逗号分隔，支持多个），如 "电子,计算机,通信"
    - industry_match_mode: 'any'(满足任一) 或 'all'(满足全部)
    - search_mode: 'fuzzy'(模糊) 或 'exact'(精准)
    - min_capital: 最小注册资本（元）
    - max_capital: 最大注册资本（元）
    - region: 地区筛选
    - security_types: 证券类型筛选（逗号分隔）

    返回:
    {
        'total': 总数量,
        'page': 当前页码,
        'page_size': 每页大小,
        'total_pages': 总页数,
        'data': [{'stock_code': ..., 'company_name': ..., 'eastmoney_industry': ..., 'regulatory_industry': ...}, ...]
    }
    """
    try:
        # 至少需要一个搜索条件
        if not q and not industry:
            return {'total': 0, 'page': 1, 'page_size': page_size, 'total_pages': 0, 'data': []}

        # 查询字段（优化显示内容）
        cols = [
            'stock_code',              # 股票代码
            'a_stock_abbr',            # 股票简称
            'company_name',            # 公司名称
            'security_category',       # 证券类型
            'chairman',                # 董事长
            'legal_representative',    # 法人
            'region',                  # 区域
            'registered_capital',      # 注册资本（元）
            'eastmoney_industry',      # 东财行业（保留用于筛选）
            'regulatory_industry',     # 证监会行业（保留用于筛选）
            'listing_exchange'         # 交易所
        ]
        cols_sql = ', '.join(cols)

        # 构建 WHERE 条件
        where_conditions = []
        params = {}

        # 关键字搜索
        if q:
            if search_mode == 'exact':
                # 精准匹配
                where_conditions.append("""
                    (stock_code = :exact_q 
                    OR company_name = :exact_q 
                    OR a_stock_abbr = :exact_q)
                """)
                params['exact_q'] = q
            else:
                # 模糊搜索
                likeq = f"%{q}%"
                where_conditions.append("""
                    (stock_code LIKE :likeq 
                    OR company_name LIKE :likeq 
                    OR a_stock_abbr LIKE :likeq
                    OR eastmoney_industry LIKE :likeq 
                    OR regulatory_industry LIKE :likeq)
                """)
                params['likeq'] = likeq
                params['q'] = q

        # 行业筛选
        if industry:
            industries = [ind.strip() for ind in industry.split(',') if ind.strip()]
            if industries:
                if industry_match_mode == 'all':
                    # 满足全部标签（AND关系）
                    for i, ind in enumerate(industries):
                        key_east = f'ind_east_{i}'
                        key_reg = f'ind_reg_{i}'
                        where_conditions.append(f"""
                            (eastmoney_industry LIKE :{key_east} 
                             OR regulatory_industry LIKE :{key_reg})
                        """)
                        params[key_east] = f"%{ind}%"
                        params[key_reg] = f"%{ind}%"
                else:
                    # 满足任一标签（OR关系）
                    industry_or_conditions = []
                    for i, ind in enumerate(industries):
                        key_east = f'ind_east_{i}'
                        key_reg = f'ind_reg_{i}'
                        industry_or_conditions.append(f"""
                            (eastmoney_industry LIKE :{key_east} 
                             OR regulatory_industry LIKE :{key_reg})
                        """)
                        params[key_east] = f"%{ind}%"
                        params[key_reg] = f"%{ind}%"
                    
                    if industry_or_conditions:
                        where_conditions.append(f"({' OR '.join(industry_or_conditions)})")

        # 注册资本范围筛选
        # 数据库中存储格式：数字+单位（如 "194.1亿"、"119.3亿"、"1.324亿"）
        # 需要提取数字部分并根据单位换算为元
        if min_capital is not None:
            where_conditions.append("""
                (CASE 
                    WHEN registered_capital LIKE '%亿%' THEN 
                        CAST(REPLACE(REPLACE(registered_capital, '亿', ''), ' ', '') AS DECIMAL(20, 2)) * 100000000
                    WHEN registered_capital LIKE '%万%' THEN 
                        CAST(REPLACE(REPLACE(registered_capital, '万', ''), ' ', '') AS DECIMAL(20, 2)) * 10000
                    WHEN registered_capital LIKE '%元%' THEN 
                        CAST(REPLACE(REPLACE(registered_capital, '元', ''), ' ', '') AS DECIMAL(20, 2))
                    ELSE 
                        CAST(registered_capital AS DECIMAL(20, 2))
                END) >= :min_capital
            """)
            params['min_capital'] = min_capital
        
        if max_capital is not None:
            where_conditions.append("""
                (CASE 
                    WHEN registered_capital LIKE '%亿%' THEN 
                        CAST(REPLACE(REPLACE(registered_capital, '亿', ''), ' ', '') AS DECIMAL(20, 2)) * 100000000
                    WHEN registered_capital LIKE '%万%' THEN 
                        CAST(REPLACE(REPLACE(registered_capital, '万', ''), ' ', '') AS DECIMAL(20, 2)) * 10000
                    WHEN registered_capital LIKE '%元%' THEN 
                        CAST(REPLACE(REPLACE(registered_capital, '元', ''), ' ', '') AS DECIMAL(20, 2))
                    ELSE 
                        CAST(registered_capital AS DECIMAL(20, 2))
                END) <= :max_capital
            """)
            params['max_capital'] = max_capital

        # 地区筛选
        if region:
            where_conditions.append("region LIKE :region")
            params['region'] = f"%{region}%"

        # 证券类型筛选
        if security_types:
            types = [t.strip() for t in security_types.split(',') if t.strip()]
            if types:
                type_conditions = []
                for i, stype in enumerate(types):
                    key = f'stype_{i}'
                    type_conditions.append(f"security_category LIKE :{key}")
                    params[key] = f"%{stype}%"
                
                if type_conditions:
                    where_conditions.append(f"({' OR '.join(type_conditions)})")

        # 组合 WHERE 子句
        where_clause = ' AND '.join(where_conditions) if where_conditions else '1=1'

        with db.begin():
            # 使用 DISTINCT 去重
            count_sql = f"""
                SELECT COUNT(DISTINCT stock_code) as total FROM stock_basic_info 
                WHERE {where_clause}
            """
            
            count_result = db.execute(text(count_sql), params).fetchone()
            total = count_result[0] if count_result else 0

            if total == 0:
                return {'total': 0, 'page': page, 'page_size': page_size, 'total_pages': 0, 'data': []}

            # 计算总页数
            total_pages = (total + page_size - 1) // page_size
            
            # 确保页码有效
            if page < 1:
                page = 1
            if page > total_pages:
                page = total_pages

            # 计算偏移量
            offset = (page - 1) * page_size

            # 查询数据（使用 DISTINCT 去重，按优先级排序）
            order_clause = ""
            if q and search_mode == 'fuzzy':
                order_clause = f"""
                    ORDER BY 
                        CASE 
                            WHEN stock_code = :q THEN 1
                            WHEN stock_code LIKE :likeq THEN 2
                            WHEN eastmoney_industry LIKE :likeq THEN 3
                            WHEN regulatory_industry LIKE :likeq THEN 4
                            ELSE 5
                        END,
                        stock_code
                """
            else:
                order_clause = "ORDER BY stock_code"

            data_sql = f"""
                SELECT DISTINCT {cols_sql} FROM stock_basic_info 
                WHERE {where_clause}
                {order_clause}
                LIMIT :limit OFFSET :offset
            """
            
            params['limit'] = page_size
            params['offset'] = offset
            
            results = db.execute(text(data_sql), params).mappings().fetchall()

            data = [dict(r) for r in results]

            return {
                'total': total,
                'page': page,
                'page_size': page_size,
                'total_pages': total_pages,
                'data': data
            }

    except Exception as e:
        print(f"search_companies_by_industry error: {e}")
        traceback.print_exc()
        return {'total': 0, 'page': 1, 'page_size': page_size, 'total_pages': 0, 'data': [], 'error': str(e)}


def get_company_profile(db, q: str) -> Optional[Dict[str, Any]]:
    """从数据库中查询公司基本资料，q 可以是股票代码或公司名称（模糊匹配）

    返回单条记录的字典或 None。
    """
    try:
        if not q:
            return None

        # explicit columns to return (keep stable ordering and field names for frontend)
        # 排除字段: extended_abbr, b_stock_code, h_stock_code, b_stock_abbr, h_stock_abbr
        cols = [
            'stock_code', 'company_name', 'english_name', 
            'a_stock_code', 'a_stock_abbr', 'former_name',
            'security_category', 'eastmoney_industry', 'listing_exchange', 'regulatory_industry',
            'general_manager', 'legal_representative', 'board_secretary', 'chairman',
            'securities_representative', 'independent_directors',
            'contact_phone', 'email', 'fax', 'website',
            'office_address', 'registered_address', 'region', 'postal_code',
            'registered_capital', 'business_registration', 'employee_count', 'management_count',
            'law_firm', 'accounting_firm', 'company_intro', 'business_scope'
        ]
        cols_sql = ', '.join(cols)

        # 使用 SQL 进行模糊匹配，优先尝试按 stock_code 精确匹配
        sql_exact = f"SELECT {cols_sql} FROM stock_basic_info WHERE stock_code = :q LIMIT 1"
        with db.begin():
            # use mappings() to get a dict-like result across SQLAlchemy versions
            res = db.execute(text(sql_exact), {"q": q}).mappings().fetchone()
            profile = None
            if res:
                profile = dict(res)

            # 模糊匹配 company_name 或 a_stock_code 或 a_stock_abbr
            if profile is None:
                sql_like = f"SELECT {cols_sql} FROM stock_basic_info WHERE company_name LIKE :likeq OR a_stock_code LIKE :likeq OR a_stock_abbr LIKE :likeq LIMIT 1"
                likeq = f"%{q}%"
                res2 = db.execute(text(sql_like), {"likeq": likeq}).mappings().fetchone()
                if res2:
                    profile = dict(res2)

            if profile is None:
                return None

            # fetch related tables: shareholdings and issuer/issuance records
            stock_code = profile.get('stock_code')
            try:
                # use actual column names in stock_shareholding_info (created_time / updated_time)
                sh_sql = """
                    SELECT id, enterprise_name, registered_capital, group_holding_ratio, created_time, updated_time
                    FROM stock_shareholding_info
                    WHERE stock_code = :stock_code
                    ORDER BY updated_time DESC
                """
                sh_rows = db.execute(text(sh_sql), {"stock_code": stock_code}).mappings().fetchall()
                shareholdings = [dict(r) for r in sh_rows] if sh_rows else []
            except Exception:
                logger.debug("Failed to query stock_shareholding_info for %s", stock_code, exc_info=True)
                shareholdings = []

            try:
                # stock_issuer_info uses different column names (sponsor_institution, main_underwriter, establishment_date, listing_date, etc.)
                issuer_sql = """
                    SELECT id, sponsor_institution, main_underwriter, establishment_date, listing_date,
                           issue_pe_ratio, online_issue_date, issue_method, face_value_per_share,
                           issue_quantity, issue_price_per_share, issue_cost, total_issue_market_value,
                           net_funds_raised, first_day_open_price, first_day_close_price, first_day_turnover_rate,
                           first_day_high_price, offline_allotment_lottery_rate, pricing_lottery_rate, created_time, updated_time
                    FROM stock_issuer_info
                    WHERE stock_code = :stock_code
                    ORDER BY listing_date DESC
                """
                issuer_rows = db.execute(text(issuer_sql), {"stock_code": stock_code}).mappings().fetchall()
                issuance = [dict(r) for r in issuer_rows] if issuer_rows else []
            except Exception:
                logger.debug("Failed to query stock_issuer_info for %s", stock_code, exc_info=True)
                issuance = []

            # sanitize numeric/complex types to JSON-friendly primitives
            profile['shareholdings'] = _to_json_safe(shareholdings)
            profile['issuance'] = _to_json_safe(issuance)

            return profile
    except Exception as e:
        print(f"get_company_profile error: {e}")
        return None
