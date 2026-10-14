
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.case import Case


def get_case_by_id(
    db: Session,
    case_id: uuid.UUID,
    organization_id: uuid.UUID,
) -> Case | None:
    statement = select(Case).where(
        Case.id == case_id,
        Case.organization_id == organization_id,
    )

    return db.scalar(statement)


def create_case(
    db: Session,
    organization_id: uuid.UUID,
    created_by: uuid.UUID,
    reference_code: str,
    title: str | None,
    description: str | None,
) -> Case:
    case = Case(
        organization_id=organization_id,
        created_by=created_by,
        reference_code=reference_code,
        title=title,
        description=description,
        status="CREATED",
    )

    db.add(case)
    db.commit()
    db.refresh(case)

    return case


def list_cases(
    db: Session,
    organization_id: uuid.UUID,
    limit: int = 20,
    offset: int = 0,
    case_status: str | None = None,
) -> list[Case]:
    statement = select(Case).where(
        Case.organization_id == organization_id,
    )

    if case_status is not None:
        statement = statement.where(
            Case.status == case_status,
        )

    statement = (
        statement
        .order_by(Case.created_at.desc())
        .limit(limit)
        .offset(offset)
    )

    return list(db.scalars(statement).all())
