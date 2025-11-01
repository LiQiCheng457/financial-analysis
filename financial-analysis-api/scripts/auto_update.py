import pymysql
import pandas as pd
from datetime import datetime, timedelta
import time
import schedule  # type: ignore[reportMissingImports]
import logging
import sys
from threading import Thread
import os
import argparse
import tushare as ts  # type: ignore[reportMissingImports]
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()


class StockDataAutoUpdater:
    def __init__(self, host: str = None, user: str = None, password: str = None, database: str = None, charset: str = None, tushare_token: str = None):
        """初始化，参数可通过环境变量传入：
        - DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME, DATABASE_CHARSET
        - TUSHARE_TOKEN
        """
        self.db_config = {
            'host': host or os.getenv('DATABASE_HOST', 'localhost'),
            'user': user or os.getenv('DATABASE_USER', 'root'),
            'password': password or os.getenv('DATABASE_PASSWORD', ''),
            'database': database or os.getenv('DATABASE_NAME', 'financial_analysis_db'),
            'charset': charset or os.getenv('DATABASE_CHARSET', 'utf8mb4')
        }
        token = tushare_token or os.getenv('TUSHARE_TOKEN')
        if token:
            try:
                self.pro = ts.pro_api(token)
            except Exception:
                # fallback to default initializer (may raise later if token required)
                self.pro = ts.pro_api()
        else:
            # no token provided; try default
            try:
                self.pro = ts.pro_api()
            except Exception:
                self.pro = None

        # 用于标记是否有交易日历接口权限
        self._has_trade_cal_permission = None
        
        self.setup_logging()

    def setup_logging(self):
        # 确保 logs 目录存在
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, 'stock_data_update.log')
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def get_connection(self):
        try:
            return pymysql.connect(**self.db_config, cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            self.logger.error(f"数据库连接失败: {e}")
            return None

    def convert_to_tushare_format(self, stock_code: str) -> str:
        if stock_code.startswith('SZ'):
            return stock_code.replace('SZ', '') + '.SZ'
        elif stock_code.startswith('SH'):
            return stock_code.replace('SH', '') + '.SH'
        else:
            return stock_code

    def clean_stock_code(self, ts_code: str) -> str:
        if ts_code.endswith('.SZ'):
            return 'SZ' + ts_code.replace('.SZ', '')
        elif ts_code.endswith('.SH'):
            return 'SH' + ts_code.replace('.SH', '')
        else:
            return ts_code

    def get_latest_trade_date(self, stock_code: str):
        """获取某只股票在数据库中最新的交易日期"""
        conn = self.get_connection()
        if not conn:
            return None
        try:
            with conn.cursor() as cursor:
                sql = "SELECT trade_date FROM stock_daily_data WHERE stock_code = %s ORDER BY trade_date DESC LIMIT 1"
                cursor.execute(sql, (stock_code,))
                r = cursor.fetchone()
                return r['trade_date'] if r else None
        except Exception as e:
            self.logger.error(f"获取最新交易日期失败 {stock_code}: {e}")
            return None
        finally:
            conn.close()
    
    def is_trading_day(self, check_date=None):
        """检查指定日期是否是交易日（通过Tushare交易日历）
        
        Args:
            check_date: datetime对象，默认为今天
        
        Returns:
            bool: True表示是交易日，False表示休市
        """
        if check_date is None:
            check_date = datetime.now()
        
        # 周末直接返回False
        if check_date.weekday() >= 5:  # 5=周六, 6=周日
            return False
        
        # 如果已知没有权限，直接使用简单判断
        if self._has_trade_cal_permission is False:
            # 周一到周五为交易日（不考虑节假日）
            return check_date.weekday() < 5
        
        # 从Tushare获取交易日历
        try:
            date_str = check_date.strftime('%Y%m%d')
            # 获取前后10天的交易日历（确保包含目标日期）
            start = (check_date - timedelta(days=10)).strftime('%Y%m%d')
            end = (check_date + timedelta(days=10)).strftime('%Y%m%d')
            
            df = self.pro.trade_cal(exchange='SSE', start_date=start, end_date=end)
            if df is not None and not df.empty:
                # 标记有权限
                if self._has_trade_cal_permission is None:
                    self._has_trade_cal_permission = True
                    self.logger.info("✓ 交易日历接口可用")
                
                # 查找指定日期
                day_info = df[df['cal_date'] == date_str]
                if not day_info.empty:
                    # is_open=1表示交易日，0表示休市
                    return int(day_info.iloc[0]['is_open']) == 1
        except Exception as e:
            # 如果是权限错误，标记为无权限
            if '权限' in str(e) or 'permission' in str(e).lower():
                if self._has_trade_cal_permission is None:
                    self._has_trade_cal_permission = False
                    self.logger.info("ℹ️  交易日历接口无权限，将使用简单日期判断（周一至周五为交易日）")
            else:
                if self._has_trade_cal_permission is None:
                    self.logger.warning(f"获取交易日历失败，使用简单判断: {e}")
        
        # 如果API调用失败，简单判断：周一到周五为交易日
        return check_date.weekday() < 5

    def get_latest_trading_day(self):
        """获取最近的交易日（包括今天，如果今天是交易日）
        
        Returns:
            datetime: 最近的交易日日期
        """
        # 如果已知没有权限，直接使用简单逻辑
        if self._has_trade_cal_permission is False:
            check_date = datetime.now()
            while check_date.weekday() >= 5:  # 如果是周末，往前推
                check_date -= timedelta(days=1)
            return check_date
        
        try:
            # 获取最近30天的交易日历
            end_date = datetime.now().strftime('%Y%m%d')
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            
            df = self.pro.trade_cal(exchange='SSE', start_date=start_date, end_date=end_date)
            if df is not None and not df.empty:
                # 标记有权限
                if self._has_trade_cal_permission is None:
                    self._has_trade_cal_permission = True
                    self.logger.info("✓ 交易日历接口可用")
                
                # 筛选出交易日，并按日期降序排列
                trading_days = df[df['is_open'] == 1].sort_values('cal_date', ascending=False)
                if not trading_days.empty:
                    latest_date_str = trading_days.iloc[0]['cal_date']
                    return datetime.strptime(latest_date_str, '%Y%m%d')
        except Exception as e:
            # 如果是权限错误，标记为无权限
            if '权限' in str(e) or 'permission' in str(e).lower():
                if self._has_trade_cal_permission is None:
                    self._has_trade_cal_permission = False
                    self.logger.info("ℹ️  交易日历接口无权限，将使用简单日期判断（周一至周五为交易日）")
            else:
                # 其他错误才打印警告
                if self._has_trade_cal_permission is None:
                    self.logger.warning(f"获取最近交易日失败: {e}")
        
        # 如果API失败或无权限，使用简单逻辑：从今天往前找，跳过周末
        check_date = datetime.now()
        while check_date.weekday() >= 5:  # 如果是周末，往前推
            check_date -= timedelta(days=1)
        return check_date

    def insert_daily_data(self, df: pd.DataFrame, tushare_ts_code: str):
        conn = self.get_connection()
        if not conn:
            return 0
        try:
            with conn.cursor() as cursor:
                success = 0
                clean_code = self.clean_stock_code(tushare_ts_code)
                for _, row in df.iterrows():
                    try:
                        trade_date = row['trade_date']
                        formatted_date = f"{trade_date[:4]}-{trade_date[4:6]}-{trade_date[6:8]}" if isinstance(trade_date, str) and len(trade_date) == 8 else trade_date
                        sql = """
                            INSERT IGNORE INTO stock_daily_data (stock_code, trade_date, open_price, high_price, low_price, close_price, pre_close, change_amount, pct_chg, volume, amount)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """
                        cursor.execute(sql, (
                            clean_code,
                            formatted_date,
                            row.get('open'), row.get('high'), row.get('low'), row.get('close'), row.get('pre_close'), row.get('change'), row.get('pct_chg'), int(row.get('vol')) if pd.notna(row.get('vol')) else None, float(row.get('amount')) if pd.notna(row.get('amount')) else None
                        ))
                        success += 1
                    except Exception:
                        continue
                conn.commit()
                return success
        except Exception as e:
            self.logger.error(f"插入数据失败: {e}")
            conn.rollback()
            return 0
        finally:
            conn.close()

    def update_single_stock_data(self, stock_code: str, check_latest=True):
        """更新单只股票的数据（从数据库最新日期的下一天开始）
        
        Args:
            stock_code: 股票代码（格式：SZ000001或SH600000）
            check_latest: 是否检查并跳过已是最新的股票，默认True
        
        Returns:
            int: 成功插入的记录条数，0表示无新数据或已是最新，-1表示失败
        """
        try:
            # 获取数据库中该股票的最新日期
            latest_date = self.get_latest_trade_date(stock_code)
            
            # 获取最近的交易日
            latest_trading_day = self.get_latest_trading_day()
            
            if latest_date:
                # 如果启用了智能检查，且数据已是最新，直接跳过
                if check_latest and latest_date >= latest_trading_day.date():
                    self.logger.debug(f"{stock_code}: 数据已是最新（{latest_date}），跳过更新")
                    return 0
                
                # 从最新日期的下一天开始更新
                start_dt = latest_date + timedelta(days=1)
                start_str = start_dt.strftime('%Y%m%d')
                
                # 如果最新日期已是今天或更晚，无需更新
                today_str = datetime.now().strftime('%Y%m%d')
                if start_str > today_str:
                    self.logger.debug(f"{stock_code}: 数据已是最新，无需更新")
                    return 0
            else:
                # 如果数据库中无数据，从2015年开始（Tushare推荐的起始日期）
                start_str = '20150101'
                self.logger.info(f"{stock_code}: 首次导入数据，起始日期 {start_str}")
            
            # 结束日期为今天
            end_str = datetime.now().strftime('%Y%m%d')
            
            # 转换为Tushare格式（000001.SZ 或 600000.SH）
            tushare_code = self.convert_to_tushare_format(stock_code)
            
            self.logger.info(f"{stock_code}: 获取 {start_str} 至 {end_str} 的数据")
            
            # 从Tushare获取日线数据（未复权）
            df = self.pro.daily(ts_code=tushare_code, start_date=start_str, end_date=end_str)
            
            if df is None or df.empty:
                self.logger.debug(f"{stock_code}: 无新数据或停牌")
                return 0
            
            # 插入数据库
            success_count = self.insert_daily_data(df, tushare_code)
            
            if success_count > 0:
                self.logger.info(f"{stock_code}: 成功更新 {success_count} 条记录")
            
            return success_count
            
        except Exception as e:
            self.logger.error(f"{stock_code}: 更新失败 - {e}")
            return -1

    def batch_update_stocks_data(self, stock_codes=None, delay_seconds=1.5, smart_skip=True):
        """批量更新股票数据（所有4500+只股票）
        
        Args:
            stock_codes: 股票代码列表，None表示更新所有股票
            delay_seconds: 每次请求间隔（秒），默认1.5秒（每分钟40次，避免触发限制）
            smart_skip: 是否智能跳过已更新到最新的股票，默认True
        
        Returns:
            dict: 更新结果统计
        """
        # 获取最近的交易日
        latest_trading_day = self.get_latest_trading_day()
        latest_trading_day_str = latest_trading_day.strftime('%Y-%m-%d')
        
        self.logger.info(f"最近的交易日: {latest_trading_day_str}")
        
        # 检查数据库中是否已有最新数据
        conn = self.get_connection()
        if not conn:
            self.logger.error("无法连接数据库")
            return None
        
        needs_update = False
        try:
            with conn.cursor() as cursor:
                # 直接统计需要更新的股票数（无论当前最大日期是多少）
                cursor.execute("""
                    SELECT COUNT(*) as need_update_count
                    FROM stock_basic_info sbi
                    LEFT JOIN (
                        SELECT stock_code, MAX(trade_date) as latest_date
                        FROM stock_daily_data
                        GROUP BY stock_code
                    ) sdd ON sbi.stock_code = sdd.stock_code
                    WHERE sdd.latest_date IS NULL OR sdd.latest_date < %s
                """, (latest_trading_day.date(),))
                need_update_result = cursor.fetchone()
                need_update_count = need_update_result['need_update_count'] if need_update_result else 0
                
                if need_update_count > 0:
                    self.logger.info(f"有 {need_update_count} 只股票需要更新至 {latest_trading_day_str}")
                    needs_update = True
                else:
                    self.logger.info(f"所有股票已更新到最新（{latest_trading_day_str}），无需更新")
                    needs_update = False
        except Exception as e:
            self.logger.error(f"检查数据库状态失败: {e}")
            needs_update = True  # 出错时尝试更新
        finally:
            conn.close()
        
        # 如果不需要更新，直接返回
        if not needs_update:
            return {
                'is_trading_day': self.is_trading_day(),
                'needs_update': False,
                'total_stocks': 0,
                'success': 0,
                'failed': 0,
                'updated_records': 0,
                'skipped': 0,
                'elapsed_time': 0,
                'message': '数据已是最新，无需更新'
            }
        
        self.logger.info("开始更新股票数据...")
        
        # 如果未指定股票列表，从数据库获取股票
        if stock_codes is None:
            conn = self.get_connection()
            if not conn:
                self.logger.error("无法连接数据库")
                return None
            try:
                with conn.cursor() as cursor:
                    if smart_skip:
                        # 智能模式：只获取需要更新的股票，并按优先级排序
                        # 优先级：1. 无数据的股票（首次导入）
                        #        2. 数据过时的股票（按日期从早到晚）
                        self.logger.info("🎯 启用智能更新模式：只更新需要的股票，跳过已是最新的股票")
                        cursor.execute("""
                            SELECT sbi.stock_code,
                                   sdd.latest_date,
                                   CASE 
                                       WHEN sdd.latest_date IS NULL THEN 0
                                       ELSE DATEDIFF(%s, sdd.latest_date)
                                   END as days_behind
                            FROM stock_basic_info sbi
                            LEFT JOIN (
                                SELECT stock_code, MAX(trade_date) as latest_date
                                FROM stock_daily_data
                                GROUP BY stock_code
                            ) sdd ON sbi.stock_code = sdd.stock_code
                            WHERE sdd.latest_date IS NULL OR sdd.latest_date < %s
                            ORDER BY 
                                CASE WHEN sdd.latest_date IS NULL THEN 0 ELSE 1 END,
                                sdd.latest_date ASC,
                                sbi.stock_code
                        """, (latest_trading_day.date(), latest_trading_day.date()))
                        rows = cursor.fetchall()
                        stock_codes = [r['stock_code'] for r in rows]
                        
                        # 统计信息
                        no_data_count = sum(1 for r in rows if r['latest_date'] is None)
                        outdated_count = len(rows) - no_data_count
                        
                        self.logger.info(f"📊 需要更新的股票: {len(stock_codes)} 只")
                        if no_data_count > 0:
                            self.logger.info(f"   ├─ 无数据（首次导入）: {no_data_count} 只")
                        if outdated_count > 0:
                            self.logger.info(f"   └─ 数据过时: {outdated_count} 只")
                        
                        # 显示几个例子
                        if len(rows) > 0:
                            self.logger.info("📝 更新队列前5只股票:")
                            for i, r in enumerate(rows[:5], 1):
                                if r['latest_date'] is None:
                                    self.logger.info(f"   {i}. {r['stock_code']}: 无数据，将从2015年开始导入")
                                else:
                                    self.logger.info(f"   {i}. {r['stock_code']}: 最新日期 {r['latest_date']}, 落后 {r['days_behind']} 天")
                    else:
                        # 普通模式：获取所有股票
                        cursor.execute("SELECT stock_code FROM stock_basic_info ORDER BY stock_code")
                        rows = cursor.fetchall()
                        stock_codes = [r['stock_code'] for r in rows]
                        self.logger.info(f"从数据库获取到 {len(stock_codes)} 只股票")
            finally:
                conn.close()
        
        total = len(stock_codes)
        results = {
            'is_trading_day': self.is_trading_day(),
            'needs_update': True,
            'total_stocks': total,
            'success': 0,
            'failed': 0,
            'updated_records': 0,
            'skipped': 0,
            'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.logger.info(f"=" * 60)
        self.logger.info(f"开始批量更新 {total} 只股票的历史行情数据")
        self.logger.info(f"=" * 60)
        
        start_time = time.time()
        
        for i, stock_code in enumerate(stock_codes, 1):
            try:
                # 显示进度
                if i % 100 == 0 or i == total:
                    elapsed = time.time() - start_time
                    avg_time = elapsed / i
                    eta = avg_time * (total - i)
                    self.logger.info(
                        f"进度: {i}/{total} ({i/total*100:.1f}%) | "
                        f"成功: {results['success']} | "
                        f"失败: {results['failed']} | "
                        f"跳过: {results['skipped']} | "
                        f"新增: {results['updated_records']} 条 | "
                        f"预计剩余: {eta/60:.1f}分钟"
                    )
                
                # 更新单只股票（check_latest=False，因为已经在SQL查询中过滤过了）
                added = self.update_single_stock_data(stock_code, check_latest=False)
                
                if added > 0:
                    results['success'] += 1
                    results['updated_records'] += added
                elif added == 0:
                    # 无新数据或已是最新
                    results['skipped'] += 1
                elif added == -1:
                    # 更新失败
                    results['failed'] += 1
                
                # 添加延迟，避免触发Tushare频率限制
                # 基础积分：每分钟500次，约0.12秒/次
                time.sleep(delay_seconds)
                
            except Exception as e:
                results['failed'] += 1
                self.logger.error(f"{stock_code}: 处理异常 - {e}")
                # 出错后增加延迟
                time.sleep(delay_seconds * 2)
                continue
        
        # 计算总耗时
        elapsed_time = time.time() - start_time
        results['elapsed_time'] = elapsed_time
        results['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 输出汇总
        self.logger.info(f"=" * 60)
        self.logger.info(f"批量更新完成")
        self.logger.info(f"=" * 60)
        self.logger.info(f"总股票数: {total}")
        self.logger.info(f"成功更新: {results['success']} 只")
        self.logger.info(f"失败: {results['failed']} 只")
        self.logger.info(f"跳过（无新数据）: {results['skipped']} 只")
        self.logger.info(f"新增记录: {results['updated_records']} 条")
        self.logger.info(f"总耗时: {elapsed_time/60:.1f} 分钟")
        self.logger.info(f"平均速度: {elapsed_time/total:.2f} 秒/只")
        
        return results

    def run_scheduled_task(self, at_time: str = "20:00"):
        """Run a scheduler loop that executes daily update at `at_time` (HH:MM).

        This method blocks while running the schedule loop; call it in a background thread.
        """
        try:
            schedule.clear()
            # schedule the job
            schedule.every().day.at(at_time).do(lambda: self.batch_update_stocks_data())
            self.logger.info(f"Auto-updater scheduled daily at {at_time}")
            while True:
                schedule.run_pending()
                time.sleep(30)
        except Exception as e:
            self.logger.error(f"Scheduler loop stopped: {e}")

    def start_background_scheduler(self, at_time: str = "20:00"):
        """Start the scheduler in a daemon background thread and return the Thread object."""
        t = Thread(target=self.run_scheduled_task, args=(at_time,), daemon=True)
        t.start()
        return t


def main():
    parser = argparse.ArgumentParser(description='Stock data auto updater')
    parser.add_argument('--run-scheduler', action='store_true', help='Run scheduler loop (blocking)')
    parser.add_argument('--run-once', action='store_true', help='Run one update cycle and exit')
    parser.add_argument('--stock', type=str, help='Update single stock (e.g., SH600000)')
    parser.add_argument('--time', type=str, default=os.getenv('AUTO_UPDATE_TIME', '20:00'), help='Scheduler time HH:MM')
    parser.add_argument('--no-smart-skip', action='store_true', help='Disable smart skip (update all stocks)')
    args = parser.parse_args()

    updater = StockDataAutoUpdater()

    if args.stock:
        print(f'Updating single stock: {args.stock}...')
        added = updater.update_single_stock_data(args.stock)
        if added > 0:
            print(f'✅ Successfully updated {added} records')
        elif added == 0:
            print('ℹ️  Stock is already up to date, no new data')
        else:
            print('❌ Update failed, please check logs')
        return

    if args.run_once:
        print('Running one update cycle...')
        smart_skip = not args.no_smart_skip
        if smart_skip:
            print('🎯 Smart skip enabled: Only outdated stocks will be updated')
        else:
            print('⚠️  Smart skip disabled: All stocks will be processed')
        res = updater.batch_update_stocks_data(smart_skip=smart_skip)
        print('Update result:', res)
        return

    if args.run_scheduler:
        print(f'Starting scheduler loop at {args.time} ...')
        updater.run_scheduled_task(at_time=args.time)
        return

    print('auto_update: no action specified. Use --run-once, --run-scheduler, or --stock')
    print('Hint: Use --no-smart-skip to disable smart update mode')


if __name__ == '__main__':
    main()
