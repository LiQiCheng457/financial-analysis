from fastapi import APIRouter

router = APIRouter()


@router.get("/search")
async def search_companies(keyword: str = "", industry: str = ""):
    """搜索公司"""
    return {
        "code": 200,
        "message": "success",
        "data": [],
    }


@router.get("/{stock_code}")
async def get_company_detail(stock_code: str):
    """获取公司详情"""
    return {
        "code": 200,
        "message": "success",
        "data": {
            "stock_code": stock_code,
            "name": "示例公司",
        },
    }
