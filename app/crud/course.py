from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from app.crud.base import CRUDBase
from app.models.course import Course, CourseSchedule
from app.models.enums import PermissionLevel
from app.models.user import UserRole, User

tz_utc_8 = timezone(timedelta(hours=8))

class CRUDCourse(CRUDBase[Course, Dict[str, Any], Dict[str, Any]]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[Course]:
        """通过课程代码获取课程"""
        return db.query(Course).filter(Course.code == code).first()
    
    def get_by_organization(self, db: Session, *, organization_id: int, skip: int = 0, limit: int = 100) -> List[Course]:
        """获取组织的所有课程"""
        return db.query(Course).filter(Course.organization_id == organization_id).offset(skip).limit(limit).all()
    
    def get_active_courses(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Course]:
        """获取所有活跃课程"""
        return db.query(Course).filter(Course.is_active == True).offset(skip).limit(limit).all()
    
    def get_public_courses(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Course]:
        """获取所有公开课程"""
        return db.query(Course).filter(
            Course.is_active == True,
            Course.is_public == True
        ).offset(skip).limit(limit).all()
    
    def get_organization_public_courses(self, db: Session, *, organization_id: int, skip: int = 0, limit: int = 100) -> List[Course]:
        """获取组织的公开课程"""
        return db.query(Course).filter(
            Course.organization_id == organization_id,
            Course.is_active == True,
            Course.is_public == True
        ).offset(skip).limit(limit).all()
    
    def get_user_courses(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> List[Course]:
        """获取用户创建的课程"""
        return db.query(Course).filter(
            Course.created_by == user_id
        ).offset(skip).limit(limit).all()
    
    def get_by_department(self, db: Session, *, organization_id: int, department: str, skip: int = 0, limit: int = 100) -> List[Course]:
        """获取指定院系的课程"""
        return db.query(Course).filter(
            Course.organization_id == organization_id,
            Course.department == department
        ).offset(skip).limit(limit).all()
    
    def get_by_semester(self, db: Session, *, organization_id: int, semester: str, year: int, skip: int = 0, limit: int = 100) -> List[Course]:
        """获取指定学期的课程"""
        return db.query(Course).filter(
            Course.organization_id == organization_id,
            Course.semester == semester,
            Course.year == year
        ).offset(skip).limit(limit).all()
    
    def create_course(self, db: Session, *, obj_in: Dict[str, Any], user_id: int) -> Course:
        """创建新课程"""
        course_data = {
            **obj_in,
            "created_by": user_id,
            "created_at": datetime.now(tz_utc_8),
            "updated_at": datetime.now(tz_utc_8)
        }
        
        course = Course(**course_data)
        db.add(course)
        db.commit()
        db.refresh(course)
        return course
    
    def update_course(self, db: Session, *, course_id: int, obj_in: Dict[str, Any]) -> Optional[Course]:
        """更新课程信息"""
        course = self.get(db, id=course_id)
        if not course:
            return None
        
        obj_in["updated_at"] = datetime.now(tz_utc_8)
        return self.update(db, db_obj=course, obj_in=obj_in)
    
    def can_create_course(self, db: Session, *, user_id: int, organization_id: int) -> bool:
        """检查用户是否有权限创建课程"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        # 检查用户是否属于组织
        if user.organization_id != organization_id:
            return False
        
        # 检查用户是否有权限（O-Convener 或 PermissionLevel 3）
        is_convener = user.role == UserRole.O_CONVENER
        has_permission_level_3 = user.permission_level == PermissionLevel.PRIVATE_DATA_PROVIDER
        
        return is_convener or has_permission_level_3
    
    def can_update_course(self, db: Session, *, user_id: int, course_id: int) -> bool:
        """检查用户是否有权限更新课程"""
        course = self.get(db, id=course_id)
        if not course:
            return False
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        # 检查用户是否是课程创建者
        if user.id == course.created_by:
            return True
        
        # 检查用户是否是组织的 O-Convener
        if user.organization_id == course.organization_id and user.role == UserRole.O_CONVENER:
            return True
        
        return False
    
    def can_delete_course(self, db: Session, *, user_id: int, course_id: int) -> bool:
        """检查用户是否有权限删除课程"""
        return self.can_update_course(db, user_id=user_id, course_id=course_id)
    
    def can_view_course(self, db: Session, *, user_id: int, course_id: int) -> bool:
        """检查用户是否有权限查看课程"""
        course = self.get(db, id=course_id)
        print(f"course: {course}")
        if not course:
            return False
        if course.is_public:
            return True
        # 非公开课程，只有同组织成员可看
        user = db.query(User).filter(User.id == user_id).first()
        return user and user.organization_id == course.organization_id


class CRUDCourseSchedule(CRUDBase[CourseSchedule, Dict[str, Any], Dict[str, Any]]):
    def get_by_course(self, db: Session, *, course_id: int) -> List[CourseSchedule]:
        """获取课程的所有课表"""
        return db.query(CourseSchedule).filter(CourseSchedule.course_id == course_id).all()
    
    def create_schedule(self, db: Session, *, course_id: int, day_of_week: int, 
                       start_time: str, end_time: str, location: str) -> CourseSchedule:
        """创建课程表"""
        schedule_data = {
            "course_id": course_id,
            "day_of_week": day_of_week,
            "start_time": start_time,
            "end_time": end_time,
            "location": location,
            "is_active": True
        }
        
        schedule = CourseSchedule(**schedule_data)
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        return schedule
    
    def update_schedule(self, db: Session, *, schedule_id: int, obj_in: Dict[str, Any]) -> Optional[CourseSchedule]:
        """更新课程表"""
        schedule = self.get(db, id=schedule_id)
        if not schedule:
            return None
        
        return self.update(db, db_obj=schedule, obj_in=obj_in)


course = CRUDCourse(Course)
course_schedule = CRUDCourseSchedule(CourseSchedule)