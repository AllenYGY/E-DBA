from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.api import deps

router = APIRouter()


@router.get("/by-status", response_model=schemas.VerificationStatusListResponse)
async def get_verifications_by_status(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    e_admin_status: str = Query(None, description="e_admin_approved status, optional: PENDING、APPROVAL、REJECTION"),
    senior_status: str = Query(None, description="senior_approved status, optional: PENDING、APPROVAL、REJECTION"),
    current_user: models.user.User = Depends(deps.get_current_e_admin),
) -> Any:
    """根据 e_admin_approved 和 senior_approved 状态筛选验证记录，不传参数时返回全部（需要E-Admin权限）"""
    query = db.query(models.VerificationStatus)
    if e_admin_status:
        query = query.filter(models.VerificationStatus.e_admin_approved == e_admin_status)
    if senior_status:
        query = query.filter(models.VerificationStatus.senior_approved == senior_status)
    total = query.count()
    verifications = query.offset(skip).limit(limit).all()
    return {"items": verifications, "total": total}


@router.get("/by-e-admin-status", response_model=schemas.VerificationStatusListResponse)
def get_by_e_admin_status(
    status: str = Query(None, description="e_admin_approved status, optional: PENDING、APPROVAL、REJECTION"),
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_e_admin),
) -> Any:
    """根据e_admin_approved状态获取审核记录（需要E-Admin权限），不传status则返回所有"""
    if status:
        total = db.query(models.VerificationStatus).filter(
            models.VerificationStatus.e_admin_approved == status
        ).count()
        verifications = crud.verification_status.get_by_status(db, status=status, skip=skip, limit=limit)
    else:
        total = db.query(models.VerificationStatus).count()
        verifications = crud.verification_status.get_multi(db, skip=skip, limit=limit)
    return {"items": verifications, "total": total}

@router.get("/by-senior-status", response_model=schemas.VerificationStatusListResponse)
def get_by_senior_status(
    status: str = Query(None, description="senior_approved status, optional: PENDING、APPROVAL、REJECTION"),
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_senior_e_admin),
) -> Any:
    """根据senior_approved状态获取审核记录（需要Senior E-Admin权限），不传status则返回所有"""
    if status:
        total = db.query(models.VerificationStatus).filter(
            models.VerificationStatus.senior_approved == status
        ).count()
        verifications = crud.verification_status.get_by_senior_status(db, status=status, skip=skip, limit=limit)
    else:
        total = db.query(models.VerificationStatus).count()
        verifications = crud.verification_status.get_multi(db, skip=skip, limit=limit)
    return {"items": verifications, "total": total}

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
            detail="Organization not found",
        )
    
    # 检查权限：只有组织成员、组织协调人或管理员可以查看验证状态
    if current_user.organization_id != organization_id and current_user.role not in [
        models.UserRole.E_ADMIN, models.UserRole.SENIOR_E_ADMIN, models.UserRole.T_ADMIN
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions, cannot view verification status",
        )
    
    verification_status = crud.verification_status.get_by_organization(db, organization_id=organization_id)
    if not verification_status:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Verification status record not found",
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
        if status_in.senior_approved == "APPROVAL":
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
        if status_in.approved == 'APPROVAL':
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