
import secrets
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.modules.cases import repository
from app.modules.cases.schemas import CaseCreate


def create_case(
    db: Session,
    case_data: CaseCreate,
    current_user,
):
    reference_code = f"BVG-{secrets.token_hex(6).upper()}"

    try:
        return repository.create_case(
            db=db,
            organization_id=current_user.organization_id,
            created_by=current_user.id,
            reference_code=reference_code,
            title=case_data.title,
            description=case_data.description,
        )
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Could not create the case because of a database conflict",
        )


def get_case(
    db: Session,
    case_id: UUID,
    current_user,
):
    case = repository.get_case_by_id(
        db=db,
        case_id=case_id,
        organization_id=current_user.organization_id,
    )

    if case is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Case not found",
        )

    return case


def list_cases(
    db: Session,
    current_user,
    limit: int = 20,
    offset: int = 0,
    case_status: str | None = None,
):
    return repository.list_cases(
        db=db,
        organization_id=current_user.organization_id,
        limit=limit,
        offset=offset,
        case_status=case_status,
    )
