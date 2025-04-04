from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.v1.models import User
from api.v1.schemas import UserResponseSchema
from api.v1.services import get_user_from_token
from db import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponseSchema)
def get_user_profile(user_id: int,
                     db: Session = Depends(get_db),
                     current_user: User = Depends(get_user_from_token)):
    """
    Get user credentials. The user can only view their own profile.
    """
    # print('current_user --->', current_user.id)
    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can only view your own profile")

    return UserResponseSchema(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        created_at=current_user.created_at
    )
