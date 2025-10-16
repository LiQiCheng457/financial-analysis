from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from apps.company.router import router as company_router
from apps.market.router import router as market_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="金融分析系统API - 重构版",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(company_router, prefix="/api/company", tags=["公司信息"])
app.include_router(market_router, prefix="/api/market", tags=["市场数据"])


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "金融分析系统API - 重构版",
        "version": "2.0.0",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
