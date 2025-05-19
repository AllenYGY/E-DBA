from typing import Any, Dict
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Body, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app import models, crud
from app.api import deps

router = APIRouter()

tz_utc_8 = timezone(timedelta(hours=8))

@router.get("/", response_model=Dict[str, Any])
async def read_policies(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User= Depends(deps.get_current_active_user),
) -> Any:
    """获取政策列表"""
    query = db.query(models.Policy).filter(models.Policy.is_deleted == False)
    total = query.count()
    policies = query.offset(skip).limit(limit).all()
    
    # 转换为字典列表，包含创建者信息
    result = []
    for policy in policies:
        policy_data = jsonable_encoder(policy)
        admin = db.query(models.User).filter(models.User.id == policy.created_by).first()
        policy_data["created_by_email"] = admin.email if admin else None
        # 不返回文件内容，只返回基本信息
        policy_data.pop("file_content", None)
        result.append(policy_data)
    
    return {"items": result, "total": total}

@router.post("/", response_model=dict)
async def create_policy(
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
    
    try:
        # 读取文件内容
        content = await file.read()
        file_content = content.decode('latin-1')  # 使用 latin-1 编码来保存二进制数据
        
        # 创建政策记录
        policy = crud.policy.create_policy(
            db=db,
            title=title,
            description=description,
            file_content=file_content,
            created_by=current_user.id
        )
            
        # 记录文件上传日志
        crud.log.create_log(
            db=db,
            user_id=current_user.id,
            organization_id=current_user.organization_id,
            log_type=models.LogType.ADMIN_ACTION,
            action="上传政策文件",
            details=f"管理员 {current_user.email} 上传了政策文件 {file.filename}"
        )
        
        # 返回政策信息（不包含文件内容）
        result = jsonable_encoder(policy)
        result.pop("file_content", None)  # 移除文件内容
        result["created_by_email"] = current_user.email
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件保存失败: {str(e)}"
        )

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
    result.pop("file_content", None)  # 移除文件内容
    admin = db.query(models.User).filter(models.User.id == policy.created_by).first()
    result["created_by_email"] = admin.email if admin else None
    
    return result

@router.post("/{policy_id}", response_model=dict)
async def update_policy(
    *,
    db: Session = Depends(deps.get_db),
    policy_id: int,
    title: str = Form(None),
    description: str = Form(None),
    file: UploadFile = File(None),
    is_active: bool = Form(None),
    remove_file: bool = Form(False),
    current_user: models.user.User= Depends(deps.get_current_e_admin),
) -> Any:
    """更新政策信息（需要E-Admin权限）"""
    policy = db.query(models.Policy).filter(models.Policy.id == policy_id).first()
    if not policy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="政策不存在，无法更新政策信息",
        )

    update_data = {}
    if title is not None:
        update_data["title"] = title
    if description is not None:
        update_data["description"] = description
    if is_active is not None:
        update_data["is_active"] = is_active

    # 处理文件上传
    if file is not None:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="只支持PDF格式的文件",
            )
        content = await file.read()
        update_data["file_content"] = content.decode('latin-1')
    elif remove_file:
        update_data["file_content"] = None

    # 更新政策
    updated_policy = crud.policy.update_policy(
        db=db,
        policy_id=policy_id,
        **update_data
    )

    if not updated_policy:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新政策失败"
        )

    return {"message": "政策信息更新成功"}

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
    policy.is_deleted = True
    policy.updated_at = datetime.now(tz_utc_8)
    db.add(policy)
    db.commit()
    
    # 记录政策删除日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        log_type=models.LogType.ADMIN_ACTION,
        action="删除政策",
        details=f"管理员 {current_user.email} 删除了政策 {policy_title}"
    )
    
    return {
        "id": policy_id,
        "message": "政策已成功删除"
    }

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
    
    if not policy.file_content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="政策文件内容不存在",
        )
    
    # 记录下载日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        log_type=models.LogType.ADMIN_ACTION,
        action="下载政策文件",
        details=f"用户 {current_user.email} 下载了政策文件"
    )
    
    # 将存储的内容转换回二进制
    file_content = policy.file_content.encode('latin-1')
    
    # 返回文件内容
    return Response(
        content=file_content,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=policy_{policy_id}.pdf"
        }
    )