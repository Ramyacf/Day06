
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.modules.cases import service
from app.modules.cases.schemas import CaseCreate, CaseResponse


router = APIRouter(
    prefix="/cases",
    tags=["Cases"],
)


@router.post(
    "",
    response_model=CaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_case(
    case_data: CaseCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.create_case(
        db=db,
        case_data=case_data,
        current_user=current_user,
    )


@router.get(
    "",
    response_model=list[CaseResponse],
)
def list_cases(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    case_status: str | None = Query(default=None, alias="status", max_length=30),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.list_cases(
        db=db,
        current_user=current_user,
        limit=limit,
        offset=offset,
        case_status=case_status,
    )


@router.get(
    "/{case_id}",
    response_model=CaseResponse,
)
def get_case(
    case_id: UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.get_case(
        db=db,
        case_id=case_id,
        current_user=current_user,
    )
