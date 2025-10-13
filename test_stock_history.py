import akshare as ak
from datetime import datetime, timedelta

def test_get_stock_history(code: str):
    """
    测试获取指定股票代码的日度历史行情数据。
    使用腾讯财经接口。
    默认查询过去一年的数据。
    """
    print(f"\n正在测试获取股票代码 {code} 的历史行情 (使用腾讯财经接口)...")
    
    # 设置查询的日期范围为过去一年
    end_date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
    
    print(f"查询参数: 股票代码='{code}', 开始日期='{start_date}', 结束日期='{end_date}'")

    try:
        # 更换为腾讯财经的接口: stock_zh_a_hist_tx
        stock_zh_a_hist_df = ak.stock_zh_a_hist_tx(
            symbol=code, 
            start_date=start_date, 
            end_date=end_date, 
            adjust="qfq"  # 前复权
        )
        
        if stock_zh_a_hist_df is not None and not stock_zh_a_hist_df.empty:
            print(f"成功获取到股票 {code} 的历史数据！")
            print("-------------------- 数据预览 (前5条) --------------------")
            print(stock_zh_a_hist_df.head())
            print("---------------------------------------------------------")
            print(f"总共获取到 {len(stock_zh_a_hist_df)} 条记录。")
            print("测试成功！这表明 akshare 的腾讯财经接口可以正常工作。")
        else:
            print("未能获取到任何数据。可能原因：")
            print("1. 股票代码不正确或已退市。")
            print("2. 指定日期范围内没有交易数据。")
            print("3. 网络问题或 akshare 接口暂时不可用。")

    except Exception as e:
        print(f"获取股票 {code} 数据时发生严重错误: {e}")
        print("请检查您的网络连接以及 akshare 是否为最新版本。")

if __name__ == "__main__":
    # --- 使用说明 ---
    # 1. 请确保您已经激活了正确的 Python 环境 (conda activate financial_analysis)
    # 2. 在下方输入您想要测试的股票代码
    test_stock_code = "000001"  # 平安银行
    # test_stock_code = "600519"  # 贵州茅台
    
    test_get_stock_history(test_stock_code)
