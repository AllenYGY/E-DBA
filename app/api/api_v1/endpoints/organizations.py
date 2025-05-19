from typing import Any, List
import os

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app import models, schemas, crud
from app.api import deps


router = APIRouter()


@router.get("/", response_model=schemas.OrganizationListResponse)
async def read_organizations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    search: str = Query(None, description="Search organizations by name, full name, or email domain"),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get organization list , supports pagination and multi-field search
    """
    query = db.query(models.Organization)
    if search:
        query = query.filter(
            or_(
                models.Organization.name.ilike(f"%{search}%"),
                models.Organization.full_name.ilike(f"%{search}%"),
                models.Organization.email_domain.ilike(f"%{search}%"),
            )
        )
    total = query.count()
    organizations = query.offset(skip).limit(limit).all()
    return {"items": organizations, "total": total}


class OrganizationCreateWithBank(schemas.OrganizationCreate):
    account_name: str
    account_number: str
    bank: str
    password: str

@router.get("/my-organization", response_model=schemas.Organization)
async def read_my_organization(
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get the organization information of the current user"""
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not a member of any organization",
        )
    organization = db.query(models.Organization).filter(models.Organization.id == current_user.organization_id).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found, cannot get organization information",
        )
    return organization


@router.get("/{organization_id}", response_model=schemas.Organization)
async def read_organization(
    organization_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get organization information by ID"""
    organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )
    
    # Check permission: only organization members, organizers, or admins can view organization information
    if current_user.organization_id != organization_id and current_user.role not in [
        models.UserRole.E_ADMIN, models.UserRole.T_ADMIN, models.UserRole.SENIOR_E_ADMIN
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied, cannot view other organization information",
        )
    
    return organization


@router.put("/{organization_id}", response_model=schemas.Organization)
async def update_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: int,
    organization_in: schemas.OrganizationUpdate,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """update organization information"""
    organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )
    
    # Check permission: only organizers or admins can update organization information
    is_admin = current_user.role in [models.UserRole.E_ADMIN, models.UserRole.T_ADMIN, models.UserRole.SENIOR_E_ADMIN]
    is_convener = current_user.id == organization.convener_id
    
    if not (is_admin or is_convener):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied, only the organizer or admin can update the organization information",
        )
    
    # Admins can update all fields, organizers can only update basic information
    if not is_admin:
        # Remove fields that organizers cannot update
        if hasattr(organization_in, "is_verified"):
            delattr(organization_in, "is_verified")
        if hasattr(organization_in, "is_active"):
            delattr(organization_in, "is_active")
        if hasattr(organization_in, "convener_id"):
            delattr(organization_in, "convener_id")
    
    organization = crud.organization.update(db, db_obj=organization, obj_in=organization_in)
    
    # Record organization update log
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=organization.id,
        log_type=models.LogType.ORGANIZATION,
        action="update organization information",
        details=f"User {current_user.email} updated the information of organization {organization.name}"
    )
    
    return organization


@router.post("/{organization_id}/upload-verification", response_model=schemas.Organization)
async def upload_verification_document(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: int,
    file: UploadFile = File(...),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """Upload organization verification document"""
    organization = crud.organization.get(db, id=organization_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )
    
    # Check permission: only organizers or admins can upload verification document
    if current_user.id != organization.convener_id and current_user.role not in [
        models.UserRole.E_ADMIN, models.UserRole.SENIOR_E_ADMIN, models.UserRole.T_ADMIN
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied, cannot upload verification document",
        )
    
    # Check file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported",
        )
    
    # Generate file storage path
    file_path = f"uploads/verification/{organization_id}_{file.filename}"
    
    # Automatically create directory
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File saving failed: {str(e)}",
        )
    
    # Update organization verification document path
    organization = crud.organization.update(
        db,
        db_obj=organization,
        obj_in={"verification_document": file_path}
    )
    
    # Create or update verification status record
    verification_status = crud.verification_status.get_by_organization(db, organization_id=organization_id)
    if not verification_status:
        verification_status = crud.verification_status.create_verification_status(db, organization_id=organization_id)
    
    # Record file upload log
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=organization.id,
        log_type=models.LogType.ORGANIZATION,
        action="Upload verification document",
        details=f"User {current_user.email} uploaded verification document for organization {organization.name}"
    )
    
    return organization


@router.get("/{organization_id}/members", response_model=List[schemas.User])
async def read_organization_members(
    organization_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get organization member list"""
    organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )
    
    # Check permission: only organization members, organizers, or admins can view organization members
    is_admin = current_user.role in [models.UserRole.E_ADMIN, models.UserRole.T_ADMIN, models.UserRole.SENIOR_E_ADMIN]
    is_member = current_user.organization_id == organization_id
    is_convener = current_user.id == organization.convener_id
    
    if not (is_admin or is_member or is_convener):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied, cannot view organization members",
        )
    
    members = db.query(models.User).filter(models.User.organization_id == organization_id).offset(skip).limit(limit).all()
    return members