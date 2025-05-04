from typing import Any, List

from fastapi import APIRouter,Depends, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.api import deps
from app.models.log import LogType

router = APIRouter()


@router.get("/", response_model=List[schemas.CourseWithOrganization])
async def read_courses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """获取课程列表（所有用户可访问）"""
    # 查询所有公开课程
    courses = crud.course.get_public_courses(db, skip=skip, limit=limit)
    
    # 转换为字典列表，包含组织信息
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
    """创建新课程（需要O-Convener权限或PermissionLevel为3）"""
    # 检查用户权限
    if not crud.course.can_create_course(db, user_id=current_user.id, organization_id=current_user.organization_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要O-Convener权限或PermissionLevel为3",
        )
    
    # 检查用户是否属于组织
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您不属于任何组织，无法创建课程",
        )
    
    # 检查组织是否已验证
    organization = db.query(models.Organization).filter(models.Organization.id == current_user.organization_id).first()
    if not organization.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="组织尚未通过验证，无法创建课程",
        )
    
    # 创建课程
    course_data = course_in.dict()
    course_data["organization_id"] = current_user.organization_id
    course_data["created_by"] = current_user.id
    course_data["is_active"] = True
    print(f"course_data: {course_data}")
    course = crud.course.create_course(db, obj_in=course_data, user_id=current_user.id)
    

    # print("log_type:", LogType.COURSE)
    
    # 记录课程创建日志
    result = jsonable_encoder(course)
    result["organization_name"] = organization.name
    
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=course.organization_id,
        log_type=LogType.COURSE,
        action="创建课程",
        details=f"用户 {current_user.email} 为组织 {organization.name} 创建了课程 {course.title}"
    )
    
    return result


@router.get("/my-courses", response_model=List[schemas.CourseWithOrganization])
async def read_my_courses(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """获取当前用户创建的课程列表"""
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="您不属于任何组织",
        )
    
    # 查询用户创建的课程
    courses = crud.course.get_user_courses(db, user_id=current_user.id, skip=skip, limit=limit)
    
    # 获取组织信息
    organization = db.query(models.Organization).filter(models.Organization.id == current_user.organization_id).first()
    
    # 转换为字典列表，包含组织信息
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
    """根据ID获取课程信息（所有用户可访问）"""

    # 检查访问权限
    print(f"current_user.id: {current_user.id}, course_id: {course_id}")
    
    if not crud.course.can_view_course(db,user_id=current_user.id,course_id=course_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，无法查看课程",
        )
    
    course = crud.course.get(db, id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在，请检查课程ID是否正确",
        )
    
    # 获取组织信息
    organization = db.query(models.Organization).filter(models.Organization.id == course.organization_id).first()
    
    # 返回课程信息，包含组织名称
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
    """更新课程信息（需要O-Convener权限或是课程创建者）"""
    # 检查权限
    if not crud.course.can_update_course(db, user_id=current_user.id, course_id=course_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，只有课程所属组织的协调人或课程创建者可以更新课程信息",
        )
    
    course = crud.course.get(db, id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在",
        )
    
    # 更新课程信息
    course = crud.course.update_course(db, course_id=course_id, obj_in=course_in.dict(exclude_unset=True))
    
    # 获取组织信息
    organization = db.query(models.Organization).filter(models.Organization.id == course.organization_id).first()
    
    # 记录课程更新日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=course.organization_id,
        log_type=models.LogType.COURSE,
        action="更新课程信息",
        details=f"用户 {current_user.email} 更新了课程 {course.title} 的信息"
    )
    
    # 返回课程信息，包含组织名称
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
    """删除课程（需要O-Convener权限或是课程创建者）"""
    # 检查权限
    if not crud.course.can_delete_course(db, user_id=current_user.id, course_id=course_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，只有课程所属组织的协调人或课程创建者可以删除课程",
        )
    
    course = crud.course.get(db, id=course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="课程不存在",
        )
    
    # 获取组织信息（用于日志记录）
    organization = db.query(models.Organization).filter(models.Organization.id == course.organization_id).first()
    organization_id = course.organization_id
    course_title = course.title
    
    # 删除课程
    db.delete(course)
    db.commit()
    
    # 记录课程删除日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=organization_id,
        log_type=models.LogType.COURSE,
        action="删除课程",
        details=f"用户 {current_user.email} 删除了课程 {course_title}"
    )
    
    # 返回删除结果
    result = jsonable_encoder(course)
    result["organization_name"] = organization.name if organization else None
    result["message"] = "课程已成功删除"
    
    return result


@router.get("/search/", response_model=List[schemas.CourseWithOrganization])
async def search_courses(
    db: Session = Depends(deps.get_db),
    keyword: str = Query(None, description="搜索关键词"),
    organization_id: int = Query(None, description="组织ID"),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """搜索课程，keyword 或 organization_id 必须至少有一个"""
    if not keyword and not organization_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="keyword 和 organization_id 至少需要填写一个"
        )
    query = db.query(models.Course).filter(models.Course.is_public == True)
    if keyword:
        query = query.filter(
            (models.Course.title.ilike(f"%{keyword}%")) |
            (models.Course.description.ilike(f"%{keyword}%"))
        )
    if organization_id:
        query = query.filter(models.Course.organization_id == organization_id)
    courses = query.offset(skip).limit(limit).all()
    result = []
    for course in courses:
        course_data = jsonable_encoder(course)
        organization = db.query(models.Organization).filter(models.Organization.id == course.organization_id).first()
        course_data["organization_name"] = organization.name if organization else None
        result.append(course_data)
    return result