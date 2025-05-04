from sqlalchemy.orm import Session

from app import crud, schemas
from app.core.config import settings
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.db.session import SessionLocal
from app.models.service import ServiceType
from app.db import base  # noqa: F401

def init_db(db: Session) -> None:
    
    # 初始化 E-DBA 组织
    e_dba_org = crud.organization.get_by_name(db, name="E-DBA")
    if not e_dba_org:
        e_dba_org_in = schemas.OrganizationCreate(
            name="E-DBA",
            description="External Database Administration",
            email_domain="e-dba.org",
            is_verified=True,
            is_active=True
        )
        e_dba_org = crud.organization.create(db, obj_in=e_dba_org_in)
        print("E-DBA organization created successfully!")
    
    # 初始化外部数据库接口配置
    services_config = {
        ServiceType.STUDENT_VERIFICATION: {
            "name": settings.STUDENT_VERIFICATION_NAME,
            "path": settings.STUDENT_VERIFICATION_PATH,
            "method": settings.STUDENT_VERIFICATION_METHOD,
            "input_format": {
                "name": "string",
                "id": "string",
                "photo": "file"
            },
            "output_format": {
                "status": "string"
            },
            "service_type": ServiceType.STUDENT_VERIFICATION
        },
        ServiceType.STUDENT_GPA: {
            "name": settings.STUDENT_GPA_NAME,
            "description": settings.STUDENT_GPA_DESCRIPTION,
            "path": settings.STUDENT_GPA_PATH,
            "method": settings.STUDENT_GPA_METHOD,
            "input_format": {
                "name": "string",
                "id": "string"
            },
            "output_format": {
                "name": "string",
                "enroll_year": "string",
                "graduation_year": "string",
                "gpa": "float"
            },
            "service_type": ServiceType.STUDENT_GPA
        },
        ServiceType.PAPER_SHARING: {
            "name": settings.PAPER_SHARING_NAME,
            "description": settings.PAPER_SHARING_DESCRIPTION,
            "path": settings.PAPER_SHARING_PATH,
            "method": settings.PAPER_SHARING_METHOD,
            "input_format": {
                "keywords": "string"
            },
            "output_format": {
                "title": "string",
                "abstract": "string"
            },
            "service_type": ServiceType.PAPER_SHARING
        },
        ServiceType.PAPER_PDF: {
            "name": settings.PAPER_PDF_NAME,
            "description": settings.PAPER_PDF_DESCRIPTION,
            "path": settings.PAPER_PDF_PATH,
            "method": settings.PAPER_PDF_METHOD,
            "input_format": {
                "title": "string"
            },
            "output_format": {
                "file": "binary"
            }
        },
        ServiceType.BANK_AUTH: {
            "name": settings.BANK_AUTH_NAME,
            "description": settings.BANK_AUTH_DESCRIPTION,
            "path": settings.BANK_AUTH_PATH,
            "method": settings.BANK_AUTH_METHOD,
            "input_format": {
                "account_number": "string",
                "id_number": "string"
            },
            "output_format": {
                "status": "string",
                "account_name": "string"
            },
            "service_type": ServiceType.BANK_AUTH
        },
        ServiceType.BANK_TRANSFER: {
            "name": settings.BANK_TRANSFER_NAME,
            "description": settings.BANK_TRANSFER_DESCRIPTION,
            "path": settings.BANK_TRANSFER_PATH,
            "method": settings.BANK_TRANSFER_METHOD,
            "input_format": {
                "from_account": "string",
                "to_account": "string",
                "amount": "float"
            },
            "output_format": {
                "status": "string",
                "transaction_id": "string"
            },
            "service_type": ServiceType.BANK_TRANSFER
        }
    }

    for service_type, config in services_config.items():
        # 创建服务
        service = crud.service.get_by_type(db, service_type=service_type)
        if not service:
            service_in = schemas.ServiceCreate(
                name=config["name"],
                description=config["description"],
                service_type=service_type,
                is_public=True,
                fee_per_use=0.0,
                fee_unit="RMB",
                organization_id=e_dba_org.id
            )
            service = crud.service.create(db, obj_in=service_in)
        else:
            # 如果服务已存在，更新其组织 ID
            service.organization_id = e_dba_org.id
            db.add(service)
            db.commit()
            db.refresh(service)

        # 创建或更新API配置
        api_config = service.external_api_config
        if not api_config:
            api_config_in = schemas.ExternalApiConfigCreate(
                service_type=service_type,
                base_url=settings.EXTERNAL_SERVICE_BASE_URL,
                path=config["path"],
                route_prefix=config["route_prefix"],
                method=config["method"],
                input_format=config["input_format"],
                output_format=config["output_format"]
            )
            api_config = crud.service.create_api_config(db, service_id=service.id, obj_in=api_config_in)
        else:
            # 更新现有API配置的service_type
            api_config.service_type = service_type
            db.add(api_config)
        db.commit()
        db.refresh(api_config)

    # Create T-Admin
    t_admin = db.query(User).filter(User.email == settings.T_ADMIN_EMAIL).first()
    if not t_admin:
        t_admin = User(
            email=settings.T_ADMIN_EMAIL,
            username=settings.T_ADMIN_NAME,
            hashed_password=get_password_hash(settings.T_ADMIN_PASSWORD),
            role=UserRole.T_ADMIN,
            permission_level=3,
            is_active=True,
            balance=10000.0,
            organization_id=e_dba_org.id
        )
        db.add(t_admin)
        db.commit()
        db.refresh(t_admin)
        print("T-Admin account created successfully!")

    # Create E-Admin
    e_admin = db.query(User).filter(User.email == settings.E_ADMIN_EMAIL).first()
    if not e_admin:
        admin = User(
            email=settings.E_ADMIN_EMAIL,
            username=settings.E_ADMIN_NAME,
            hashed_password=get_password_hash(settings.E_ADMIN_PASSWORD),
            role=UserRole.E_ADMIN,
            permission_level=3,
            is_active=True,
            balance=10000.0,
            organization_id=e_dba_org.id
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        print("Default E-Admin account created successfully!")

    # Create Senior E-Admin
    senior_e_admin = db.query(User).filter(User.email == settings.SENIOR_E_ADMIN_EMAIL).first()
    if not senior_e_admin:
        senior_e_admin = User(
            email=settings.SENIOR_E_ADMIN_EMAIL,
            username=settings.SENIOR_E_NAME,
            hashed_password=get_password_hash(settings.SENIOR_E_ADMIN_PASSWORD),
            role=UserRole.SENIOR_E_ADMIN,
            permission_level=3,
            is_active=True,
            balance=10000.0,
            organization_id=e_dba_org.id
        )
        db.add(senior_e_admin)
        db.commit()
        db.refresh(senior_e_admin)
        print("Senior E-Admin account created successfully!")

    # 设置 E-DBA 组织的协调人为 T-Admin
    if e_dba_org and t_admin:
        e_dba_org.convener_id = t_admin.id
        db.add(e_dba_org)
        db.commit()
        print("Set T-Admin as E-DBA organization convener successfully!")

def main() -> None:
    db = SessionLocal()
    init_db(db)

if __name__ == "__main__":
    print("Initializing database...")
    main() 