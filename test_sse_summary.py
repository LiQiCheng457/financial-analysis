import akshare as ak
from datetime import datetime, timedelta
import argparse

def test_get_sse_daily_summary(date_str: str):
    """
    测试获取上海证券交易所-每日概况。
    :param date_str: 指定查询的日期，格式为 "YYYYMMDD"
    """
    print(f"正在测试获取上海证券交易所 {date_str} 的每日概况...")
    
    try:
        summary_df = ak.stock_sse_deal_daily(date=date_str)
        
        # 检查返回的 DataFrame 是否有效
        if summary_df is not None and not summary_df.empty:
            print(f"成功获取到 {date_str} 的数据！")
            print("-------------------- 数据如下 --------------------")
            print(summary_df)
            print("--------------------------------------------------")
            print("测试成功！")
        else:
            # akshare 在非交易日或无数据时，有时返回空 DataFrame，有时返回 None
            print(f"未能获取到 {date_str} 的数据。这很可能是因为当天是非交易日。")

    except Exception as e:
        # 捕获并打印其他可能的错误，例如网络问题或 akshare 内部错误
        print(f"获取 {date_str} 数据时发生错误: {e}")
        print("请检查您的网络连接以及 akshare 库是否为最新版本。")

if __name__ == "__main__":
    # --- 使用 argparse 来接收命令行参数 ---
    parser = argparse.ArgumentParser(description="测试获取上交所每日概况。")
    # 添加一个可选的 -d 或 --date 参数
    parser.add_argument(
        "-d", "--date", 
        type=str, 
        help='指定查询日期，格式为 "YYYYMMDD"。如果未提供，则默认为昨天。'
    )
    args = parser.parse_args()

    # --- 决定使用哪个日期 ---
    if args.date:
        # 如果用户通过命令行提供了日期
        target_date_str = args.date
    else:
        # 否则，默认使用昨天的日期
        yesterday = datetime.now() - timedelta(days=1)
        target_date_str = yesterday.strftime("%Y%m%d")
        print(f"未指定日期，将默认查询昨天的日期: {target_date_str}")

    # 执行测试函数
    test_get_sse_daily_summary(target_date_str)

