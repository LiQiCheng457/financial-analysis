"""技术指标计算服务

提供常用技术指标的计算：
- MA: 移动平均线
- EMA: 指数移动平均线
- MACD: 平滑异同移动平均线
- KDJ: 随机指标
- RSI: 相对强弱指标
- BOLL: 布林带
- VOL: 成交量指标
- 信号检测：识别买卖信号
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime


def calculate_ma(data: pd.DataFrame, periods: List[int] = [5, 10, 20, 60]) -> pd.DataFrame:
    """计算移动平均线 (Moving Average)
    
    Args:
        data: DataFrame，必须包含'收盘'列
        periods: 均线周期列表，默认[5, 10, 20, 60]
    
    Returns:
        DataFrame，添加了MA5, MA10, MA20, MA60等列
    """
    df = data.copy()
    
    for period in periods:
        col_name = f'MA{period}'
        df[col_name] = df['收盘'].rolling(window=period, min_periods=1).mean()
    
    return df


def calculate_ema(data: pd.DataFrame, periods: List[int] = [12, 26]) -> pd.DataFrame:
    """计算指数移动平均线 (Exponential Moving Average)
    
    Args:
        data: DataFrame，必须包含'收盘'列
        periods: EMA周期列表
    
    Returns:
        DataFrame，添加了EMA12, EMA26等列
    """
    df = data.copy()
    
    for period in periods:
        col_name = f'EMA{period}'
        df[col_name] = df['收盘'].ewm(span=period, adjust=False).mean()
    
    return df


def calculate_macd(data: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """计算MACD指标 (Moving Average Convergence Divergence)
    
    Args:
        data: DataFrame，必须包含'收盘'列
        fast: 快速EMA周期，默认12
        slow: 慢速EMA周期，默认26
        signal: 信号线周期，默认9
    
    Returns:
        DataFrame，添加了DIF, DEA, MACD列
    """
    df = data.copy()
    
    # 计算快速和慢速EMA
    ema_fast = df['收盘'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['收盘'].ewm(span=slow, adjust=False).mean()
    
    # DIF = 快线 - 慢线
    df['DIF'] = ema_fast - ema_slow
    
    # DEA = DIF的9日EMA (信号线)
    df['DEA'] = df['DIF'].ewm(span=signal, adjust=False).mean()
    
    # MACD柱 = 2 * (DIF - DEA)
    df['MACD'] = 2 * (df['DIF'] - df['DEA'])
    
    return df


def calculate_kdj(data: pd.DataFrame, n: int = 9, m1: int = 3, m2: int = 3) -> pd.DataFrame:
    """计算KDJ指标 (Stochastic Oscillator)
    
    Args:
        data: DataFrame，必须包含'最高', '最低', '收盘'列
        n: RSV周期，默认9
        m1: K值平滑周期，默认3
        m2: D值平滑周期，默认3
    
    Returns:
        DataFrame，添加了K, D, J列
    """
    df = data.copy()
    
    # 计算RSV (未成熟随机值)
    low_min = df['最低'].rolling(window=n, min_periods=1).min()
    high_max = df['最高'].rolling(window=n, min_periods=1).max()
    
    rsv = (df['收盘'] - low_min) / (high_max - low_min) * 100
    rsv = rsv.fillna(50)  # 初始值设为50
    
    # 计算K值 (RSV的移动平均)
    df['K'] = rsv.ewm(alpha=1/m1, adjust=False).mean()
    
    # 计算D值 (K值的移动平均)
    df['D'] = df['K'].ewm(alpha=1/m2, adjust=False).mean()
    
    # 计算J值
    df['J'] = 3 * df['K'] - 2 * df['D']
    
    return df


def calculate_rsi(data: pd.DataFrame, periods: List[int] = [6, 12, 24]) -> pd.DataFrame:
    """计算RSI指标 (Relative Strength Index)
    
    Args:
        data: DataFrame，必须包含'收盘'列
        periods: RSI周期列表，默认[6, 12, 24]
    
    Returns:
        DataFrame，添加了RSI6, RSI12, RSI24列
    """
    df = data.copy()
    
    # 计算价格变化
    delta = df['收盘'].diff()
    
    for period in periods:
        # 分离涨跌
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        
        # 计算平均涨跌
        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()
        
        # 计算RS和RSI
        rs = avg_gain / avg_loss.replace(0, 1e-10)  # 避免除0
        rsi = 100 - (100 / (1 + rs))
        
        col_name = f'RSI{period}'
        df[col_name] = rsi
    
    return df


def calculate_boll(data: pd.DataFrame, period: int = 20, std_dev: float = 2) -> pd.DataFrame:
    """计算布林带指标 (Bollinger Bands)
    
    Args:
        data: DataFrame，必须包含'收盘'列
        period: 均线周期，默认20
        std_dev: 标准差倍数，默认2
    
    Returns:
        DataFrame，添加了BOLL_MIDDLE, BOLL_UPPER, BOLL_LOWER列
    """
    df = data.copy()
    
    # 中轨 = N日移动平均线
    df['BOLL_MIDDLE'] = df['收盘'].rolling(window=period, min_periods=1).mean()
    
    # 标准差
    std = df['收盘'].rolling(window=period, min_periods=1).std()
    
    # 上轨 = 中轨 + K * 标准差
    df['BOLL_UPPER'] = df['BOLL_MIDDLE'] + std_dev * std
    
    # 下轨 = 中轨 - K * 标准差
    df['BOLL_LOWER'] = df['BOLL_MIDDLE'] - std_dev * std
    
    return df


def calculate_vol_ma(data: pd.DataFrame, periods: List[int] = [5, 10]) -> pd.DataFrame:
    """计算成交量均线
    
    Args:
        data: DataFrame，必须包含'成交量'列
        periods: 均量周期列表，默认[5, 10]
    
    Returns:
        DataFrame，添加了VOL_MA5, VOL_MA10列
    """
    df = data.copy()
    
    for period in periods:
        col_name = f'VOL_MA{period}'
        df[col_name] = df['成交量'].rolling(window=period, min_periods=1).mean()
    
    return df


def calculate_all_indicators(data: List[Dict[str, Any]], 
                             indicators: Optional[List[str]] = None) -> Dict[str, Any]:
    """计算所有技术指标
    
    Args:
        data: 股票历史数据列表
        indicators: 需要计算的指标列表，None表示计算所有指标
            可选值: ['MA', 'EMA', 'MACD', 'KDJ', 'RSI', 'BOLL', 'VOL']
    
    Returns:
        包含原始数据和指标数据的字典
    """
    # 基本输入校验
    if not data:
        return {'status': 'error', 'message': '数据为空'}
    
    try:
        # 转换为DataFrame
        df = pd.DataFrame(data)

        # 容错：如果前端/数据库使用英文列名或其他命名，尝试进行常见列名映射
        # 例如: trade_date -> 日期, close -> 收盘, high -> 最高, low -> 最低, volume -> 成交量
        col_aliases = {
            'trade_date': '日期', 'tradeDate': '日期', 'date': '日期',
            'close': '收盘', 'close_price': '收盘', 'closePrice': '收盘',
            'open': '开盘', 'open_price': '开盘',
            'high': '最高', 'high_price': '最高',
            'low': '最低', 'low_price': '最低',
            'volume': '成交量', 'vol': '成交量',
            'amount': '成交额', 'pct_chg': '涨跌幅', 'change': '涨跌额'
        }
        # 进行列名替换（只替换存在的列）
        rename_map = {c: col_aliases[c] for c in df.columns if c in col_aliases}
        if rename_map:
            df = df.rename(columns=rename_map)

        # 确保必要的列存在（尝试宽松检测）
        required_cols = ['日期', '收盘']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            return {'status': 'error', 'message': f'缺少必要列: {missing_cols}'}

        # 强制将关键数值列转换为数值类型，不能转换的设为 NaN
        try:
            df['收盘'] = pd.to_numeric(df['收盘'], errors='coerce')
            if '开盘' in df.columns:
                df['开盘'] = pd.to_numeric(df['开盘'], errors='coerce')
            if '最高' in df.columns:
                df['最高'] = pd.to_numeric(df['最高'], errors='coerce')
            if '最低' in df.columns:
                df['最低'] = pd.to_numeric(df['最低'], errors='coerce')
            if '成交量' in df.columns:
                df['成交量'] = pd.to_numeric(df['成交量'], errors='coerce')
        except Exception:
            # 若数值转换发生异常，返回更清晰的错误信息以便前端/日志定位
            return {'status': 'error', 'message': '关键数值列类型转换失败'}
        
        # 按日期排序
        df = df.sort_values('日期').reset_index(drop=True)
        
        # 默认计算所有指标
        if indicators is None:
            indicators = ['MA', 'EMA', 'MACD', 'KDJ', 'RSI', 'BOLL', 'VOL']
        
        # 计算各项指标
        if 'MA' in indicators:
            df = calculate_ma(df, periods=[5, 10, 20, 60])
        
        if 'EMA' in indicators:
            df = calculate_ema(df, periods=[12, 26])
        
        if 'MACD' in indicators:
            df = calculate_macd(df)
        
        if 'KDJ' in indicators and all(col in df.columns for col in ['最高', '最低']):
            df = calculate_kdj(df)
        
        if 'RSI' in indicators:
            df = calculate_rsi(df, periods=[6, 12, 24])
        
        if 'BOLL' in indicators:
            df = calculate_boll(df)
        
        if 'VOL' in indicators and '成交量' in df.columns:
            df = calculate_vol_ma(df)
        
        # 处理NaN值
        df = df.replace({np.nan: None, np.inf: None, -np.inf: None})
        
        # 转回字典列表
        result_data = df.to_dict('records')
        
        return {
            'status': 'ok',
            'data': result_data,
            'indicators': indicators,
            'total': len(result_data)
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'message': f'计算技术指标失败: {str(e)}'
        }


def get_indicator_config() -> Dict[str, Any]:
    """获取技术指标配置信息
    
    Returns:
        各指标的默认参数和说明
    """
    return {
        'MA': {
            'name': '移动平均线',
            'description': '反映价格趋势的平滑指标',
            'default_periods': [5, 10, 20, 60],
            'adjustable': True
        },
        'EMA': {
            'name': '指数移动平均线',
            'description': '对近期价格赋予更高权重的均线',
            'default_periods': [12, 26],
            'adjustable': True
        },
        'MACD': {
            'name': '平滑异同移动平均线',
            'description': '趋势跟踪和动量指标',
            'default_params': {'fast': 12, 'slow': 26, 'signal': 9},
            'adjustable': True
        },
        'KDJ': {
            'name': '随机指标',
            'description': '超买超卖指标，范围0-100',
            'default_params': {'n': 9, 'm1': 3, 'm2': 3},
            'adjustable': True
        },
        'RSI': {
            'name': '相对强弱指标',
            'description': '衡量价格变动速度和幅度',
            'default_periods': [6, 12, 24],
            'adjustable': True
        },
        'BOLL': {
            'name': '布林带',
            'description': '价格波动区间指标',
            'default_params': {'period': 20, 'std_dev': 2},
            'adjustable': True
        },
        'VOL': {
            'name': '成交量均线',
            'description': '成交量的移动平均',
            'default_periods': [5, 10],
            'adjustable': True
        }
    }


def detect_signals(data: pd.DataFrame, lookback: int = 5) -> List[Dict[str, Any]]:
    """检测技术信号
    
    Args:
        data: DataFrame，必须包含技术指标数据
        lookback: 回看天数，检测最近N天的信号
    
    Returns:
        信号列表，每个信号包含日期、类型、指标、描述、强度等信息
    """
    if len(data) < 2:
        return []
    
    signals = []
    
    # 只检测最近的数据
    recent_data = data.tail(lookback) if len(data) > lookback else data
    
    for i in range(1, len(recent_data)):
        idx = recent_data.index[i]
        prev_idx = recent_data.index[i-1]
        date = str(recent_data.loc[idx, '日期'])
        
        # 1. MACD信号检测
        if 'DIF' in recent_data.columns and 'DEA' in recent_data.columns:
            dif_curr = recent_data.loc[idx, 'DIF']
            dif_prev = recent_data.loc[prev_idx, 'DIF']
            dea_curr = recent_data.loc[idx, 'DEA']
            dea_prev = recent_data.loc[prev_idx, 'DEA']
            
            if pd.notna(dif_curr) and pd.notna(dif_prev) and pd.notna(dea_curr) and pd.notna(dea_prev):
                # MACD金叉
                if dif_prev < dea_prev and dif_curr > dea_curr:
                    macd_val = recent_data.loc[idx, 'MACD'] if 'MACD' in recent_data.columns else 0
                    strength = min(5, max(1, int(abs(macd_val) / 0.1) + 3))
                    signals.append({
                        'date': date,
                        'type': 'buy',
                        'indicator': 'MACD',
                        'name': 'MACD金叉',
                        'description': f'DIF上穿DEA，形成金叉买入信号',
                        'strength': strength,
                        'price': float(recent_data.loc[idx, '收盘']) if '收盘' in recent_data.columns else None,
                        'details': {
                            'DIF': float(dif_curr),
                            'DEA': float(dea_curr),
                            'MACD': float(macd_val) if pd.notna(macd_val) else None
                        }
                    })
                
                # MACD死叉
                elif dif_prev > dea_prev and dif_curr < dea_curr:
                    macd_val = recent_data.loc[idx, 'MACD'] if 'MACD' in recent_data.columns else 0
                    strength = min(5, max(1, int(abs(macd_val) / 0.1) + 3))
                    signals.append({
                        'date': date,
                        'type': 'sell',
                        'indicator': 'MACD',
                        'name': 'MACD死叉',
                        'description': f'DIF下穿DEA，形成死叉卖出信号',
                        'strength': strength,
                        'price': float(recent_data.loc[idx, '收盘']) if '收盘' in recent_data.columns else None,
                        'details': {
                            'DIF': float(dif_curr),
                            'DEA': float(dea_curr),
                            'MACD': float(macd_val) if pd.notna(macd_val) else None
                        }
                    })
        
        # 2. KDJ信号检测
        if 'K' in recent_data.columns and 'D' in recent_data.columns:
            k_curr = recent_data.loc[idx, 'K']
            k_prev = recent_data.loc[prev_idx, 'K']
            d_curr = recent_data.loc[idx, 'D']
            d_prev = recent_data.loc[prev_idx, 'D']
            j_curr = recent_data.loc[idx, 'J'] if 'J' in recent_data.columns else None
            
            if pd.notna(k_curr) and pd.notna(k_prev) and pd.notna(d_curr) and pd.notna(d_prev):
                # KDJ金叉（低位）
                if k_prev < d_prev and k_curr > d_curr and k_curr < 30:
                    signals.append({
                        'date': date,
                        'type': 'buy',
                        'indicator': 'KDJ',
                        'name': 'KDJ低位金叉',
                        'description': f'K线上穿D线，且处于超卖区域（K={k_curr:.1f}），买入信号',
                        'strength': 5,
                        'price': float(recent_data.loc[idx, '收盘']) if '收盘' in recent_data.columns else None,
                        'details': {
                            'K': float(k_curr),
                            'D': float(d_curr),
                            'J': float(j_curr) if pd.notna(j_curr) else None
                        }
                    })
                
                # KDJ死叉（高位）
                elif k_prev > d_prev and k_curr < d_curr and k_curr > 70:
                    signals.append({
                        'date': date,
                        'type': 'sell',
                        'indicator': 'KDJ',
                        'name': 'KDJ高位死叉',
                        'description': f'K线下穿D线，且处于超买区域（K={k_curr:.1f}），卖出信号',
                        'strength': 5,
                        'price': float(recent_data.loc[idx, '收盘']) if '收盘' in recent_data.columns else None,
                        'details': {
                            'K': float(k_curr),
                            'D': float(d_curr),
                            'J': float(j_curr) if pd.notna(j_curr) else None
                        }
                    })
                
                # KDJ超卖
                elif k_curr < 20 and d_curr < 20:
                    signals.append({
                        'date': date,
                        'type': 'buy',
                        'indicator': 'KDJ',
                        'name': 'KDJ超卖',
                        'description': f'KDJ进入超卖区域（K={k_curr:.1f}, D={d_curr:.1f}），可能反弹',
                        'strength': 3,
                        'price': float(recent_data.loc[idx, '收盘']) if '收盘' in recent_data.columns else None,
                        'details': {
                            'K': float(k_curr),
                            'D': float(d_curr),
                            'J': float(j_curr) if pd.notna(j_curr) else None
                        }
                    })
                
                # KDJ超买
                elif k_curr > 80 and d_curr > 80:
                    signals.append({
                        'date': date,
                        'type': 'sell',
                        'indicator': 'KDJ',
                        'name': 'KDJ超买',
                        'description': f'KDJ进入超买区域（K={k_curr:.1f}, D={d_curr:.1f}），可能回调',
                        'strength': 3,
                        'price': float(recent_data.loc[idx, '收盘']) if '收盘' in recent_data.columns else None,
                        'details': {
                            'K': float(k_curr),
                            'D': float(d_curr),
                            'J': float(j_curr) if pd.notna(j_curr) else None
                        }
                    })
        
        # 3. RSI信号检测
        if 'RSI6' in recent_data.columns:
            rsi_curr = recent_data.loc[idx, 'RSI6']
            rsi_prev = recent_data.loc[prev_idx, 'RSI6']
            
            if pd.notna(rsi_curr) and pd.notna(rsi_prev):
                # RSI超卖
                if rsi_prev > 30 and rsi_curr <= 30:
                    signals.append({
                        'date': date,
                        'type': 'buy',
                        'indicator': 'RSI',
                        'name': 'RSI超卖',
                        'description': f'RSI进入超卖区域（RSI={rsi_curr:.1f}），市场可能超跌',
                        'strength': 4,
                        'price': float(recent_data.loc[idx, '收盘']) if '收盘' in recent_data.columns else None,
                        'details': {
                            'RSI6': float(rsi_curr),
                            'RSI12': float(recent_data.loc[idx, 'RSI12']) if 'RSI12' in recent_data.columns and pd.notna(recent_data.loc[idx, 'RSI12']) else None
                        }
                    })
                
                # RSI超买
                elif rsi_prev < 70 and rsi_curr >= 70:
                    signals.append({
                        'date': date,
                        'type': 'sell',
                        'indicator': 'RSI',
                        'name': 'RSI超买',
                        'description': f'RSI进入超买区域（RSI={rsi_curr:.1f}），市场可能过热',
                        'strength': 4,
                        'price': float(recent_data.loc[idx, '收盘']) if '收盘' in recent_data.columns else None,
                        'details': {
                            'RSI6': float(rsi_curr),
                            'RSI12': float(recent_data.loc[idx, 'RSI12']) if 'RSI12' in recent_data.columns and pd.notna(recent_data.loc[idx, 'RSI12']) else None
                        }
                    })
        
        # 4. MA均线信号检测
        if 'MA5' in recent_data.columns and 'MA10' in recent_data.columns:
            ma5_curr = recent_data.loc[idx, 'MA5']
            ma5_prev = recent_data.loc[prev_idx, 'MA5']
            ma10_curr = recent_data.loc[idx, 'MA10']
            ma10_prev = recent_data.loc[prev_idx, 'MA10']
            
            if pd.notna(ma5_curr) and pd.notna(ma5_prev) and pd.notna(ma10_curr) and pd.notna(ma10_prev):
                # MA5上穿MA10（金叉）
                if ma5_prev < ma10_prev and ma5_curr > ma10_curr:
                    signals.append({
                        'date': date,
                        'type': 'buy',
                        'indicator': 'MA',
                        'name': 'MA金叉',
                        'description': f'MA5上穿MA10，短期趋势转强',
                        'strength': 4,
                        'price': float(recent_data.loc[idx, '收盘']) if '收盘' in recent_data.columns else None,
                        'details': {
                            'MA5': float(ma5_curr),
                            'MA10': float(ma10_curr),
                            'MA20': float(recent_data.loc[idx, 'MA20']) if 'MA20' in recent_data.columns and pd.notna(recent_data.loc[idx, 'MA20']) else None
                        }
                    })
                
                # MA5下穿MA10（死叉）
                elif ma5_prev > ma10_prev and ma5_curr < ma10_curr:
                    signals.append({
                        'date': date,
                        'type': 'sell',
                        'indicator': 'MA',
                        'name': 'MA死叉',
                        'description': f'MA5下穿MA10，短期趋势转弱',
                        'strength': 4,
                        'price': float(recent_data.loc[idx, '收盘']) if '收盘' in recent_data.columns else None,
                        'details': {
                            'MA5': float(ma5_curr),
                            'MA10': float(ma10_curr),
                            'MA20': float(recent_data.loc[idx, 'MA20']) if 'MA20' in recent_data.columns and pd.notna(recent_data.loc[idx, 'MA20']) else None
                        }
                    })
        
        # 5. 布林带信号检测
        if all(col in recent_data.columns for col in ['收盘', 'BOLL_UPPER', 'BOLL_LOWER', 'BOLL_MIDDLE']):
            close_curr = recent_data.loc[idx, '收盘']
            close_prev = recent_data.loc[prev_idx, '收盘']
            upper = recent_data.loc[idx, 'BOLL_UPPER']
            lower = recent_data.loc[idx, 'BOLL_LOWER']
            middle = recent_data.loc[idx, 'BOLL_MIDDLE']
            
            if all(pd.notna(v) for v in [close_curr, close_prev, upper, lower, middle]):
                # 触及下轨反弹
                if close_prev <= lower and close_curr > lower:
                    signals.append({
                        'date': date,
                        'type': 'buy',
                        'indicator': 'BOLL',
                        'name': '布林下轨反弹',
                        'description': f'价格触及布林下轨后反弹，可能止跌',
                        'strength': 3,
                        'price': float(close_curr),
                        'details': {
                            'close': float(close_curr),
                            'lower': float(lower),
                            'middle': float(middle),
                            'upper': float(upper)
                        }
                    })
                
                # 触及上轨回落
                elif close_prev >= upper and close_curr < upper:
                    signals.append({
                        'date': date,
                        'type': 'sell',
                        'indicator': 'BOLL',
                        'name': '布林上轨回落',
                        'description': f'价格触及布林上轨后回落，可能调整',
                        'strength': 3,
                        'price': float(close_curr),
                        'details': {
                            'close': float(close_curr),
                            'lower': float(lower),
                            'middle': float(middle),
                            'upper': float(upper)
                        }
                    })
        
        # 6. 成交量突破信号
        if 'VOL_MA5' in recent_data.columns and '成交量' in recent_data.columns:
            vol_curr = recent_data.loc[idx, '成交量']
            vol_ma5 = recent_data.loc[idx, 'VOL_MA5']
            close_curr = recent_data.loc[idx, '收盘']
            close_prev = recent_data.loc[prev_idx, '收盘']
            
            if all(pd.notna(v) for v in [vol_curr, vol_ma5, close_curr, close_prev]):
                # 放量上涨
                if vol_curr > vol_ma5 * 1.5 and close_curr > close_prev:
                    signals.append({
                        'date': date,
                        'type': 'buy',
                        'indicator': 'VOL',
                        'name': '放量上涨',
                        'description': f'成交量放大1.5倍以上配合价格上涨，买盘积极',
                        'strength': 4,
                        'price': float(close_curr),
                        'details': {
                            'volume': float(vol_curr),
                            'vol_ma5': float(vol_ma5),
                            'ratio': float(vol_curr / vol_ma5)
                        }
                    })
                
                # 放量下跌
                elif vol_curr > vol_ma5 * 1.5 and close_curr < close_prev:
                    signals.append({
                        'date': date,
                        'type': 'sell',
                        'indicator': 'VOL',
                        'name': '放量下跌',
                        'description': f'成交量放大1.5倍以上配合价格下跌，抛压沉重',
                        'strength': 4,
                        'price': float(close_curr),
                        'details': {
                            'volume': float(vol_curr),
                            'vol_ma5': float(vol_ma5),
                            'ratio': float(vol_curr / vol_ma5)
                        }
                    })
    
    # 按日期降序排列（最新的在前面）
    signals.sort(key=lambda x: x['date'], reverse=True)
    
    return signals


def generate_trading_advice(signals: List[Dict[str, Any]], 
                            recent_data: pd.DataFrame) -> Dict[str, Any]:
    """生成交易建议
    
    Args:
        signals: 检测到的信号列表
        recent_data: 最近的行情数据
    
    Returns:
        包含综合评分和建议的字典
    """
    if not signals:
        return {
            'signal_type': 'neutral',
            'score': 50,
            'rating': '中性',
            'advice': '暂无明显买卖信号',
            'reasons': [],
            'stop_loss': None,
            'target_price': None
        }
    
    # 计算最近3天的信号得分
    recent_signals = [s for s in signals if len(signals) <= 3 or signals.index(s) < 3]
    
    buy_score = sum(s['strength'] for s in recent_signals if s['type'] == 'buy')
    sell_score = sum(s['strength'] for s in recent_signals if s['type'] == 'sell')
    
    # 综合评分 (0-100)
    total_strength = buy_score + sell_score
    if total_strength == 0:
        score = 50
        signal_type = 'neutral'
    else:
        # 买入信号占比转换为0-100分
        score = int((buy_score / total_strength) * 100)
        
        if score >= 70:
            signal_type = 'strong_buy'
        elif score >= 55:
            signal_type = 'buy'
        elif score >= 45:
            signal_type = 'neutral'
        elif score >= 30:
            signal_type = 'sell'
        else:
            signal_type = 'strong_sell'
    
    # 评级文字
    rating_map = {
        'strong_buy': '强烈买入',
        'buy': '买入',
        'neutral': '中性',
        'sell': '卖出',
        'strong_sell': '强烈卖出'
    }
    rating = rating_map.get(signal_type, '中性')
    
    # 生成建议理由
    reasons = []
    for signal in recent_signals[:5]:  # 最多列出5个理由
        reasons.append(f"{signal['name']}：{signal['description']}")
    
    # 生成操作建议
    if signal_type in ['strong_buy', 'buy']:
        advice = '当前多个指标显示买入信号，可考虑逢低布局，建议分批建仓，控制仓位。'
        # 计算止损价和目标价
        if len(recent_data) > 0:
            current_price = float(recent_data['收盘'].iloc[-1])
            stop_loss = round(current_price * 0.95, 2)  # 5%止损
            target_price = round(current_price * 1.1, 2)  # 10%目标
        else:
            stop_loss = None
            target_price = None
    elif signal_type in ['strong_sell', 'sell']:
        advice = '当前多个指标显示卖出信号，建议谨慎操作，持仓者可考虑逢高减仓。'
        if len(recent_data) > 0:
            current_price = float(recent_data['收盘'].iloc[-1])
            stop_loss = round(current_price * 1.03, 2)  # 3%止损
            target_price = round(current_price * 0.92, 2)  # 8%目标
        else:
            stop_loss = None
            target_price = None
    else:
        advice = '当前信号不明确，建议保持观望，等待更明确的信号。'
        stop_loss = None
        target_price = None
    
    return {
        'signal_type': signal_type,
        'score': score,
        'rating': rating,
        'advice': advice,
        'reasons': reasons,
        'stop_loss': stop_loss,
        'target_price': target_price,
        'buy_signals': len([s for s in recent_signals if s['type'] == 'buy']),
        'sell_signals': len([s for s in recent_signals if s['type'] == 'sell'])
    }
