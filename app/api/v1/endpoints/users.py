from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import desc
from sqlalchemy.orm import Session

from api.v1.models import User, BookTransaction
from api.v1.schemas import UserResponseSchema
from api.v1.schemas.borrow import BorrowResponseSchema
from api.v1.services import get_user_from_token, get_borrow_history
from db import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponseSchema)
def get_user_profile(user_id: int,
                     db: Session = Depends(get_db),
                     current_user: User = Depends(get_user_from_token)):
    """
    Get user credentials. The user can only view their own profile.
    """

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


@router.get("/{user_id}/history",
             response_model=List[BorrowResponseSchema],
             status_code=status.HTTP_200_OK)
def view_users_borrow_history(
        user_id: int,
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        active: bool = Query(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_user_from_token)):

    if current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You can only view your own profile")

    history = get_borrow_history(db=db, user_id=user_id, active=active, limit=limit, offset=offset)

    return history
