import akshare as ak
import pandas as pd

def test_trade_date_interface():
    """
    独立测试 ak.tool_trade_date_hist_sina() 接口。
    """
    print("正在调用 ak.tool_trade_date_hist_sina() 来获取交易日历...")
    
    try:
        # 1. 直接调用接口
        trade_dates_df = ak.tool_trade_date_hist_sina()
        
        print("\n--------- 接口原始返回数据 (前5条) ---------")
        print(trade_dates_df.head())
        print("--------------------------------------------")

        # 2. 检查返回数据是否为空
        if trade_dates_df is None or trade_dates_df.empty:
            print("\n[失败] 接口返回了 None 或空的数据框。")
            return

        # 3. 模拟项目中的日期格式转换操作
        print("\n正在尝试将日期列转换为 'YYYYMMDD' 格式...")
        trade_dates_df['trade_date_formatted'] = pd.to_datetime(trade_dates_df['trade_date']).dt.strftime('%Y%m%d')
        
        print("\n--------- 格式转换后数据 (前5条) ---------")
        print(trade_dates_df.head())
        print("--------------------------------------------")
        
        print("\n[成功] 获取并处理交易日历数据成功！")

    except Exception as e:
        print(f"\n[失败] 在调用或处理过程中发生严重错误: {e}")
        print("请检查您的网络连接或 akshare 库状态。")

if __name__ == "__main__":
    test_trade_date_interface()
