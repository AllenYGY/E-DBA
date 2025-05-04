from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from app.crud.base import CRUDBase
from app.models.payment import Payment, PaymentStatus, PaymentType, Transfer

tz_utc_8 = timezone(timedelta(hours=8))

class CRUDPayment(CRUDBase[Payment, Dict[str, Any], Dict[str, Any]]):
    def get_by_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> List[Payment]:
        """获取用户的支付记录"""
        return db.query(Payment).filter(
            Payment.user_id == user_id,
            Payment.is_deleted == False
        ).order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_organization(self, db: Session, *, organization_id: int, skip: int = 0, limit: int = 100) -> List[Payment]:
        """获取组织的支付记录"""
        return db.query(Payment).filter(
            Payment.organization_id == organization_id,
            Payment.is_deleted == False
        ).order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()
    
    
    def get_by_type(self, db: Session, *, payment_type: PaymentType, skip: int = 0, limit: int = 100) -> List[Payment]:
        """获取指定类型的支付记录"""
        return db.query(Payment).filter(
            Payment.payment_type == payment_type,
            Payment.is_deleted == False
        ).order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()
    
    def create_payment(self, db: Session, *,
                       organization_id: int, payment_type: PaymentType, 
                        account_name: str, account_number: str,
                         password: str, bank: str) -> Payment:
        """创建支付记录"""
        payment_data = {
            "organization_id": organization_id,
            "payment_type": payment_type,
            "account_name": account_name,
            "account_number": account_number,
            "password": password,
            "bank": bank,
            "is_default": True,
            "is_active": True,
            "created_at": datetime.now(tz_utc_8),
            "updated_at": datetime.now(tz_utc_8),
            "is_deleted": False
        }
        
        payment = Payment(**payment_data)
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return payment
    
    def update_payment_status(self, db: Session, *, payment_id: int, status: PaymentStatus, 
                            transaction_id: Optional[str] = None) -> Optional[Payment]:
        """更新支付状态"""
        payment = self.get(db, id=payment_id)
        if not payment:
            return None
        
        update_data = {
            "status": status,
            "updated_at": datetime.now(tz_utc_8)
        }
        
        if transaction_id:
            update_data["transaction_id"] = transaction_id
        
        return self.update(db, db_obj=payment, obj_in=update_data)
    
    def soft_delete(self, db: Session, *, payment_id: int) -> Optional[Payment]:
        """软删除支付记录"""
        payment = self.get(db, id=payment_id)
        if not payment:
            return None
        
        update_data = {
            "is_deleted": True,
            "deleted_at": datetime.now(tz_utc_8),
            "updated_at": datetime.now(tz_utc_8)
        }
        
        return self.update(db, db_obj=payment, obj_in=update_data)

class CRUDTransfer(CRUDBase[Transfer, Dict[str, Any], Dict[str, Any]]):
    def create_transfer(self, db: Session, *,
                       organization_id: int,
                       from_user_id: int,
                       to_bank_account_id: int,
                       amount: float,
                       currency: str = "RMB",
                       status: PaymentStatus = PaymentStatus.SUCCESS,
                       transaction_id: Optional[str] = None,
                       description: Optional[str] = None) -> Transfer:
        """创建转账记录"""
        transfer_data = {
            "organization_id": organization_id,
            "from_user_id": from_user_id,
            "to_bank_account_id": to_bank_account_id,
            "amount": amount,
            "currency": currency,
            "status": status,
            "transaction_id": transaction_id,
            "description": description,
            "created_at": datetime.now(tz_utc_8),
            "updated_at": datetime.now(tz_utc_8),
            "is_deleted": False
        }
        
        transfer = Transfer(**transfer_data)
        db.add(transfer)
        db.commit()
        db.refresh(transfer)
        return transfer
    
    def get_by_organization(self, db: Session, *, organization_id: int, skip: int = 0, limit: int = 100) -> List[Transfer]:
        """获取组织的转账记录"""
        return db.query(Transfer).filter(
            Transfer.organization_id == organization_id,
            Transfer.is_deleted == False
        ).order_by(Transfer.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> List[Transfer]:
        """获取用户的转账记录"""
        return db.query(Transfer).filter(
            Transfer.from_user_id == user_id,
            Transfer.is_deleted == False
        ).order_by(Transfer.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_bank_account(self, db: Session, *, bank_account_id: int, skip: int = 0, limit: int = 100) -> List[Transfer]:
        """获取银行账户的转账记录"""
        return db.query(Transfer).filter(
            Transfer.to_bank_account_id == bank_account_id,
            Transfer.is_deleted == False
        ).order_by(Transfer.created_at.desc()).offset(skip).limit(limit).all()
    
    def update_transfer_status(self, db: Session, *, transfer_id: int, status: PaymentStatus,
                             transaction_id: Optional[str] = None) -> Optional[Transfer]:
        """更新转账状态"""
        transfer = self.get(db, id=transfer_id)
        if not transfer:
            return None
        
        update_data = {
            "status": status,
            "updated_at": datetime.now(tz_utc_8)
        }
        
        if transaction_id:
            update_data["transaction_id"] = transaction_id
        
        return self.update(db, db_obj=transfer, obj_in=update_data)
    
    def soft_delete(self, db: Session, *, transfer_id: int) -> Optional[Transfer]:
        """软删除转账记录"""
        transfer = self.get(db, id=transfer_id)
        if not transfer:
            return None
        
        update_data = {
            "is_deleted": True,
            "deleted_at": datetime.now(tz_utc_8),
            "updated_at": datetime.now(tz_utc_8)
        }
        
        return self.update(db, db_obj=transfer, obj_in=update_data)

payment = CRUDPayment(Payment)
transfer = CRUDTransfer(Transfer)