from typing import Any, List, Optional
from datetime import timezone, timedelta
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
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new service.
    Need to be O-Convener or Data User with permission level 3.
    """
    # Check if the organization is verified
    organization = crud.organization.get(db, id=current_user.organization_id)
    if not organization or not organization.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization must be verified to create services",
        )
    
    # Check if the user has permission to create services
    if not crud.service.can_create_service(
        db, 
        user_id=current_user.id, 
        organization_id=current_user.organization_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied. Need to be O-Convener or Data User with permission level 3",
        )
    
    # Check if the service already exists
    if crud.service.check_service_exists(
        db,
        organization_id=current_user.organization_id,
        service_type=service_in.service_type,
        name=service_in.name
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service with type {service_in.service_type} and name '{service_in.name}' already exists in this organization"
        )
    
    # Ensure organization_id is set
    service_data = service_in.dict() if hasattr(service_in, 'dict') else dict(service_in)
    service_data['organization_id'] = current_user.organization_id
    
    try:
        service = crud.service.create_service(db=db, obj_in=schemas.ServiceCreate(**service_data))
        
        # Create log for service creation
        crud.log.create_log(
            db=db,
            user_id=current_user.id,
            organization_id=current_user.organization_id,
            log_type=LogType.SERVICE_ACCESS,
            action="Create service",
            details=f"User {current_user.email} created service {service.name}"
        )
        
        return service
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/org-services", response_model=List[dict])
async def read_services_by_organization(
    db: Session = Depends(deps.get_db),
    organization_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get services by organization_id (if provided), else by current user's organization.
    """
    if organization_id is not None:
        org = db.query(Organization).filter(Organization.id == organization_id).first()
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
        services = db.query(Service).filter(Service.organization_id == organization_id)
    else:
        if not current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are not a member of any organization",
            )
        services = db.query(Service).filter(Service.organization_id == current_user.organization_id)
        org = db.query(Organization).filter(Organization.id == current_user.organization_id).first()
    services = services.offset(skip).limit(limit).all()
    result = []
    for service in services:
        service_data = jsonable_encoder(service)
        service_data["organization_name"] = org.name if org else None
        result.append(service_data)
    return result


@router.get("/{service_id}", response_model=dict)
async def read_service(
    service_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Get service information by ID"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found, cannot get information",
        )
    
    # Get organization information
    organization = db.query(Organization).filter(Organization.id == service.organization_id).first()
    
    # Return service information, including organization name
    result = jsonable_encoder(service)
    result["organization_name"] = organization.name if organization else None
    
    return result


@router.put("/{service_id}", response_model=dict)
async def update_service(
    *,
    db: Session = Depends(deps.get_db),
    service_id: int,
    service_in: schemas.ServiceUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """Update service information"""
    service = crud.service.get(db, id=service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )
        
    # Update service information
    service = crud.service.update_service(
        db=db,
        service_id=service_id,
        obj_in=service_in
    )
    
    # Create log for service update
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        log_type=LogType.SERVICE_ACCESS,
        action="Update service",
        details=f"User {current_user.email} updated service {service.name}"
    )
    
    # Get organization information
    organization = db.query(Organization).filter(Organization.id == service.organization_id).first()
    
    # Return updated service information
    result = jsonable_encoder(service)
    result["organization_name"] = organization.name if organization else None
    
    return result


@router.delete("/{service_id}", response_model=dict)
async def delete_service(
    *,
    db: Session = Depends(deps.get_db),
    service_id: int,
    current_user: User = Depends(deps.get_current_o_convener),
) -> Any:
    """Delete service"""
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found",
        )
    
    # Get organization information (for logging)
    organization = db.query(Organization).filter(Organization.id == service.organization_id).first()
    organization_id = service.organization_id
    service_name = service.name
    
    # Delete service
    db.delete(service)
    db.commit()
    
    # Create log for service deletion
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=organization_id,
        log_type=LogType.SERVICE_ACCESS,
        action="Delete service",
        details=f"User {current_user.email} deleted service {service_name}"
    )
    
    # Return deletion result
    return {
        "id": service_id,
        "message": "Service deleted successfully",
        "organization_name": organization.name if organization else None
    }










