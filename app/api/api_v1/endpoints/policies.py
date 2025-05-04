from typing import Any, List
from datetime import datetime, timezone, timedelta
import os

from fastapi import APIRouter, Body, Depends, HTTPException, status, UploadFile, File
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse

from app import models, crud
from app.api import deps

router = APIRouter()

tz_utc_8 = timezone(timedelta(hours=8))

@router.get("/", response_model=List[dict])
async def read_policies(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User= Depends(deps.get_current_active_user),
) -> Any:
    """获取政策列表"""
    # 查询所有活跃的政策
    policies = db.query(models.Policy).filter(models.Policy.is_active).offset(skip).limit(limit).all()
    
    # 转换为字典列表，包含创建者信息
    result = []
    for policy in policies:
        policy_data = jsonable_encoder(policy)
        admin = db.query(models.User).filter(models.User.id == policy.created_by).first()
        policy_data["created_by_email"] = admin.email if admin else None
        result.append(policy_data)
    
    return result


@router.post("/", response_model=dict)
async def create_policy(
    *,
    db: Session = Depends(deps.get_db),
    title: str = Body(...),
    description: str = Body(None),
    file_path: str = Body(...),  # 实际应用中应该上传文件
    current_user: models.user.User= Depends(deps.get_current_e_admin),
) -> Any:
    """创建新政策（需要E-Admin权限）"""
    # 创建政策
    policy = models.Policy(
        title=title,
        description=description,
        file_path=file_path,
        created_by=current_user.id,
        created_at=datetime.now(tz_utc_8),
        updated_at=datetime.now(tz_utc_8),
    )
    
    db.add(policy)
    db.commit()
    db.refresh(policy)
    
    # 记录政策创建日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        log_type=models.LogType.ADMIN_ACTION,
        action="创建政策",
        details=f"管理员 {current_user.email} 创建了政策 {policy.title}"
    )
    
    # 返回政策信息，包含创建者信息
    result = jsonable_encoder(policy)
    result["created_by_email"] = current_user.email
    
    return result


@router.get("/{policy_id}", response_model=dict)
async def read_policy(
    policy_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.user.User= Depends(deps.get_current_active_user),
) -> Any:
    """根据ID获取政策信息"""
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="政策不存在，无法获得政策信息",
        )
    
    # 返回政策信息，包含创建者信息
    result = jsonable_encoder(policy)
    admin = db.query(models.User).filter(models.User.id == policy.created_by).first()
    result["created_by_email"] = admin.email if admin else None
    
    return result


@router.put("/{policy_id}", response_model=dict)
async def update_policy(
    *,
    db: Session = Depends(deps.get_db),
    policy_id: int,
    title: str = Body(None),
    description: str = Body(None),
    file_path: str = Body(None),
    is_active: bool = Body(None),
    current_user: models.user.User= Depends(deps.get_current_e_admin),
) -> Any:
    """更新政策信息（需要E-Admin权限）"""
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="政策不存在，无法更新政策信息",
        )
    
    # 更新政策信息
    if title is not None:
        policy.title = title
    if description is not None:
        policy.description = description
    if file_path is not None:
        policy.file_path = file_path
    if is_active is not None:
        policy.is_active = is_active
    
    policy.updated_at = datetime.now(tz_utc_8)
    db.add(policy)
    db.commit()
    db.refresh(policy)
    
    # 记录政策更新日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        log_type=models.LogType.ADMIN_ACTION,
        action="更新政策",
        details=f"管理员 {current_user.email} 更新了政策 {policy.title} 的信息"
    )
    
    # 返回政策信息，包含创建者信息
    result = jsonable_encoder(policy)
    admin = db.query(models.User).filter(models.User.id == policy.created_by).first()
    result["created_by_email"] = admin.email if admin else None
    
    return result


@router.delete("/{policy_id}", response_model=dict)
async def delete_policy(
    *,
    db: Session = Depends(deps.get_db),
    policy_id: int,
    current_user: models.user.User= Depends(deps.get_current_e_admin),
) -> Any:
    """删除政策（需要E-Admin权限）"""
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="政策不存在",
        )
    
    # 获取政策信息（用于日志记录）
    policy_title = policy.title
    
    # 删除政策（实际上只是将其标记为非活跃）
    policy.is_active = False
    policy.updated_at = datetime.now(tz_utc_8)
    db.add(policy)
    db.commit()
    
    # 记录政策删除日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        log_type=models.LogType.ADMIN_ACTION,
        action="删除政策",
        details=f"管理员 {current_user.email} 删除了政策 {policy_title}"
    )
    
    # 返回删除结果
    return {
        "id": policy_id,
        "message": "政策已成功删除"
    }


@router.post("/upload", response_model=dict)
async def upload_policy_file(
    *,
    db: Session = Depends(deps.get_db),
    title: str = Body(...),
    description: str = Body(None),
    file: UploadFile = File(...),
    current_user: models.user.User= Depends(deps.get_current_e_admin),
) -> Any:
    """上传政策文件（需要E-Admin权限）"""
    # 检查文件类型
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持PDF格式的文件",
        )
    
    # 创建上传目录
    upload_dir = "uploads/policies"
    os.makedirs(upload_dir, exist_ok=True)
    
    # 生成安全的文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(upload_dir, safe_filename)
    
    try:
        # 保存文件
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            
        # 创建政策记录
        policy = models.Policy(
            title=title,
            description=description,
            file_path=file_path,
            created_by=current_user.id,
            created_at=datetime.now(tz_utc_8),
            updated_at=datetime.now(tz_utc_8),
            is_active=True
        )
        
        db.add(policy)
        db.commit()
        db.refresh(policy)
            
        # 记录文件上传日志
        crud.log.create_log(
            db=db,
            user_id=current_user.id,
            log_type=models.LogType.ADMIN_ACTION,
            action="上传政策文件",
            details=f"管理员 {current_user.email} 上传了政策文件 {file.filename}"
        )
        
        # 返回政策信息
        result = jsonable_encoder(policy)
        result["created_by_email"] = current_user.email
        
        return result
    except Exception as e:
        # 如果保存失败，删除可能已创建的文件
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件保存失败: {str(e)}"
        )


@router.get("/{policy_id}/download")
async def download_policy_file(
    *,
    db: Session = Depends(deps.get_db),
    policy_id: int,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """下载政策文件"""
    # 获取政策信息
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="政策不存在",
        )
    
    # 检查文件是否存在
    if not os.path.exists(policy.file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="政策文件不存在",
        )
    
    # 记录下载日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        log_type=models.LogType.ADMIN_ACTION,
        action="下载政策文件",
        details=f"用户 {current_user.email} 下载了政策文件 {os.path.basename(policy.file_path)}"
    )
    
    # 返回文件
    return FileResponse(
        path=policy.file_path,
        filename=os.path.basename(policy.file_path),
        media_type="application/pdf"
    )