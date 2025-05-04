from typing import Any, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
import httpx

from app import crud
from app.api import deps
from app.models.service import ServiceType

router = APIRouter()

@router.post("/authenticate", response_model=dict)
async def verify_student(
    *,
    db: Session = Depends(deps.get_db),
    name: str = Form(...),
    id: str = Form(...),
    photo: Optional[UploadFile] = File(None),
) -> Any:
    """验证学生身份
    Args:
        name: 学生姓名
        id: 学生学号
        photo: 可选的照片文件
    Returns:
        {"status": "string"}
    """
    try:
        # 从内部数据库获取API配置
        service = crud.service.get_by_type(db, service_type=ServiceType.STUDENT_VERIFICATION)
        if not service or not service.external_api_config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="学生验证服务未配置"
            )
        
        config = service.external_api_config
        
        # 构建请求数据
        verification_data = {
            "name": name,
            "id": id,
        }
        
        files = None
        if photo and photo.filename:  # 检查文件是否存在且有文件名
            # 如果提供了照片，将其作为文件上传
            photo_content = await photo.read()
            files = {"photo": (photo.filename, photo_content, photo.content_type)}
        
        # 发送请求到外部验证服务
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{config.base_url}{config.path}",
                data=verification_data,
                files=files,
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"验证失败: {response.text}"
                )
            
            return response.json()
            
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"验证服务暂时不可用: {str(e)}"
        )

@router.post("/record", response_model=dict)
async def get_student_record(
    *,
    db: Session = Depends(deps.get_db),
    name: str = Body(...),
    id: str = Body(...),
) -> Any:
    """获取学生GPA和年份信息
    
    Args:
        name: 学生姓名
        id: 学生学号
    Returns:
        {
            "name": "string",
            "enroll_year": "string",
            "graduation_year": "string",
            "gpa": float
        }
    """
    try:
        # 从内部数据库获取API配置
        service = crud.service.get_by_type(db, service_type=ServiceType.STUDENT_GPA)
        if not service or not service.external_api_config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="学生GPA查询服务未配置"
            )
        
        config = service.external_api_config
        
        # 构建请求数据
        record_data = {
            "name": name,
            "id": id,
        }
        
        # 发送请求到外部服务
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{config.base_url}{config.path}",
                json=record_data,
                headers={"Authorization": f"Bearer {config.api_key}"} if config.api_key else None
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"获取记录失败: {response.text}"
                )
            
            return response.json()
            
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"服务暂时不可用: {str(e)}"
        )