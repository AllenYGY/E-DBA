from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.api import deps

router = APIRouter()


@router.get("/pending", response_model=List[schemas.VerificationStatus])
async def get_pending_verifications(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_e_admin),
) -> Any:
    """获取待审核的组织验证申请列表（需要E-Admin权限）"""
    verifications = crud.verification_status.get_pending_verifications(db, skip=skip, limit=limit)
    return verifications


@router.get("/{organization_id}", response_model=schemas.VerificationStatus)
async def get_verification_status(
    organization_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """获取组织的验证状态"""
    organization = crud.organization.get(db, id=organization_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="组织不存在",
        )
    
    # 检查权限：只有组织成员、组织协调人或管理员可以查看验证状态
    if current_user.organization_id != organization_id and current_user.role not in [
        models.UserRole.E_ADMIN, models.UserRole.SENIOR_E_ADMIN, models.UserRole.T_ADMIN
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，无法查看验证状态",
        )
    
    verification_status = crud.verification_status.get_by_organization(db, organization_id=organization_id)
    if not verification_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="验证状态记录不存在",
        )
    
    return verification_status

@router.post("/{organization_id}/e-admin-review", response_model=schemas.VerificationStatus)
def e_admin_review_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    status_in: schemas.EAdminVerificationStatusUpdate,
) -> Any:
    """
    E-Admin review organization verification.
    """
    print(f"Starting e_admin_review for organization {organization_id}")
    
    # 检查用户权限
    if current_user.role != models.UserRole.E_ADMIN:
        raise HTTPException(
            status_code=400,
            detail="The user doesn't have enough privileges, please check your role"
        )
    
    try:
        # 更新验证状态
        verification = crud.verification_status.e_admin_review(
            db,
            organization_id=organization_id,
            e_admin_id=current_user.id,
            approved=status_in.e_admin_approved,
            comment=status_in.e_admin_comment
        )
        
        # 记录日志
        try:
            crud.log.create(
                db,
                obj_in=schemas.LogCreate(
                    user_id=current_user.id,
                    organization_id=organization_id,
                    log_type=models.LogType.ORGANIZATION,
                    action="e_admin_review",
                    details=f"E-Admin {current_user.email} reviewed organization {organization_id} verification"
                )
            )
        except Exception as e:
            print(f"Error creating log: {str(e)}")
            # 不要因为日志创建失败而中断整个流程
        
        return verification
        
    except Exception as e:
        print(f"Error in e_admin_review: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update verification status: {str(e)}"
        )

@router.post("/{organization_id}/senior-review", response_model=schemas.VerificationStatus)
def senior_e_admin_review_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    status_in: schemas.SeniorEAdminVerificationStatusUpdate,
) -> Any:
    """
    Senior E-Admin review organization verification.
    """
    if current_user.role != models.UserRole.SENIOR_E_ADMIN:
        raise HTTPException(
            status_code=400,
            detail="The user doesn't have enough privileges"
        )
    
    try:
        # 更新验证状态
        verification = crud.verification_status.senior_admin_review(
            db,
            organization_id=organization_id,
            senior_e_admin_id=current_user.id,
            approved=status_in.senior_approved,
            comment=status_in.senior_comment
        )
        
        # 审核通过后，更新 organization 的 is_verified 字段
        organization = crud.organization.get(db, id=organization_id)
        if status_in.senior_approved:
            organization.is_verified = True
        else:
            organization.is_verified = False
        db.commit()
        db.refresh(organization)
        
        # 记录日志
        crud.log.create(
            db,
            obj_in=schemas.LogCreate(
                user_id=current_user.id,
                organization_id=organization_id,
                log_type=models.LogType.ORGANIZATION,
                action="senior_review",
                details=f"Senior E-Admin {current_user.email} reviewed organization {organization_id} verification, result: {status_in.senior_approved}"
            )
        )
        
        return verification
        
    except Exception as e:
        print(f"Error in senior review: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update verification status: {str(e)}"
        )

@router.post("/{organization_id}/t-admin-review", response_model=schemas.VerificationStatus)
def t_admin_review_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    status_in: schemas.TAdminVerificationUpdate,
) -> Any:
    """
    T-admin review organization verification.
    """
    print(f"Current user role: {current_user.role}")
    if current_user.role != models.UserRole.T_ADMIN:
        raise HTTPException(
            status_code=400,
            detail="The user doesn't have enough privileges"
        )
    
    # 检查组织是否存在
    organization = crud.organization.get(db, id=organization_id)
    if not organization:
        raise HTTPException(
            status_code=404,
            detail="Organization not found"
        )
    print(f"Found organization: {organization.id}")
    
    # 获取 E-admin 和 Senior E-admin 的 ID
    e_admin = crud.user.get_first_e_admin(db)
    senior_e_admin = crud.user.get_first_senior_e_admin(db)
    
    if not e_admin:
        raise HTTPException(
            status_code=500,
            detail="No E-admin user found in the system"
        )
    if not senior_e_admin:
        raise HTTPException(
            status_code=500,
            detail="No Senior E-admin user found in the system"
        )
    
    print(f"Using E-admin ID: {e_admin.id}, Senior E-admin ID: {senior_e_admin.id}")
    
    # T-admin 直接通过 E-admin 和 Senior E-admin 的审核
    try:
        verification = crud.verification_status.e_admin_review(
            db,
            organization_id=organization_id,
            e_admin_id=e_admin.id,
            approved=status_in.approved,
            comment=f"T-admin review: {status_in.comment}"
        )
        if not verification:
            raise HTTPException(
                status_code=500,
                detail="Failed to update E-admin review"
            )
        print("E-admin review updated successfully")
        
        verification = crud.verification_status.senior_admin_review(
            db,
            organization_id=organization_id,
            senior_e_admin_id=senior_e_admin.id,
            approved=status_in.approved,
            comment=f"T-admin review: {status_in.comment}"
        )
        if not verification:
            raise HTTPException(
                status_code=500,
                detail="Failed to update Senior E-admin review"
            )
        print("Senior E-admin review updated successfully")
        
        # 审核通过后，更新 organization 的 is_verified 字段
        if status_in.approved:
            organization.is_verified = True
        else:
            organization.is_verified = False
        db.commit()
        db.refresh(organization)
        
        # 记录日志
        try:
            crud.log.create(
                db,
                obj_in=schemas.LogCreate(
                    user_id=current_user.id,
                    organization_id=organization_id,
                    log_type=models.LogType.ORGANIZATION,
                    action="t_admin_review",
                    details=f"T-admin {current_user.email} reviewed organization {organization_id} verification"
                )
            )
            print("Log created successfully")
        except Exception as e:
            print(f"Error creating log: {str(e)}")
        
        return verification
        
    except Exception as e:
        print(f"Error during review updates: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error during review updates: {str(e)}"
        ) 