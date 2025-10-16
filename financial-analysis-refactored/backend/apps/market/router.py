from fastapi import APIRouter

router = APIRouter()


@router.get("/overview")
async def get_market_overview():
    """获取市场概况"""
    return {
        "code": 200,
        "message": "success",
        "data": {},
    }
