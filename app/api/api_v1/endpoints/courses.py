from typing import Any, List

from fastapi import APIRouter,Depends, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.api import deps
from app.models.log import LogType

router = APIRouter()


@router.get("/search/", response_model=dict)
async def search_courses(
    db: Session = Depends(deps.get_db),
    keyword: str = Query(None, description="搜索关键词"),
    organization_id: int = Query(None, description="组织ID"),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    print("search_courses called")  
    query = db.query(models.Course).filter(models.Course.is_public == True)
    if keyword:
        query = query.filter(
            (models.Course.title.ilike(f"%{keyword}%")) |
            (models.Course.description.ilike(f"%{keyword}%"))
        )
    if organization_id:
        query = query.filter(models.Course.organization_id == organization_id)
    total = query.count()
    courses = query.offset(skip).limit(limit).all()
    result = []
    for course in courses:
        course_data = jsonable_encoder(course)
        organization = db.query(models.Organization).filter(models.Organization.id == course.organization_id).first()
        course_data["organization_name"] = organization.name if organization else None
        result.append(course_data)
    return {"total": total, "items": result}


@router.get("/", response_model=List[schemas.CourseWithOrganization])
async def read_courses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get course list (all users can access)"""
    # Query all public courses
    courses = crud.course.get_public_courses(db, skip=skip, limit=limit)
    
    # Convert to dictionary list, including organization information
    result = []
    for course in courses:
        course_data = jsonable_encoder(course)
        organization = db.query(models.Organization).filter(models.Organization.id == course.organization_id).first()
        course_data["organization_name"] = organization.name if organization else None
        result.append(course_data)
    
    return result


@router.post("/", response_model=schemas.CourseWithOrganization)
async def create_course(
    *,
    db: Session = Depends(deps.get_db),
    course_in: schemas.CourseCreate,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """Create a new course (need O-Convener permission or PermissionLevel is 3)"""
    # Check user permission
    if not crud.course.can_create_course(db, user_id=current_user.id, organization_id=current_user.organization_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied, need O-Convener permission or PermissionLevel is 3",
        )
    
    # Check if the user belongs to the organization
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not a member of any organization, cannot create a course",
        )
    
    # Check if the organization has been verified
    organization = db.query(models.Organization).filter(models.Organization.id == current_user.organization_id).first()
    if not organization.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The organization has not been verified, cannot create a course",
        )
    
    # Create course
    course_data = course_in.dict()
    course_data["organization_id"] = current_user.organization_id
    course_data["created_by"] = current_user.id
    course_data["is_active"] = True
    print(f"course_data: {course_data}")
    course = crud.course.create_course(db, obj_in=course_data, user_id=current_user.id)
    

    # print("log_type:", LogType.COURSE)
    
    # Record course creation log
    result = jsonable_encoder(course)
    result["organization_name"] = organization.name
    
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=course.organization_id,
        log_type=LogType.COURSE,
        action="Create Course",
        details=f"User {current_user.email} created a course {course.title} for organization {organization.name}"
    )
    
    return result


@router.get("/my-courses", response_model=List[schemas.CourseWithOrganization])
async def read_my_courses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get the list of courses created by the current user"""
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not a member of any organization",
        )
    
    # Query user created courses
    courses = crud.course.get_user_courses(db, user_id=current_user.id, skip=skip, limit=limit)
    
    # Get organization information
    organization = db.query(models.Organization).filter(models.Organization.id == current_user.organization_id).first()
    
    # Convert to dictionary list, including organization information
    result = []
    for course in courses:
        course_data = jsonable_encoder(course)
        course_data["organization_name"] = organization.name if organization else None
        result.append(course_data)
    
    return result


@router.get("/{course_id}", response_model=schemas.CourseWithOrganization)
async def read_course(
    course_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get course information by ID (all users can access)"""

    # Check access permission
    print(f"current_user.id: {current_user.id}, course_id: {course_id}")
    
    if not crud.course.can_view_course(db,user_id=current_user.id,course_id=course_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied, cannot view the course",
        )
    
    course = crud.course.get(db, id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found, please check if the course ID is correct",
        )
    
    # Get organization information
    organization = db.query(models.Organization).filter(models.Organization.id == course.organization_id).first()
    
    # Return course information, including organization name
    result = jsonable_encoder(course)
    result["organization_name"] = organization.name if organization else None
    
    return result


@router.put("/{course_id}", response_model=schemas.CourseWithOrganization)
async def update_course(
    *,
    db: Session = Depends(deps.get_db),
    course_id: int,
    course_in: schemas.CourseUpdate,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """Update course information (need O-Convener permission or the course creator)"""
    # Check permission
    if not crud.course.can_update_course(db, user_id=current_user.id, course_id=course_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied, only the coordinator of the course所属组织或课程创建者可以更新课程信息",
        )
    
    course = crud.course.get(db, id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    
    # Update course information
    course = crud.course.update_course(db, course_id=course_id, obj_in=course_in.dict(exclude_unset=True))
    
    # Get organization information
    organization = db.query(models.Organization).filter(models.Organization.id == course.organization_id).first()
    
    # Record course update log
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=course.organization_id,
        log_type=models.LogType.COURSE,
        action="Update Course Information",
        details=f"User {current_user.email} updated the information of course {course.title}"
    )
    
    # Return course information, including organization name
    result = {
        "id": course.id,
        "title": course.title,
        "description": course.description,
        "credits": course.credits,
        "is_public": course.is_public,
        "organization_id": course.organization_id,
        "created_by": course.created_by,
        "is_active": course.is_active,
        "created_at": course.created_at,
        "updated_at": course.updated_at,
        "organization_name": organization.name if organization else None
    }
    return result


@router.delete("/{course_id}", response_model=schemas.CourseWithOrganization)
async def delete_course(
    *,
    db: Session = Depends(deps.get_db),
    course_id: int,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete Course
    """
    # Check permission
    if not crud.course.can_delete_course(db, user_id=current_user.id, course_id=course_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied, only the coordinator of the course所属组织或课程创建者可以删除课程",
        )
    
    course = crud.course.get(db, id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found",
        )
    
    # Get organization information (for logging)
    organization = db.query(models.Organization).filter(models.Organization.id == course.organization_id).first()
    organization_id = course.organization_id
    course_title = course.title
    
    # Delete course
    db.delete(course)
    db.commit()
    
    # Record course deletion log
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=organization_id,
        log_type=models.LogType.COURSE,
        action="Delete Course",
        details=f"User {current_user.email} deleted course {course_title}"
    )
    
    # Return deletion result
    result = jsonable_encoder(course)
    result["organization_name"] = organization.name if organization else None
    result["message"] = "Course deleted successfully"
    
    return result