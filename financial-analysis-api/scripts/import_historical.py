from datetime import datetime, timedelta
import time
import os
import pymysql
import pandas as pd


class StockDailyDataDB:
    def __init__(self, host='localhost', user='root', password='lqc20050413ab', database='financial_analysis_db', charset='utf8mb4'):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset=charset,
            cursorclass=pymysql.cursors.DictCursor
        )

    def close(self):
        if self.connection:
            self.connection.close()

    def test_connection(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            print("✓ 数据库连接成功")
            return True
        except Exception as e:
            print(f"✗ 数据库连接失败: {e}")
            return False

    def create_table_if_not_exists(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS stock_daily_data (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        stock_code VARCHAR(20) NOT NULL,
                        trade_date DATE NOT NULL,
                        open_price DECIMAL(10,4),
                        high_price DECIMAL(10,4),
                        low_price DECIMAL(10,4),
                        close_price DECIMAL(10,4),
                        pre_close DECIMAL(10,4),
                        change_amount DECIMAL(10,4),
                        pct_chg DECIMAL(8,4),
                        volume BIGINT,
                        amount DECIMAL(15,2),
                        created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        UNIQUE KEY uk_stock_date (stock_code, trade_date),
                        INDEX idx_stock_code (stock_code),
                        INDEX idx_trade_date (trade_date)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)
                self.connection.commit()
                print("✓ 历史行情数据表检查/创建完成")
                return True
        except Exception as e:
            print(f"✗ 创建历史行情数据表失败: {e}")
            return False

    def insert_or_update_daily_data(self, df: pd.DataFrame, tushare_ts_code: str):
        try:
            with self.connection.cursor() as cursor:
                success_count = 0
                clean_stock_code = self.clean_stock_code(tushare_ts_code)
                for _, row in df.iterrows():
                    try:
                        trade_date = row.get('trade_date')
                        if isinstance(trade_date, str) and len(trade_date) == 8:
                            formatted_date = f"{trade_date[:4]}-{trade_date[4:6]}-{trade_date[6:8]}"
                        else:
                            formatted_date = trade_date

                        sql = """
                            INSERT INTO stock_daily_data (stock_code, trade_date, open_price, high_price, low_price, close_price, pre_close, change_amount, pct_chg, volume, amount)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            ON DUPLICATE KEY UPDATE open_price=VALUES(open_price), high_price=VALUES(high_price), low_price=VALUES(low_price), close_price=VALUES(close_price), pre_close=VALUES(pre_close), change_amount=VALUES(change_amount), pct_chg=VALUES(pct_chg), volume=VALUES(volume), amount=VALUES(amount), updated_time=CURRENT_TIMESTAMP
                        """
                        cursor.execute(sql, (
                            clean_stock_code,
                            formatted_date,
                            row.get('open'),
                            row.get('high'),
                            row.get('low'),
                            row.get('close'),
                            row.get('pre_close'),
                            row.get('change'),
                            row.get('pct_chg'),
                            int(row.get('vol')) if pd.notna(row.get('vol')) else None,
                            float(row.get('amount')) if pd.notna(row.get('amount')) else None
                        ))
                        success_count += 1
                    except Exception:
                        continue
                self.connection.commit()
                return success_count
        except Exception as e:
            print(f"✗ 批量插入数据失败: {e}")
            self.connection.rollback()
            return 0

    def clean_stock_code(self, ts_code: str) -> str:
        if ts_code.endswith('.SZ'):
            return 'SZ' + ts_code.replace('.SZ', '')
        elif ts_code.endswith('.SH'):
            return 'SH' + ts_code.replace('.SH', '')
        else:
            return ts_code


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Import historical OHLCV data into stock_daily_data')
    parser.add_argument('--file', type=str, help='CSV or Excel file path containing daily data')
    parser.add_argument('--ts-code', type=str, help='tushare ts_code like 000001.SZ (optional)')
    args = parser.parse_args()

    if not args.file:
        print('No file provided. Exiting.')
        return

    # read file with pandas
    fn = args.file
    if fn.lower().endswith('.csv'):
        df = pd.read_csv(fn, dtype=str)
    else:
        df = pd.read_excel(fn)

    db = StockDailyDataDB()
    if not db.test_connection():
        print('DB connection failed')
        return

    ok = db.create_table_if_not_exists()
    if not ok:
        print('Ensure table failed')
    # expect DataFrame to have conventional tushare column names like trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount
    ts_code = args.ts_code or ''
    count = db.insert_or_update_daily_data(df, ts_code)
    print(f'Inserted/updated {count} rows')
    db.close()


if __name__ == '__main__':
    main()
