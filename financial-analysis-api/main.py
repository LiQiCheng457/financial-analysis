from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uvicorn
from starlette.middleware.cors import CORSMiddleware
from app.apis import auth as auth_router
from app.apis import user as user_router
from app.apis import stock as stock_router
import traceback

from app.core.database import engine, Base
# ... (other imports)

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

    return app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)

