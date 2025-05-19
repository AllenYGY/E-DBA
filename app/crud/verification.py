from typing import Optional, List, Union
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.verification import VerificationStatus,VerificationStatusEnum
from app.schemas.verification import (
    VerificationStatusCreate,
    EAdminVerificationStatusUpdate,
    SeniorEAdminVerificationStatusUpdate
)

tz_utc_8 = timezone(timedelta(hours=8))

class CRUDVerificationStatus(CRUDBase[VerificationStatus, VerificationStatusCreate, Union[EAdminVerificationStatusUpdate, SeniorEAdminVerificationStatusUpdate]]):
    def get_by_organization(self, db: Session, *, organization_id: int) -> Optional[VerificationStatus]:
        """
        Get the verification status for an organization.
        """
        return db.query(VerificationStatus).filter(VerificationStatus.organization_id == organization_id).first()
    
    def get_pending_verifications(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[VerificationStatus]:
        """
        Get pending verifications.
        """
        return db.query(VerificationStatus).filter(
            VerificationStatus.e_admin_approved == 'PENDING',
            VerificationStatus.senior_approved == 'PENDING'
        ).offset(skip).limit(limit).all()
    
    def create_verification_status(self, db: Session, *, organization_id: int) -> VerificationStatus:
        """
        Create a verification status record for an organization.
        """
        db_obj = VerificationStatus(
            organization_id=organization_id,
            e_admin_approved=VerificationStatusEnum.PENDING,
            senior_approved=VerificationStatusEnum.PENDING,
            submitted_at=datetime.now()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def e_admin_review(self, db: Session, *, organization_id: int, e_admin_id: int, 
                      approved: str, comment: Optional[str] = None) -> VerificationStatus:
        """E-Admin review"""
        try:
            # get verification status
            verification = self.get_by_organization(db, organization_id=organization_id)
            if not verification:
                # if not exist, create new verification status
                verification = self.create_verification_status(db, organization_id=organization_id)
            
            print(f"Processing verification status: {verification.id}")
            
            # update verification status
            verification.e_admin_id = e_admin_id
            verification.e_admin_approved = approved  # directly use the string passed in
            verification.e_admin_comment = comment
            verification.e_admin_reviewed_at = datetime.now(tz_utc_8)
            
            print(f"Updated verification state: e_admin_id={verification.e_admin_id}, approved={verification.e_admin_approved}")
            
            # save changes
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
                           approved: str, comment: Optional[str] = None) -> VerificationStatus:
        """Senior E-Admin review"""
        try:
            # get verification status
            verification = self.get_by_organization(db, organization_id=organization_id)
            if not verification:
                # if not exist, create new verification status
                verification = self.create_verification_status(db, organization_id=organization_id)
            
            print(f"Processing verification status: {verification.id}")
            
            # update verification status
            verification.senior_e_admin_id = senior_e_admin_id
            verification.senior_approved = approved  # directly use the string passed in
            verification.senior_comment = comment
            verification.senior_reviewed_at = datetime.now(tz_utc_8)
            
            print(f"Updated verification state: senior_e_admin_id={verification.senior_e_admin_id}, approved={verification.senior_approved}")
            
            # save changes
            db.add(verification)
            db.commit()
            db.refresh(verification)
            
            print("Senior E-admin review updated successfully")
            return verification
            
        except Exception as e:
            print(f"Error in senior_admin_review: {str(e)}")
            db.rollback()
            raise

    def get_by_status(self, db: Session, *, status: str, skip: int = 0, limit: int = 100) -> List[VerificationStatus]:
        """Get records by e_admin_approved status"""
        return db.query(VerificationStatus).filter(
            VerificationStatus.e_admin_approved == status
        ).offset(skip).limit(limit).all()

    def get_by_senior_status(self, db: Session, *, status: str, skip: int = 0, limit: int = 100) -> List[VerificationStatus]:
        """Get records by senior_approved status"""
        return db.query(VerificationStatus).filter(
            VerificationStatus.senior_approved == status
        ).offset(skip).limit(limit).all()

    def reset_e_admin_status(self, db: Session, *, organization_id: int) -> Optional[VerificationStatus]:
        """Reset e_admin_approved to PENDING"""
        verification = self.get_by_organization(db, organization_id=organization_id)
        if verification:
            verification.e_admin_approved = 'PENDING'
            db.add(verification)
            db.commit()
            db.refresh(verification)
        return verification

    def batch_update_status(self, db: Session, *, ids: list, status: str) -> int:
        """Batch update e_admin_approved status"""
        result = db.query(VerificationStatus).filter(VerificationStatus.id.in_(ids)).update(
            {VerificationStatus.e_admin_approved: status}, synchronize_session=False
        )
        db.commit()
        return result

    def is_approved(self, db: Session, *, organization_id: int) -> bool:
        """Check if the organization has been approved by e_admin"""
        verification = self.get_by_organization(db, organization_id=organization_id)
        return verification and verification.e_admin_approved == 'APPROVAL'

verification_status = CRUDVerificationStatus(VerificationStatus) 