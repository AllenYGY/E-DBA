from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
import httpx
import logging
from pydantic import BaseModel

from app.crud.service import service
from app.models.service import ServiceType
from app.db.session import get_db
from app.schemas.user import BankAccountInfo

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/auth")
async def bank_auth(
    data: BankAccountInfo,
    db: Session = Depends(get_db),
):
    """银行账户认证"""
    bank_service = service.get_by_type(db=db, service_type=ServiceType.BANK_AUTH)
    if not bank_service or not bank_service.external_api_config:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="银行认证服务未配置"
        )
    config = bank_service.external_api_config
    url = f"{config.base_url}{config.path}"
    try:
        # 准备请求数据，包含银行认证需要的所有字段
        request_data = {
            "account_name": data.account_name,
            "account_number": data.account_number,
            "bank": data.bank,
            "password": data.password
        }

        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=request_data
            )
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "银行认证服务暂时不可用"
                }
            
            # 模拟银行认证成功
            return {
                "success": True,
                "message": "银行账户认证成功"
            }
    except Exception as e:
        logger.error(f"Error calling bank auth API: {str(e)}")
        return {
            "success": False,
            "message": f"调用银行认证API时出错: {str(e)}"
        }

class BankTransferRequest(BaseModel):
    from_bank: str
    from_name: str
    from_account: str
    password: str
    to_bank: str
    to_name: str
    to_account: str
    amount: int

@router.post("/transfer")
async def bank_transfer(
    data: BankTransferRequest,
    db: Session = Depends(get_db),
):
    """模拟银行转账"""
    transfer_service = service.get_by_type(db=db, service_type=ServiceType.BANK_TRANSFER)
    if not transfer_service or not transfer_service.external_api_config:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="银行转账服务未配置"
        )
    config = transfer_service.external_api_config
    url = f"{config.base_url}{config.path}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=data.dict()
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="银行转账服务暂时不可用"
                )
            return response.json()
    except Exception as e:
        logger.error(f"Error calling bank transfer API: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"调用银行转账API时出错: {str(e)}"
        )