from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import get_current_user
from app.modules.users import service
from app.modules.users.schemas import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user(
    user_id: UUID,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return service.get_user(
        db=db,
        user_id=user_id,
        current_user=current_user,
    )