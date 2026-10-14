from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.organization import Organization


def get_organization(
    db: Session,
    organization_id: UUID,
) -> Organization | None:
    statement = select(Organization).where(
        Organization.id == organization_id,
    )

    return db.scalar(statement)