from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.user import User


def get_user_by_id(
    db: Session,
    user_id: UUID,
    organization_id: UUID,
) -> User | None:
    statement = select(User).where(
        User.id == user_id,
        User.organization_id == organization_id,
    )

    return db.scalar(statement)