from fastapi import FastAPI, Request, status  # type: ignore[reportMissingImports]
from fastapi.responses import JSONResponse  # type: ignore[reportMissingImports]
from fastapi.exceptions import RequestValidationError  # type: ignore[reportMissingImports]
import uvicorn  # type: ignore[reportMissingImports]
from starlette.middleware.cors import CORSMiddleware  # type: ignore[reportMissingImports]
from app.apis import auth as auth_router
from app.apis import user as user_router
from app.apis import stock as stock_router
from app.apis import vadmin_users as vadmin_users_router
import traceback

from app.core.database import engine, Base
from app.core.database import SessionLocal
from app.services.auth_service import AuthService
import os
from dotenv import load_dotenv
load_dotenv()
# ... (other imports)
from scripts.auto_update import StockDataAutoUpdater

def create_db_and_tables():
    Base.metadata.create_all(bind=engine)

def create_app():
    """
    启动项目
    """
    create_db_and_tables()  # 在应用启动时创建表

    app = FastAPI(
        title="Financial Analysis",
# ... (rest of the file)
        description="金融分析项目",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    # 启动时按环境变量决定是否创建默认管理员账号（仅用于开发/测试）
    @app.on_event("startup")
    def ensure_admin_user():
        # 仅当明确设置 ENABLE_DEFAULT_ADMIN 为 true/1/yes 时才创建默认管理员
        enable_seed = os.getenv('ENABLE_DEFAULT_ADMIN')
        should_seed = bool(enable_seed and enable_seed.lower() in ['1', 'true', 'yes'])

        if not should_seed:
            return

        db = SessionLocal()
        try:
            admin = AuthService.get_user_by_username(db, username='admin')
            if not admin:
                # 使用 AuthService 的 create_user 以便密码哈希一致，并设置 role='admin'
                try:
                    from app.schemas.auth import UserCreate
                    admin_user = UserCreate(username='admin', password='admin123')
                    created = AuthService.create_user(db=db, user=admin_user)
                    try:
                        # 如果模型支持 role 字段，设置为 admin
                        if created and getattr(created, 'role', None) != 'admin':
                            created.role = 'admin'
                            db.add(created)
                            db.commit()
                            db.refresh(created)
                    except Exception:
                        pass
                    print("[startup] 默认管理员 admin 已创建，初始密码: admin123")
                except Exception as e:
                    print("[startup] 创建默认管理员失败:", e)
        finally:
            db.close()

    # 可选：启动自动更新调度（每天固定时间执行）
    @app.on_event("startup")
    def start_auto_update_scheduler():
        try:
            enable_auto = os.getenv('ENABLE_AUTO_UPDATE', '0')
            if str(enable_auto).lower() in ('1', 'true', 'yes'):
                # create updater with DB config read from env if provided
                updater = StockDataAutoUpdater(
                    host=os.getenv('DATABASE_HOST', 'localhost'),
                    user=os.getenv('DATABASE_USER', 'root'),
                    password=os.getenv('DATABASE_PASSWORD', ''),
                    database=os.getenv('DATABASE_NAME', 'financial_analysis_db')
                )
                
                # 可选：服务器启动时立即执行一次更新
                run_on_startup = os.getenv('AUTO_UPDATE_ON_STARTUP', '0')
                if str(run_on_startup).lower() in ('1', 'true', 'yes'):
                    print("=" * 60)
                    print("[启动时更新] 开始执行股票数据更新...")
                    print("[启动时更新] 这将在后台运行，不会阻塞服务启动")
                    print("[启动时更新] 详细日志请查看: logs/stock_data_update.log")
                    print("=" * 60)
                    print()
                    print("💡 提示：可在新的 PowerShell 窗口中运行以下命令实时查看日志：")
                    print("   Get-Content logs\\stock_data_update.log -Encoding UTF8 -Wait")
                    print()
                    
                    # 在后台线程中执行，避免阻塞启动
                    import threading
                    def update_task():
                        try:
                            print("[启动时更新] 后台更新线程已启动...")
                            results = updater.batch_update_stocks_data()
                            if results:
                                if not results.get('needs_update', True):
                                    print(f"[启动时更新] ℹ️  {results.get('message', '数据已是最新')}")
                                elif results.get('total_stocks', 0) > 0:
                                    print("\n" + "=" * 60)
                                    print("[启动时更新] ✅ 更新完成！")
                                    print("=" * 60)
                                    print(f"  总股票数: {results['total_stocks']} 只")
                                    print(f"  成功更新: {results['success']} 只")
                                    print(f"  失败: {results['failed']} 只")
                                    print(f"  跳过: {results['skipped']} 只")
                                    print(f"  新增记录: {results['updated_records']} 条")
                                    print(f"  总耗时: {results['elapsed_time']/60:.1f} 分钟")
                                    print("=" * 60)
                        except Exception as e:
                            print(f"[启动时更新] ❌ 更新失败: {e}")
                            import traceback
                            traceback.print_exc()
                    
                    threading.Thread(target=update_task, daemon=True).start()
                
                # run scheduler at 20:00 by default; can override with AUTO_UPDATE_TIME
                at_time = os.getenv('AUTO_UPDATE_TIME', '20:00')
                updater.start_background_scheduler(at_time)
                print(f"[startup] 自动更新调度已启动，每天 {at_time} 执行")
        except Exception as e:
            print(f"[startup] 自动更新调度启动失败: {e}")

    # 跨域解决
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 允许所有来源，生产环境请替换为你的前端地址
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 自定义验证错误处理器
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        # 将错误信息整合为一个字符串
        error_messages = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error['loc'] if loc != 'body')
            message = error['msg']
            error_messages.append(f"字段 '{field}': {message}")
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "; ".join(error_messages)},
        )

    # 全局异常处理器
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        print("!!!!!!!!!!!!!! UNEXPECTED ERROR !!!!!!!!!!!!!!")
        traceback.print_exc()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "服务器内部错误，请查看后端控制台日志"},
        )

    # 引入应用中的路由
    app.include_router(auth_router.router, prefix="/api/auth", tags=["认证"])
    app.include_router(user_router.router, prefix="/api/users", tags=["用户"])
    app.include_router(stock_router.router, prefix="/api/stocks", tags=["股票"])
    # vadmin 用户管理放到 /api/vadmin/users 下，保持与前端 /api 前缀一致
    app.include_router(vadmin_users_router.router, prefix="/api/vadmin/users", tags=["vadmin_users"])

    return app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

