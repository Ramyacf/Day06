from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.organization import Organization
from app.db.models.user import User
from app.db.models.email_verification_token import EmailVerificationToken
from app.db.models.password_reset_token import PasswordResetToken


def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:
    return db.scalar(
        select(User).where(
            User.email == email.lower(),
        )
    )


def get_user_by_id(
    db: Session,
    user_id: UUID,
) -> User | None:
    return db.get(User, user_id)


def get_organization(
    db: Session,
    organization_id: UUID,
) -> Organization | None:
    return db.get(Organization, organization_id)


def create_user(
    db: Session,
    organization_id: UUID | None,
    email: str,
    full_name: str,
    password_hash: str,
    phone_number: str | None = None,
    department: str | None = None,
    employee_id: str | None = None,
) -> User:
    user = User(
        organization_id=organization_id,
        email=email.lower(),
        full_name=full_name,
        password_hash=password_hash,
        phone_number=phone_number,
        department=department,
        employee_id=employee_id,
        status="PENDING_VERIFICATION",
        is_active=False,
        email_verified=False,
    )

    db.add(user)
    db.flush()

    return user


def create_email_verification_token(
    db: Session,
    user_id: UUID,
    token_hash: str,
    expires_at: datetime,
) -> EmailVerificationToken:
    token = EmailVerificationToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    db.add(token)
    db.flush()

    return token


def get_email_verification_token(
    db: Session,
    token_hash: str,
) -> EmailVerificationToken | None:
    return db.scalar(
        select(EmailVerificationToken).where(
            EmailVerificationToken.token_hash == token_hash
        )
    )


def mark_email_verification_token_used(
    db: Session,
    token: EmailVerificationToken,
) -> None:
    token.used_at = datetime.now(timezone.utc)


def create_password_reset_token(
    db: Session,
    user_id: UUID,
    token_hash: str,
    expires_at: datetime,
) -> PasswordResetToken:
    token = PasswordResetToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    db.add(token)
    db.flush()

    return token


def get_password_reset_token(
    db: Session,
    token_hash: str,
) -> PasswordResetToken | None:
    return db.scalar(
        select(PasswordResetToken).where(
            PasswordResetToken.token_hash == token_hash
        )
    )


def mark_password_reset_token_used(
    db: Session,
    token: PasswordResetToken,
) -> None:
    token.used_at = datetime.now(timezone.utc)