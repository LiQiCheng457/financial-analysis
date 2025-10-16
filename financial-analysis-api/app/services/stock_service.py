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

import pandas as pd
import numpy as np
import math
import traceback
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy import text


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


        def search_stocks(query: str, limit: int = 20) -> List[Dict[str, Any]]:
            """搜索股票（按代码或名称模糊匹配）。

            若环境中安装并可用 akshare，会尝试从常见的 A 股列表中搜索；否则返回空列表。
            返回格式: [{ 'code': '600519', 'name': '贵州茅台' }, ...]
            """
            try:
                if not query:
                    return []
                q = str(query).strip()
                if ak is None:
                    return []

                # Try to load a list of A-share codes/names and filter
                # ak.stock_zh_a_spot provides real-time snapshot; fallback to other available methods
                df = None
                if hasattr(ak, 'stock_zh_a_spot'):
                    try:
                        df = ak.stock_zh_a_spot()
                    except Exception:
                        df = None

                # If df is available, try to extract code/name columns
                results: List[Dict[str, Any]] = []
                if df is not None:
                    # normalise columns
                    cols = [c.lower() for c in df.columns]
                    # try to find code and name columns
                    code_col = None
                    name_col = None
                    for c in df.columns:
                        lc = str(c).lower()
                        if 'code' in lc or '股票代码' in lc or '代码' in lc:
                            code_col = c
                        if 'name' in lc or '股票名称' in lc or '名称' in lc:
                            name_col = c
                    if code_col is None and '代码' in df.columns:
                        code_col = '代码'
                    if name_col is None and '名称' in df.columns:
                        name_col = '名称'

                    if code_col is None or name_col is None:
                        # try common keys
                        for c in df.columns:
                            if str(c).lower() in ('code', 'symbol') and code_col is None:
                                code_col = c
                            if str(c).lower() in ('name', 'stock_name') and name_col is None:
                                name_col = c

                    # fallback: use first two columns
                    if code_col is None:
                        code_col = df.columns[0]
                    if name_col is None and len(df.columns) > 1:
                        name_col = df.columns[1]

                    # do case-insensitive contains filter on code or name
                    for _, row in df.iterrows():
                        try:
                            code_val = str(row.get(code_col, '')).strip()
                            name_val = str(row.get(name_col, '')).strip()
                            if q in code_val or q in name_val:
                                results.append({'code': code_val, 'name': name_val})
                                if len(results) >= limit:
                                    break
                        except Exception:
                            continue

                return results
            except Exception as e:
                print(f"search_stocks error: {e}")
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


def search_companies_by_industry(db, q: str, page: int = 1, page_size: int = 50, industry: str = None) -> Dict[str, Any]:
    """按关键词和/或行业搜索公司列表（支持分页）

    参数:
    - db: 数据库会话
    - q: 搜索关键词（股票代码、公司名称等）
    - page: 页码（从1开始）
    - page_size: 每页数量（默认50）
    - industry: 行业筛选（逗号分隔，支持多个），如 "电子,计算机,通信"

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

        # 关键字搜索（原有逻辑）
        if q:
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

        # 行业筛选（新增逻辑 - OR 条件）
        if industry:
            industries = [ind.strip() for ind in industry.split(',') if ind.strip()]
            if industries:
                industry_or_conditions = []
                for i, ind in enumerate(industries):
                    key_east = f'ind_east_{i}'
                    key_reg = f'ind_reg_{i}'
                    industry_or_conditions.append(f"""
                        (eastmoney_industry LIKE :{key_east} OR regulatory_industry LIKE :{key_reg})
                    """)
                    params[key_east] = f"%{ind}%"
                    params[key_reg] = f"%{ind}%"
                
                if industry_or_conditions:
                    where_conditions.append(f"({' OR '.join(industry_or_conditions)})")

        # 组合 WHERE 子句
        where_clause = ' AND '.join(where_conditions) if where_conditions else '1=1'

        with db.begin():
            # 使用 DISTINCT 去重（防止同一公司因多个行业匹配而重复）
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
            if q:
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
            if res:
                return dict(res)

            # 模糊匹配 company_name 或 a_stock_code 或 a_stock_abbr
            sql_like = f"SELECT {cols_sql} FROM stock_basic_info WHERE company_name LIKE :likeq OR a_stock_code LIKE :likeq OR a_stock_abbr LIKE :likeq LIMIT 1"
            likeq = f"%{q}%"
            res2 = db.execute(text(sql_like), {"likeq": likeq}).mappings().fetchone()
            if res2:
                return dict(res2)

        return None
    except Exception as e:
        print(f"get_company_profile error: {e}")
        return None
