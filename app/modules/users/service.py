from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.modules.users import repository


def get_user(
    db: Session,
    user_id: UUID,
    current_user,
):
    user = repository.get_user_by_id(
        db=db,
        user_id=user_id,
        organization_id=current_user.organization_id,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user