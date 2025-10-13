from typing import Optional
import traceback

from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app.services import stock_service

router = APIRouter()


@router.get("/trade_dates", summary="获取交易日历")
async def trade_dates():
    try:
        dates = stock_service.get_trade_dates()
        return JSONResponse(content=jsonable_encoder(dates))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sse_daily_summary", summary="上海证券交易所-每日概况")
async def sse_daily_summary(date: Optional[str] = Query(None, description="交易日期 YYYYMMDD")):
    try:
        summary = stock_service.get_sse_daily_summary(date)
        return JSONResponse(content=jsonable_encoder(summary))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history", summary="获取个股历史行情")
async def get_stock_history(
    code: str,
    start_date: Optional[str] = Query(None, description="开始日期 YYYYMMDD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYYMMDD"),
    adjust: Optional[str] = Query('', description="调整类型: '' 不复权, 'qfq' 前复权, 'hfq' 后复权"),
    source: Optional[str] = Query('eastmoney', description="数据源: eastmoney | sina | tencent")
):
    try:
        records = stock_service.get_stock_history_data(code=code, start_date=start_date, end_date=end_date, adjust=adjust or "", source=(source or 'eastmoney'))
        return JSONResponse(content=jsonable_encoder(records))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
