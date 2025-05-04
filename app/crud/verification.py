from typing import Optional, List, Union
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.verification import VerificationStatus
from app.schemas.verification import (
    VerificationStatusCreate,
    EAdminVerificationStatusUpdate,
    SeniorEAdminVerificationStatusUpdate
)

tz_utc_8 = timezone(timedelta(hours=8))

class CRUDVerificationStatus(CRUDBase[VerificationStatus, VerificationStatusCreate, Union[EAdminVerificationStatusUpdate, SeniorEAdminVerificationStatusUpdate]]):
    def get_by_organization(self, db: Session, *, organization_id: int) -> Optional[VerificationStatus]:
        """获取组织的验证状态"""
        return db.query(VerificationStatus).filter(VerificationStatus.organization_id == organization_id).first()
    
    def get_pending_verifications(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[VerificationStatus]:
        """获取待处理的验证请求"""
        return db.query(VerificationStatus).filter(
            VerificationStatus.e_admin_approved == False,
            VerificationStatus.senior_approved == False
        ).offset(skip).limit(limit).all()
    
    def create_verification_status(self, db: Session, *, organization_id: int) -> VerificationStatus:
        """创建组织验证状态记录"""
        db_obj = VerificationStatus(
            organization_id=organization_id,
            e_admin_approved=False,
            senior_approved=False,
            submitted_at=datetime.now()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def e_admin_review(self, db: Session, *, organization_id: int, e_admin_id: int, 
                      approved: bool, comment: Optional[str] = None) -> VerificationStatus:
        """E-Admin审核"""
        try:
            # 获取验证状态
            verification = self.get_by_organization(db, organization_id=organization_id)
            if not verification:
                # 如果不存在，创建新的验证状态
                verification = self.create_verification_status(db, organization_id=organization_id)
            
            print(f"Processing verification status: {verification.id}")
            
            # 更新验证状态
            verification.e_admin_id = e_admin_id
            verification.e_admin_approved = approved
            verification.e_admin_comment = comment
            verification.e_admin_reviewed_at = datetime.now(tz_utc_8)
            
            print(f"Updated verification state: e_admin_id={verification.e_admin_id}, approved={verification.e_admin_approved}")
            
            # 保存更改
            db.add(verification)
            db.commit()
            db.refresh(verification)
            
            print("E-admin review updated successfully")
            return verification
            
        except Exception as e:
            print(f"Error in e_admin_review: {str(e)}")
            db.rollback()
            raise
    
    def senior_admin_review(self, db: Session, *, organization_id: int, senior_e_admin_id: int, 
                           approved: bool, comment: Optional[str] = None) -> VerificationStatus:
        """Senior E-Admin审核"""
        try:
            # 获取验证状态
            verification = self.get_by_organization(db, organization_id=organization_id)
            if not verification:
                # 如果不存在，创建新的验证状态
                verification = self.create_verification_status(db, organization_id=organization_id)
            
            print(f"Processing verification status: {verification.id}")
            
            # 更新验证状态
            verification.senior_e_admin_id = senior_e_admin_id
            verification.senior_approved = approved
            verification.senior_comment = comment
            verification.senior_reviewed_at = datetime.now(tz_utc_8)
            
            print(f"Updated verification state: senior_e_admin_id={verification.senior_e_admin_id}, approved={verification.senior_approved}")
            
            # 保存更改
            db.add(verification)
            db.commit()
            db.refresh(verification)
            
            print("Senior E-admin review updated successfully")
            return verification
            
        except Exception as e:
            print(f"Error in senior_admin_review: {str(e)}")
            db.rollback()
            raise

verification_status = CRUDVerificationStatus(VerificationStatus) 