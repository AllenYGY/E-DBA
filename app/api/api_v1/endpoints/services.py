from typing import Any, List, Optional
from datetime import datetime, timezone, timedelta
import requests
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import schemas, crud
from app.models.service import Service, ServiceType
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.models.log import LogType
from app.api import deps

router = APIRouter()

tz_utc_8 = timezone(timedelta(hours=8))


@router.get("/", response_model=List[schemas.Service])
def read_services(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    service_type: Optional[ServiceType] = None,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve services.
    """
    if current_user.role == UserRole.O_CONVENER:
        # O-Convener can only see services from their organization
        services = crud.service.get_by_organization(
            db, organization_id=current_user.organization_id
        )
    else:
        # Other users can see all active services
        services = crud.service.get_multi(db, skip=skip, limit=limit)
    
    # Filter by service type if specified
    if service_type:
        services = [s for s in services if s.service_type == service_type]
    
    return services


@router.post("/", response_model=schemas.Service)
def create_service(
    *,
    db: Session = Depends(deps.get_db),
    service_in: schemas.ServiceCreate,
    current_user: User = Depends(deps.get_current_o_convener),
) -> Any:
    """
    Create new service.
    """
    # Check if organization is verified
    organization = crud.organization.get(db, id=current_user.organization_id)
    if not organization or not organization.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization must be verified to create services",
        )
    
    # 确保 organization_id 被设置
    service_data = service_in.dict() if hasattr(service_in, 'dict') else dict(service_in)
    service_data['organization_id'] = current_user.organization_id
    service = crud.service.create(db=db, obj_in=schemas.ServiceCreate(**service_data))
    
    # Create service-specific configuration
    if service.service_type == ServiceType.STUDENT_VERIFICATION:
        crud.student_verification_config.create_with_service(
            db=db, service_id=service.id
        )
    elif service.service_type == ServiceType.PAPER_SHARING:
        crud.paper_sharing_config.create_with_service(
            db=db, service_id=service.id
        )
    
    return service


@router.get("/my-services", response_model=List[dict])
async def read_my_services(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_o_convener),
) -> Any:
    """获取当前用户组织的服务列表（需要O-Convener权限）"""
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您不属于任何组织",
        )
    
    # 查询组织的服务
    services = db.query(Service).filter(
        Service.organization_id == current_user.organization_id
    ).offset(skip).limit(limit).all()
    
    # 获取组织信息
    organization = db.query(Organization).filter(Organization.id == current_user.organization_id).first()
    
    # 转换为字典列表，包含组织信息
    result = []
    for service in services:
        service_data = jsonable_encoder(service)
        service_data["organization_name"] = organization.name if organization else None
        result.append(service_data)
    
    return result


@router.get("/{service_id}", response_model=dict)
async def read_service(
    service_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """根据ID获取服务信息"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="服务不存在，无法获取信息",
        )
    
    # 获取组织信息
    organization = db.query(Organization).filter(Organization.id == service.organization_id).first()
    
    # 返回服务信息，包含组织名称
    result = jsonable_encoder(service)
    result["organization_name"] = organization.name if organization else None
    
    return result


@router.put("/{service_id}", response_model=dict)
async def update_service(
    *,
    db: Session = Depends(deps.get_db),
    service_id: int,
    service_in: dict,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """更新服务信息"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="服务不存在",
        )
    
    # 检查权限：只有服务所属组织的协调人或管理员可以更新服务信息
    is_admin = current_user.role in [UserRole.E_ADMIN, UserRole.T_ADMIN, UserRole.SENIOR_E_ADMIN]
    is_convener = current_user.organization_id == service.organization_id and current_user.role == UserRole.O_CONVENER
    
    if not (is_admin or is_convener):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，只有服务所属组织的协调人或管理员可以更新服务信息",
        )
    
    # 更新服务信息
    for key, value in service_in.items():
        if key != "id" and key != "organization_id" and key != "created_at":
            setattr(service, key, value)
    
    service.updated_at = datetime.now(tz_utc_8)
    db.add(service)
    db.commit()
    db.refresh(service)
    
    # 获取组织信息
    organization = db.query(Organization).filter(Organization.id == service.organization_id).first()
    
    # 记录服务更新日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=service.organization_id,
        log_type=LogType.SERVICE,
        action="更新服务信息",
        details=f"用户 {current_user.email} 更新了服务 {service.name} 的信息"
    )
    
    # 返回服务信息，包含组织名称
    result = jsonable_encoder(service)
    result["organization_name"] = organization.name if organization else None
    
    return result


@router.delete("/{service_id}", response_model=dict)
async def delete_service(
    *,
    db: Session = Depends(deps.get_db),
    service_id: int,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """删除服务"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="服务不存在",
        )
    
    # 检查权限：只有服务所属组织的协调人或管理员可以删除服务
    is_admin = current_user.role in [UserRole.E_ADMIN, UserRole.T_ADMIN, UserRole.SENIOR_E_ADMIN]
    is_convener = current_user.organization_id == service.organization_id and current_user.role == UserRole.O_CONVENER
    
    if not (is_admin or is_convener):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，只有服务所属组织的协调人或管理员可以删除服务",
        )
    
    # 获取组织信息（用于日志记录）
    organization = db.query(Organization).filter(Organization.id == service.organization_id).first()
    organization_id = service.organization_id
    service_name = service.name
    
    # 删除服务
    db.delete(service)
    db.commit()
    
    # 记录服务删除日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=organization_id,
        log_type=LogType.SERVICE,
        action="删除服务",
        details=f"用户 {current_user.email} 删除了服务 {service_name}"
    )
    
    # 返回删除结果
    return {
        "id": service_id,
        "message": "服务已成功删除",
        "organization_name": organization.name if organization else None
    }


@router.put("/{service_id}/config", response_model=schemas.Service)
def update_service_config(
    *,
    db: Session = Depends(deps.get_db),
    service_id: int,
    config_in: schemas.ServiceConfigUpdate,
    current_user: User = Depends(deps.get_current_o_convener),
) -> Any:
    """
    Update service configuration.
    """
    service = crud.service.get(db, id=service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )
    
    # Check if user has permission to update this service
    if service.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    
    # Update service configuration based on service type
    if service.service_type == ServiceType.STUDENT_VERIFICATION:
        config = crud.student_verification_config.get_by_service(db, service_id=service_id)
        if config:
            crud.student_verification_config.update(
                db, db_obj=config, obj_in=config_in.student_verification_config
            )
    elif service.service_type == ServiceType.PAPER_SHARING:
        config = crud.paper_sharing_config.get_by_service(db, service_id=service_id)
        if config:
            crud.paper_sharing_config.update(
                db, db_obj=config, obj_in=config_in.paper_sharing_config
            )
    
    # Update external API configuration if provided
    if config_in.external_api_config:
        api_config = crud.external_api_config.get_by_service(db, service_id=service_id)
        if api_config:
            crud.external_api_config.update(
                db, db_obj=api_config, obj_in=config_in.external_api_config
            )
        else:
            crud.external_api_config.create_with_service(
                db=db, service_id=service_id, obj_in=config_in.external_api_config
            )
    
    return service


@router.post("/{service_id}/call", response_model=Any)
def call_service_api(
    *,
    db: Session = Depends(deps.get_db),
    service_id: int,
    params: dict,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Call external API for a service.
    """
    service = crud.service.get(db, id=service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )
    
    # Check if service is active
    if not service.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service is not active",
        )
    
    # Get external API configuration
    api_config = crud.external_api_config.get_by_service(db, service_id=service_id)
    if not api_config:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service does not have external API configuration",
        )
    
    # Build request URL
    url = f"{api_config.base_url}{api_config.path}"
    
    # Prepare request parameters based on input format
    request_params = {}
    if api_config.input_format:
        for key in api_config.input_format.keys():
            if key in params:
                request_params[key] = params[key]
    
    # Make API request
    try:
        if api_config.method.upper() == "POST":
            response = requests.post(url, json=request_params)
        else:
            response = requests.get(url, params=request_params)
        
        response.raise_for_status()
        result = response.json()
        
        # Record service usage
        crud.service_usage.create(
            db=db,
            obj_in={
                "service_id": service_id,
                "user_id": current_user.id,
                "usage_details": str(params),
                "fee_charged": service.fee_per_use,
            }
        )
        
        return result
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to call external API: {str(e)}",
        )


@router.get("/public/edba", response_model=List[schemas.Service])
def get_edba_public_services(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_o_convener),
) -> Any:
    """
    获取 E-DBA 组织的公开服务列表（需要 O-Convener 权限）
    """
    # 先获取 E-DBA 组织
    edba_org = db.query(Organization).filter(Organization.name == "E-DBA").first()
    if not edba_org:
        raise HTTPException(
            status_code=404,
            detail="E-DBA organization not found"
        )
    
    # 查询 E-DBA 的公开服务
    services = db.query(Service).filter(
        Service.organization_id == edba_org.id,
        Service.is_public == True,
        Service.is_active == True
    ).offset(skip).limit(limit).all()
    
    return services


@router.post("/active/{service_type}", response_model=schemas.Service)
def active_service(
    *,
    db: Session = Depends(deps.get_db),
    service_type: ServiceType,
    current_user: User = Depends(deps.get_current_o_convener),
) -> Any:
    """
    从 E-DBA 的公开服务激活到当前组织
    """
    # 检查组织是否已验证
    organization = crud.organization.get(db, id=current_user.organization_id)
    if not organization or not organization.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization must be verified to active services",
        )
    
    # 获取 E-DBA 组织
    edba_org = db.query(Organization).filter(Organization.name == "E-DBA").first()
    if not edba_org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="E-DBA organization not found",
        )
    
    # 获取要激活的服务
    source_service = db.query(Service).filter(
        Service.service_type == service_type,
        Service.organization_id == edba_org.id,
        Service.is_public == True,
        Service.is_active == True
    ).first()
    
    if not source_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service type {service_type} not found or not available for activating",
        )
    
    # 检查当前组织是否已经激活了该类型的服务
    existing_service = db.query(Service).filter(
        Service.service_type == service_type,
        Service.organization_id == current_user.organization_id
    ).first()
    
    if existing_service:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service type {service_type} already activated in your organization",
        )
    

    print(source_service.service_type,service_type)
    # 创建新服务的数据字典，直接引用已有 external_api_config_id
    service_data = {
        "name": source_service.name,
        "description": source_service.description,
        "service_type": source_service.service_type,  # 服务类型，始终赋值
        "is_public": False,  # 默认设置为非公开
        "fee_per_use": source_service.fee_per_use,
        "fee_unit": source_service.fee_unit,
        "organization_id": current_user.organization_id,
        # 直接引用源服务的 external_api_config_id，不再创建新配置
        "external_api_config_id": source_service.external_api_config_id
    }

    # 创建服务，确保 service_type 和 external_api_config_id 字段都被赋值
    new_service = crud.service.create(
        db=db,
        obj_in=schemas.ServiceCreate(**service_data)
    )

    return new_service


