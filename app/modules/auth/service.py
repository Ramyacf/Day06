from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.config import settings
from app.core.security import (
    create_access_token,
    create_password_reset_token,
    hash_password,
    hash_reset_token,
    verify_password,
)
from app.modules.auth import repository
from app.modules.auth.schemas import (
    ForgotPasswordResponse,
    LoginResponse,
    ResetPasswordResponse,
    SignupResponse,
    VerifyEmailResponse,
)


def signup(
    db: Session,
    email: str,
    full_name: str,
    password: str,
    phone_number: str | None = None,
) -> SignupResponse:
    existing_user = repository.get_user_by_email(
        db=db,
        email=email,
    )

    if existing_user:
        raise ValueError("A user with this email already exists.")

    password_hash = hash_password(password)

    user = repository.create_user(
        db=db,
        organization_id=None,
        email=email,
        full_name=full_name,
        password_hash=password_hash,
        phone_number=phone_number,
        department=None,
        employee_id=None,
    )

    raw_token = create_password_reset_token()
    token_hash = hash_reset_token(raw_token)

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.email_verification_token_expire_minutes
    )

    repository.create_email_verification_token(
        db=db,
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    db.commit()
    db.refresh(user)

    if settings.environment.lower() == "local":
        print("=" * 70)
        print("EMAIL VERIFICATION TOKEN")
        print(f"Email: {user.email}")
        print(f"Token: {raw_token}")
        print(f"Expires: {expires_at}")
        print("=" * 70)

    return SignupResponse(
        id=user.id,
        organization_id=user.organization_id,
        email=user.email,
        full_name=user.full_name,
        phone_number=user.phone_number,
        department=user.department,
        employee_id=user.employee_id,
        status=user.status,
        is_active=user.is_active,
        email_verified=user.email_verified,
        message="Signup successful. Please verify your email.",
    )


def verify_email(
    db: Session,
    token: str,
) -> VerifyEmailResponse:
    token_hash = hash_reset_token(token)

    verification_token = repository.get_email_verification_token(
        db=db,
        token_hash=token_hash,
    )

    if verification_token is None:
        raise ValueError("Invalid email verification token.")

    if verification_token.used_at is not None:
        raise ValueError("Email verification token has already been used.")

    now = datetime.now(timezone.utc)
    expires_at = verification_token.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < now:
        raise ValueError("Email verification token has expired.")

    user = repository.get_user_by_id(
        db=db,
        user_id=verification_token.user_id,
    )

    if user is None:
        raise ValueError("User not found.")

    if user.email_verified:
        raise ValueError("Email is already verified.")

    user.email_verified = True
    user.is_active = True
    user.status = "ACTIVE"

    repository.mark_email_verification_token_used(
        db=db,
        token=verification_token,
    )

    db.commit()
    db.refresh(user)

    return VerifyEmailResponse(
        message="Email verified successfully.",
        email_verified=user.email_verified,
        status=user.status,
        is_active=user.is_active,
    )


def login(
    db: Session,
    email: str,
    password: str,
) -> LoginResponse:
    user = repository.get_user_by_email(
        db=db,
        email=email,
    )

    if user is None:
        raise ValueError("Invalid email or password.")

    if not user.email_verified:
        raise ValueError("Please verify your email before logging in.")

    if not user.is_active:
        raise ValueError("User account is inactive.")

    if not user.password_hash:
        raise ValueError("Password is not configured for this account.")

    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password.")

    access_token = create_access_token(
        subject=str(user.id),
    )

    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user_id=user.id,
        organization_id=user.organization_id,
        email=user.email,
        full_name=user.full_name,
        status=user.status,
    )


def forgot_password(
    db: Session,
    email: str,
) -> ForgotPasswordResponse:
    user = repository.get_user_by_email(
        db=db,
        email=email,
    )

    if user is None:
        return ForgotPasswordResponse(
            message="If the email exists, a password reset link will be sent.",
        )

    raw_token = create_password_reset_token()
    token_hash = hash_reset_token(raw_token)

    expires_at = datetime.now(timezone.utc) + timedelta(
        minutes=settings.password_reset_token_expire_minutes
    )

    repository.create_password_reset_token(
        db=db,
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
    )

    db.commit()

    if settings.environment.lower() == "local":
        print("=" * 70)
        print("PASSWORD RESET TOKEN")
        print(f"Email: {user.email}")
        print(f"Token: {raw_token}")
        print(f"Expires: {expires_at}")
        print("=" * 70)

    return ForgotPasswordResponse(
        message="If the email exists, a password reset link will be sent.",
    )


def reset_password(
    db: Session,
    token: str,
    new_password: str,
) -> ResetPasswordResponse:
    token_hash = hash_reset_token(token)

    reset_token = repository.get_password_reset_token(
        db=db,
        token_hash=token_hash,
    )

    if reset_token is None:
        raise ValueError("Invalid password reset token.")

    if reset_token.used_at is not None:
        raise ValueError("Password reset token has already been used.")

    now = datetime.now(timezone.utc)
    expires_at = reset_token.expires_at

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at < now:
        raise ValueError("Password reset token has expired.")

    user = repository.get_user_by_id(
        db=db,
        user_id=reset_token.user_id,
    )

    if user is None:
        raise ValueError("User not found.")

    user.password_hash = hash_password(new_password)

    repository.mark_password_reset_token_used(
        db=db,
        token=reset_token,
    )

    db.commit()

    return ResetPasswordResponse(
        message="Password reset successfully.",
    )