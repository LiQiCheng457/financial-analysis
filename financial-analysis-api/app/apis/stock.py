from typing import Optional, Any, Dict, List
import traceback

from fastapi import APIRouter, Query, HTTPException, Depends, Body  # type: ignore[reportMissingImports]
import math
from fastapi.responses import JSONResponse  # type: ignore[reportMissingImports]
from fastapi.encoders import jsonable_encoder  # type: ignore[reportMissingImports]

from app.services import stock_service
from app.services import technical_indicators
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/trade_dates", summary="获取交易日历")
async def trade_dates() -> JSONResponse:
    try:
        dates = stock_service.get_trade_dates() or []
        # For backward compatibility return the raw array (frontend expects an array)
        return JSONResponse(content=jsonable_encoder(dates))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/realtime", summary="获取单个股票实时行情")
async def get_stock_realtime(code: str = Query(..., description="股票代码（6位数字）")) -> JSONResponse:
    """获取单个股票的实时行情数据
    
    - 使用 AKShare 的 stock_individual_info_em 接口
    - 速度快，直接查询单股票
    - 示例: /api/stocks/realtime?code=000001
    """
    try:
        result = stock_service.get_stock_realtime_info(code)
        
        if result['status'] == 'error':
            return JSONResponse(
                content=jsonable_encoder(result),
                status_code=400
            )
        
        return JSONResponse(content=jsonable_encoder(result))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/realtime/batch", summary="批量获取多个股票实时行情")
async def get_stock_realtime_batch(codes: List[str] = Body(..., description="股票代码列表")) -> JSONResponse:
    """批量获取多个股票的实时行情数据
    
    - 从全量市场数据中筛选指定股票
    - 适合批量查询
    - 示例: POST /api/stocks/realtime/batch
      Body: ["000001", "600000", "300750"]
    """
    try:
        result = stock_service.get_stock_realtime_batch(codes)
        
        if result['status'] == 'error' and result['total'] == 0:
            return JSONResponse(
                content=jsonable_encoder(result),
                status_code=400
            )
        
        return JSONResponse(content=jsonable_encoder(result))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/search", summary="搜索股票（代码/名称）")
async def search_stocks(q: Optional[str] = Query(None, description="查询关键字(代码或名称)"), limit: Optional[int] = Query(20, description="返回数量上限")) -> JSONResponse:
    try:
        items = stock_service.search_stocks(q or "", limit=limit or 20) or []
        return JSONResponse(content=jsonable_encoder(items))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/trade_dates_with_status", summary="获取交易日历（含每日状态）")
async def trade_dates_with_status() -> JSONResponse:
    try:
        dates_with_status = stock_service.get_trade_dates_with_status() or []
        return JSONResponse(content=jsonable_encoder(dates_with_status))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sse_daily_summary", summary="上海证券交易所-每日概况")
async def sse_daily_summary(date: Optional[str] = Query(None, description="交易日期 YYYYMMDD")) -> JSONResponse:
    try:
        summary: Dict[str, Any] = stock_service.get_sse_daily_summary(date) or {}
        # ensure last_open_date field exists for client convenience
        if 'last_open_date' not in summary:
            try:
                summary['last_open_date'] = stock_service.get_last_open_date()
            except Exception:
                summary['last_open_date'] = None
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
) -> JSONResponse:
    try:
        records = stock_service.get_stock_history_data(code=code, start_date=start_date, end_date=end_date, adjust=adjust or "", source=(source or 'eastmoney'))
        # If the service recorded an underlying fetch error, return 502 with message
        if (not records) and getattr(stock_service, 'last_stock_history_error', None):
            return JSONResponse(content=jsonable_encoder({
                "status": "error",
                "message": f"获取历史行情失败: {stock_service.last_stock_history_error}"
            }), status_code=502)

        # 为避免 FastAPI/JSON 编码过程中因 NaN/Inf 导致的异常，再次做一次递归清洗，
        # 将任何非有限浮点数转为 None。服务层已尽量返回 JSON-safe 数据，但在极少
        # 数学运算路径上仍可能遗留不可序列化的浮点值，这里做最后防护。
        def _sanitize(obj):
            # 递归将非有限浮点和 NaN 转为 None
            if isinstance(obj, float):
                return obj if math.isfinite(obj) else None
            if isinstance(obj, dict):
                return {k: _sanitize(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [_sanitize(v) for v in obj]
            return obj

        safe_records = _sanitize(records)
        # return raw array for backward compatibility
        return JSONResponse(content=jsonable_encoder(safe_records))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/company_profile', summary='获取公司基本资料')
async def company_profile(q: Optional[str] = Query(None, description='股票代码或公司名称'), db: Session = Depends(get_db)) -> JSONResponse:
    try:
        if not q:
            return JSONResponse(content=jsonable_encoder({"status": "error", "message": "请提供查询关键字 q（股票代码或公司名称）"}), status_code=400)
        profile = stock_service.get_company_profile(db, q)
        if not profile:
            return JSONResponse(content=jsonable_encoder({"status": "not_found", "message": f"暂无 {q} 公司数据"}), status_code=200)
        return JSONResponse(content=jsonable_encoder({"status": "ok", "data": profile}))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/search_companies', summary='按行业等条件搜索公司列表（分页）')
async def search_companies(
    q: Optional[str] = Query('', description='搜索关键词（股票代码、公司名称等）'),
    industry: Optional[str] = Query(None, description='行业筛选（逗号分隔，支持多个，如：电子,计算机,通信）'),
    industry_match_mode: Optional[str] = Query('any', description='行业匹配模式：any(满足任一) 或 all(满足全部)'),
    search_mode: Optional[str] = Query('fuzzy', description='搜索模式：fuzzy(模糊) 或 exact(精准)'),
    min_capital: Optional[float] = Query(None, description='最小注册资本（元）'),
    max_capital: Optional[float] = Query(None, description='最大注册资本（元）'),
    region: Optional[str] = Query(None, description='地区筛选'),
    security_types: Optional[str] = Query(None, description='证券类型筛选（逗号分隔）'),
    page: Optional[int] = Query(1, ge=1, description='页码（从1开始）'),
    page_size: Optional[int] = Query(50, ge=1, le=200, description='每页数量（1-200）'),
    db: Session = Depends(get_db)
) -> JSONResponse:
    try:
        # q 和 industry 至少需要一个
        if not q and not industry:
            return JSONResponse(
                content=jsonable_encoder({
                    "status": "error", 
                    "message": "请提供搜索关键词 q 或行业筛选 industry"
                }), 
                status_code=400
            )
        
        result = stock_service.search_companies_by_industry(
            db, 
            q=q or '', 
            industry=industry,
            industry_match_mode=industry_match_mode or 'any',
            search_mode=search_mode or 'fuzzy',
            min_capital=min_capital,
            max_capital=max_capital,
            region=region,
            security_types=security_types,
            page=page or 1, 
            page_size=page_size or 50
        )
        
        if 'error' in result:
            return JSONResponse(
                content=jsonable_encoder({
                    "status": "error",
                    "message": result['error']
                }),
                status_code=500
            )
        
        return JSONResponse(content=jsonable_encoder({"status": "ok", **result}))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/technical_indicators", summary="计算技术指标")
async def get_technical_indicators(
    code: str = Query(..., description="股票代码"),
    start_date: Optional[str] = Query(None, description="开始日期 YYYYMMDD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYYMMDD"),
    indicators: Optional[str] = Query(None, description="指标列表，逗号分隔，如: MA,MACD,KDJ,RSI,BOLL,VOL"),
    source: Optional[str] = Query('eastmoney', description="数据源")
) -> JSONResponse:
    """获取股票历史数据并计算技术指标
    
    - 支持的指标: MA, EMA, MACD, KDJ, RSI, BOLL, VOL
    - 默认计算所有指标
    - 示例: /api/stocks/technical_indicators?code=000001&indicators=MA,MACD,RSI
    """
    try:
        # 获取历史数据
        history_data = stock_service.get_stock_history_data(
            code=code,
            start_date=start_date,
            end_date=end_date,
            adjust='',
            source=source
        )

        if not history_data:
            # If the underlying service recorded an error, return 502 with that message
            if getattr(stock_service, 'last_stock_history_error', None):
                return JSONResponse(
                    content=jsonable_encoder({
                        "status": "error",
                        "message": f"获取历史行情失败: {stock_service.last_stock_history_error}"
                    }),
                    status_code=502
                )

            return JSONResponse(
                content=jsonable_encoder({
                    "status": "error",
                    "message": "未获取到历史数据"
                }),
                status_code=404
            )
        
        # 解析指标列表
        indicator_list = None
        if indicators:
            indicator_list = [ind.strip().upper() for ind in indicators.split(',')]
        
        # 计算技术指标
        result = technical_indicators.calculate_all_indicators(
            data=history_data,
            indicators=indicator_list
        )
        
        return JSONResponse(content=jsonable_encoder(result))
    
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/indicator_config", summary="获取技术指标配置")
async def get_indicator_config() -> JSONResponse:
    """获取所有技术指标的配置信息
    
    - 返回各指标的名称、说明、默认参数等
    """
    try:
        config = technical_indicators.get_indicator_config()
        return JSONResponse(content=jsonable_encoder({
            "status": "ok",
            "data": config
        }))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/technical_signals", summary="检测技术信号")
async def get_technical_signals(
    code: str = Query(..., description="股票代码"),
    start_date: Optional[str] = Query(None, description="开始日期 YYYYMMDD"),
    end_date: Optional[str] = Query(None, description="结束日期 YYYYMMDD"),
    lookback: Optional[int] = Query(5, description="回看天数，检测最近N天的信号"),
    source: Optional[str] = Query('eastmoney', description="数据源")
) -> JSONResponse:
    """检测股票的技术信号
    
    - 自动识别MACD金叉/死叉、KDJ超买超卖、MA均线交叉等信号
    - 返回信号列表和综合交易建议
    - 示例: /api/stocks/technical_signals?code=000001&lookback=10
    """
    try:
        # 获取历史数据
        history_data = stock_service.get_stock_history_data(
            code=code,
            start_date=start_date,
            end_date=end_date,
            adjust='',
            source=source
        )
        
        if not history_data:
            return JSONResponse(
                content=jsonable_encoder({
                    "status": "error",
                    "message": "未获取到历史数据"
                }),
                status_code=404
            )
        
        # 计算所有技术指标
        indicator_result = technical_indicators.calculate_all_indicators(
            data=history_data,
            indicators=None  # 计算所有指标
        )
        
        if indicator_result['status'] != 'ok':
            return JSONResponse(
                content=jsonable_encoder(indicator_result),
                status_code=400
            )
        
        # 转换为DataFrame
        import pandas as pd
        df = pd.DataFrame(indicator_result['data'])
        
        # 检测信号
        signals = technical_indicators.detect_signals(df, lookback=lookback)
        
        # 生成交易建议
        advice = technical_indicators.generate_trading_advice(signals, df)
        
        return JSONResponse(content=jsonable_encoder({
            "status": "ok",
            "code": code,
            "signals": signals,
            "advice": advice,
            "total_signals": len(signals)
        }))
    
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

