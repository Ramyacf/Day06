from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.modules.organizations import service
from app.modules.organizations.schemas import OrganizationResponse


router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)


@router.get(
    "/{organization_id}",
    response_model=OrganizationResponse,
)
def get_organization(
    organization_id: UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.get_organization(
        db=db,
        organization_id=organization_id,
        current_user=current_user,
    )