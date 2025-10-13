import akshare as ak
import pandas as pd
import argparse
import numpy as np
from typing import List


def get_trade_dates_list() -> List[str]:
    """从 akshare 获取交易日历并返回 YYYYMMDD 格式的字符串列表。"""
    try:
        df = ak.tool_trade_date_hist_sina()
        if df is None or df.empty:
            return []
        df['trade_date'] = pd.to_datetime(df['trade_date']).dt.strftime('%Y%m%d')
        return df['trade_date'].tolist()
    except Exception as e:
        print(f"获取交易日历失败: {e}")
        return []


def final_test_summary(date_str: str):
    """
    1) 判断输入日期是否为交易日（使用 tool_trade_date_hist_sina），
    2) 若为交易日则调用 ak.stock_sse_deal_daily 获取数据并清洗（NaN -> None），打印清洗后的记录；
    3) 若为休市日则直接打印提示信息。
    """
    print(f"--- 测试查询：{date_str} ---")

    # 获取交易日历
    trade_dates = get_trade_dates_list()
    if not trade_dates:
        print("[错误] 无法获取交易日历，无法判断是否为交易日。")
        return

    if date_str not in trade_dates:
        print(f"{date_str} 为休市日，未进行数据请求。")
        return

    # 是交易日，获取每日概况
    try:
        df = ak.stock_sse_deal_daily(date=date_str)
        if df is None or df.empty:
            print(f"{date_str} 查询返回空数据（可能为当日尚未统计完毕）。")
            return

        # 将 NaN 替换为 None，确保可打印与后端兼容
        cleaned = df.replace({np.nan: None})

        print(f"{date_str} 的每日概况（清洗后）：")
        # 打印为列表形式，便于前端模拟输出
        records = cleaned.to_dict(orient='records')
        for r in records:
            print(r)

    except Exception as e:
        print(f"请求或处理每日概况时发生错误: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='测试每日概况（使用上交所接口和交易日历判断）')
    parser.add_argument('-d', '--date', required=True, help='查询日期，格式 YYYYMMDD')
    args = parser.parse_args()
    final_test_summary(args.date)
