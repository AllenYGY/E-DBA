from typing import Any, List
import httpx
from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import logging
import io

from app.crud.service import service
from app.models.service import ServiceType
from app.db.session import get_db

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/search", response_model=List[dict])
async def search_thesis(
    *,
    keywords: str = Body(..., embed=True),
    db: Session = Depends(get_db),
) -> Any:
    """搜索论文"""
    # 获取论文共享服务的配置
    thesis_service = service.get_by_type(db=db, service_type=ServiceType.PAPER_SHARING)
    logger.info(f"Thesis service: {thesis_service}")
    logger.info(f"Service type: {ServiceType.PAPER_SHARING}")
    
    if not thesis_service:
        logger.error("论文共享服务未找到")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="论文共享服务未配置,请稍后再试"
        )
    
    if not thesis_service.external_api_config:
        logger.error("论文共享服务未配置外部API")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="论文共享服务未配置,请稍后再试"
        )
    
    config = thesis_service.external_api_config
    logger.info(f"External API config: {config.__dict__}")
    
    # 调用外部API搜索论文
    url = f"{config.base_url}{config.path}"
    logger.info(f"Request URL: {url}")
    logger.info(f"Request body: {{'keywords': {keywords}}}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json={"keywords": keywords}
            )
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {response.text}")
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="论文共享服务暂时不可用,请稍后再试"
                )
            
            return response.json()
    except Exception as e:
        logger.error(f"Error calling external API: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"调用外部API时出错: {str(e)}"
        )


@router.post("/pdf")
async def get_thesis_pdf(
    *,
    title: str = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    """获取论文PDF"""
    pdf_service = service.get_by_type(db=db, service_type=ServiceType.PAPER_PDF)
    logger.info(f"PDF service: {pdf_service}")
    logger.info(f"Service type: {ServiceType.PAPER_PDF}")
    
    if not pdf_service or not pdf_service.external_api_config:
        logger.error("论文PDF服务未配置")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="论文PDF服务未配置,无法获取论文信息"
        )
    
    config = pdf_service.external_api_config
    logger.info(f"External API config: {config.__dict__}")
    
    url = f"{config.base_url}{config.path}"
    logger.info(f"Request URL: {url}")
    logger.info(f"Request body: {{'title': {title}}}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                params={"title": title}
            )
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {response.headers}")
            
            # 1. 如果是 PDF 文件流
            if response.headers.get("content-type", "").startswith("application/pdf"):
                return StreamingResponse(
                    io.BytesIO(response.content),
                    media_type="application/pdf",
                    headers={"Content-Disposition": f"attachment; filename=\"{title}.pdf\""}
                )
            
            # 2. 如果是 JSON 错误信息
            try:
                result = response.json()
                logger.info(f"Response body: {result}")
                # 兼容不同的错误返回格式
                if "PDF not found" in str(result):
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="PDF not found for given title."
                    )
                return result
            except Exception as e:
                logger.error(f"Error parsing response as JSON: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="论文PDF服务返回未知格式"
                )
    except Exception as e:
        logger.error(f"Error calling external API: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"调用外部API时出错: {str(e)}"
        ) 