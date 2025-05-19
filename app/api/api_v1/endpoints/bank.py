from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
import httpx
import logging
from pydantic import BaseModel
from typing import Any

from app.db.session import get_db
from app.schemas.user import BankAccountInfo
from app.api import deps
from app.models import user
from app.models.log import LogType
from app.models.payment import PaymentType, Payment

from app.crud import payment, log
from app.crud import payment as payment_crud

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/auth")
async def bank_auth(
    data: BankAccountInfo,
    db: Session = Depends(get_db),
):
    """Bank account verification"""
    bank_auth_service = {
        "base_url": "http://172.16.160.88:8001",
        "path": "/hw/bank/authenticate",
    }
    url = f"{bank_auth_service['base_url']}{bank_auth_service['path']}"
    try:
        request_data = {
            "account_name": data.account_name,
            "account_number": data.account_number,
            "bank": data.bank,
            "password": data.password
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                url,
                json=request_data
            )
            
            if response.status_code != 200:
                logger.error(f"Bank auth service returned status code: {response.status_code}")
                return {
                    "success": False,
                    "message": "Bank auth service temporarily unavailable"
                }

            return response.json()
    except Exception as e:
        logger.error(f"Error calling bank auth API: {str(e)}")
        return {
            "success": False,
            "message": f"Error calling bank auth API: {str(e)}"
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
    """Simulate bank transfer"""
    bank_transfer_service = {
        "base_url": "http://172.16.160.88:8001",
        "path": "/hw/bank/transfer",
        "method": "POST",
    }
    url = f"{bank_transfer_service['base_url']}{bank_transfer_service['path']}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json=data.dict()
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Bank transfer service temporarily unavailable"
                )
            return response.json()
    except Exception as e:
        logger.error(f"Error calling bank transfer API: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error calling bank transfer API: {str(e)}"
        )
    

    
    
# get all bank accounts
@router.get("/get-all-bank-accounts")
async def get_all_bank_accounts(
):
    """Get all bank accounts"""
    bank_transfer_service = {
        "base_url": "http://172.16.160.88:8001",
        "path": "/hw/bank/all",
    }
    url = f"{bank_transfer_service['base_url']}{bank_transfer_service['path']}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Bank transfer service temporarily unavailable"
                )
            return response.json()
    except Exception as e:
        logger.error(f"Error calling bank transfer API: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error calling bank transfer API: {str(e)}"
        )


@router.post("/setup-bank-account")
async def setup_bank_account(
    *,
    db: Session = Depends(deps.get_db),
    bank_account: BankAccountInfo,
    current_user: user.User = Depends(deps.get_current_o_convener),
) -> Any:
    """
    Verify bank account then create payment account
    """
    bank_auth_result = await bank_auth(bank_account, db)
    if not bank_auth_result["success"]:
        raise HTTPException(
            status_code=400,
            detail=bank_auth_result["message"],
        )

    # Create payment account
    payment.create_payment(
        db,
        organization_id=current_user.organization_id,
        payment_type=PaymentType.TRANSFER,
        account_name=bank_account.account_name,
        account_number=bank_account.account_number,
        password=bank_account.password,
        bank=bank_account.bank
    )
    print(f"Payment account created: {bank_account.account_name} {bank_account.account_number} {bank_account.bank}")

    # create log
    log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        log_type=LogType.SYSTEM,
        action="Setup bank account",
        details=f"User {current_user.email} setup bank account"
    )

    return {"success": True, "message": "Bank account verified successfully"}


@router.post("/update-bank-account")
async def update_bank_account(
    *,
    db: Session = Depends(deps.get_db),
    bank_account: BankAccountInfo,
    current_user: user.User = Depends(deps.get_current_o_convener),
) -> Any:
    """
    Update or create payment account for current organization
    """
    # verify bank account
    bank_auth_result = await bank_auth(bank_account, db)
    if bank_auth_result['status'] != "success":
        raise HTTPException(
            status_code=400,
            detail=bank_auth_result.get("message", "Bank auth failed"),
        )

    # search for existing payment account
    payment_obj = db.query(Payment).filter_by(organization_id=current_user.organization_id).first()
    if payment_obj:
        payment_obj.account_name = bank_account.account_name
        payment_obj.account_number = bank_account.account_number
        payment_obj.password = bank_account.password
        payment_obj.bank = bank_account.bank
        db.commit()
        db.refresh(payment_obj)
    else:
        payment.create_payment(
            db,
            organization_id=current_user.organization_id,
            payment_type=PaymentType.TRANSFER,
            account_name=bank_account.account_name,
            account_number=bank_account.account_number,
            password=bank_account.password,
            bank=bank_account.bank
        )

    log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        log_type=LogType.SYSTEM,
        action="Update bank account",
        details=f"User {current_user.email} updated bank account"
    )

    return {"success": True, "message": "Bank account updated successfully"}


@router.get("/get-payment-account")
async def get_payment_account(
    db: Session = Depends(get_db),
    current_user: user.User = Depends(deps.get_current_o_convener),
):
    """
    获取当前 O-Convener 所在组织的 payment 账户信息
    """
    payment = db.query(Payment).filter_by(
        organization_id=current_user.organization_id).first()
    if not payment:
        return {"detail": "No payment account found for this organization"}
    return {
        "account_name": payment.account_name,
        "account_number": payment.account_number,
        "bank": payment.bank,
    }

class OrgBankTransferRequest(BaseModel):
    from_org_id: int
    to_org_id: int
    amount: int

@router.post("/transfer-by-org")
async def bank_transfer_by_org(
    data: OrgBankTransferRequest,
    db: Session = Depends(get_db),
):
    """
    Simulate bank transfer by organization id
    """
    # 通过 payment CRUD 获取银行账户信息
    from_payment = payment_crud.get_by_organization(db, organization_id=data.from_org_id, limit=1)
    to_payment = payment_crud.get_by_organization(db, organization_id=data.to_org_id, limit=1)

    from_payment = from_payment[0] if from_payment else None
    to_payment = to_payment[0] if to_payment else None

    if not from_payment or not to_payment:
        raise HTTPException(
            status_code=400,
            detail="Organization bank account not found"
        )

    # 组装银行转账参数
    bank_transfer_service = {
        "base_url": "http://172.16.160.88:8001",
        "path": "/hw/bank/transfer",
        "method": "POST",
    }
    url = f"{bank_transfer_service['base_url']}{bank_transfer_service['path']}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                json={
                    "from_bank": from_payment.bank,
                    "from_name": from_payment.account_name,
                    "from_account": from_payment.account_number,
                    "password": from_payment.password,
                    "to_bank": to_payment.bank,
                    "to_name": to_payment.account_name,
                    "to_account": to_payment.account_number,
                    "amount": data.amount,
                }
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Bank transfer service temporarily unavailable"
                )
            return response.json()
    except Exception as e:
        logger.error(f"Error calling bank transfer API: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error calling bank transfer API: {str(e)}"
        )
