from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
import enum

from app.db.session import Base

tz_utc_8 = timezone(timedelta(hours=8))

class PaymentType(str, enum.Enum):
    TRANSFER = "transfer"
    PAYPAL = "paypal"
    WECHAT = "wechat"
    ALIPAY = "alipay"
    CREDIT_CARD = "credit_card"

class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    payment_type = Column(Enum(PaymentType, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    account_name = Column(String(255), nullable=False)
    account_number = Column(String(255), nullable=False)
    bank = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(tz_utc_8))
    updated_at = Column(DateTime, default=datetime.now(tz_utc_8), onupdate=datetime.now(tz_utc_8))
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    # 关系
    transfers = relationship("Transfer", back_populates="to_bank_account")


class Transfer(Base):
    __tablename__ = "transfers"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_bank_account_id = Column(Integer, ForeignKey("payments.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="RMB", nullable=False)
    status = Column(Enum(PaymentStatus, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    transaction_id = Column(String(255), nullable=True)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now(tz_utc_8))
    updated_at = Column(DateTime, default=datetime.now(tz_utc_8), onupdate=datetime.now(tz_utc_8))
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    # 关系
    organization = relationship("Organization", back_populates="transfers")
    from_user = relationship("User", back_populates="transfers")
    to_bank_account = relationship("Payment", back_populates="transfers")