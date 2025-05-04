from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import models, crud
from app.api import deps
from app.models.payment import PaymentStatus

router = APIRouter()


@router.get("/", response_model=List[dict])
async def read_transfers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_e_admin),
) -> Any:
    """获取所有转账记录（需要E-Admin权限）"""
    transfers = db.query(models.Transfer).offset(skip).limit(limit).all()
    
    # 转换为字典列表，包含组织信息
    result = []
    for transfer in transfers:
        transfer_data = jsonable_encoder(transfer)
        organization = db.query(models.Organization).filter(models.Organization.id == transfer.organization_id).first()
        transfer_data["organization_name"] = organization.name if organization else None
        result.append(transfer_data)
    
    return result


@router.get("/organization/{organization_id}", response_model=List[dict])
async def read_organization_transfers(
    organization_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """获取组织的转账记录"""
    # 检查组织是否存在
    organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="组织不存在",
        )
    
    # 检查权限：只有组织协调人或管理员可以查看组织的转账记录
    is_admin = current_user.role in [models.UserRole.E_ADMIN, models.UserRole.T_ADMIN, models.UserRole.SENIOR_E_ADMIN]
    is_convener = current_user.id == organization.convener_id
    
    if not (is_admin or is_convener):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，只有组织协调人或管理员可以查看组织的转账记录",
        )
    
    # 查询组织的转账记录
    transfers = crud.transfer.get_by_organization(db, organization_id=organization_id, skip=skip, limit=limit)
    
    # 转换为字典列表
    result = []
    for transfer in transfers:
        transfer_data = jsonable_encoder(transfer)
        transfer_data["organization_name"] = organization.name
        result.append(transfer_data)
    
    return result


@router.get("/{transfer_id}", response_model=dict)
async def read_transfer(
    transfer_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """根据ID获取转账记录"""
    transfer = db.query(models.Transfer).filter(models.Transfer.id == transfer_id).first()
    if not transfer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="转账记录不存在",
        )
    
    # 检查权限：只有组织协调人或管理员可以查看转账记录
    organization = db.query(models.Organization).filter(models.Organization.id == transfer.organization_id).first()
    is_admin = current_user.role in [models.UserRole.E_ADMIN, models.UserRole.T_ADMIN, models.UserRole.SENIOR_E_ADMIN]
    is_convener = organization and current_user.id == organization.convener_id
    
    if not (is_admin or is_convener):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，无法查看转账记录",
        )
    
    # 返回转账记录，包含组织信息
    result = jsonable_encoder(transfer)
    result["organization_name"] = organization.name if organization else None
    
    return result


@router.post("/transfer", response_model=dict)
async def create_transfer(
    *,
    db: Session = Depends(deps.get_db),
    amount: float = Body(...),
    description: str = Body(...),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """创建转账记录（需要组织成员权限）"""
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您不属于任何组织，无法创建转账记录",
        )
    
    # 检查组织是否已验证
    organization = db.query(models.Organization).filter(models.Organization.id == current_user.organization_id).first()
    if not organization.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="组织尚未通过验证，无法创建转账记录",
        )
    
    # 检查用户余额是否足够
    if current_user.balance < amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"您的余额不足，当前余额：{current_user.balance} 元，需要：{amount} 元",
        )
    
    # 获取组织的银行账户
    bank_account = db.query(models.Payment).filter(
        models.Payment.organization_id == organization.id,
        models.Payment.is_deleted == False,
        models.Payment.is_active == True
    ).first()
    
    if not bank_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="组织尚未设置银行账户，请联系组织协调人设置",
        )
    
    # 扣除用户余额
    current_user.balance -= amount
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    # 创建转账记录
    transfer = crud.transfer.create_transfer(
        db=db,
        organization_id=current_user.organization_id,
        from_user_id=current_user.id,
        to_bank_account_id=bank_account.id,
        amount=amount,
        description=description,
        status=PaymentStatus.SUCCESS  # 使用枚举值
    )
    
    # 记录日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        log_type=models.LogType.PAYMENT,
        action="创建转账记录",
        details=f"用户 {current_user.email} 为组织 {organization.name} 创建了转账记录 {transfer.id}，金额：{amount} 元，剩余余额：{current_user.balance} 元"
    )
    
    return {
        "message": "转账记录创建成功",
        "transfer_id": transfer.id,
        "amount": amount,
        "status": transfer.status,
        "remaining_balance": current_user.balance
    }


@router.put("/{transfer_id}/status", response_model=dict)
async def update_transfer_status(
    transfer_id: int,
    *,
    db: Session = Depends(deps.get_db),
    status: PaymentStatus = Body(...),
    transaction_id: str = Body(None),
    current_user: models.user.User = Depends(deps.get_current_e_admin),
) -> Any:
    """更新转账状态（需要E-Admin权限）"""
    transfer = db.query(models.Transfer).filter(models.Transfer.id == transfer_id).first()
    if not transfer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="转账记录不存在",
        )
    
    # 更新转账状态
    updated_transfer = crud.transfer.update_transfer_status(
        db=db,
        transfer_id=transfer_id,
        status=status,
        transaction_id=transaction_id
    )
    
    if not updated_transfer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="更新转账状态失败",
        )
    
    # 记录日志
    organization = db.query(models.Organization).filter(models.Organization.id == transfer.organization_id).first()
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=transfer.organization_id,
        log_type=models.LogType.PAYMENT,
        action="更新转账状态",
        details=f"管理员 {current_user.email} 将组织 {organization.name} 的转账记录 {transfer.id} 状态更新为 {status}"
    )
    
    return {
        "message": "转账状态更新成功",
        "transfer_id": transfer.id,
        "status": status,
        "transaction_id": transaction_id
    }