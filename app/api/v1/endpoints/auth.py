from fastapi import APIRouter, HTTPException, status, Response, Depends
from sqlalchemy.orm import Session

from db import get_db
from api.v1.schemas import TokenDataSchema, UserResponseSchema, UserCreateSchema, UserAuthSchema
from api.v1.services import create_user, verify_password, create_auth_token, get_user_by_email
from core.config import settings

router = APIRouter(prefix='/auth', tags=['auth'])
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


@router.post('/register',
             response_model=UserResponseSchema,
             status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_data.email)

    if existing_user:
        if existing_user.email == user_data.email:
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        if existing_user.username == user_data.username:
            raise HTTPException(
                status_code=400,
                detail="Username already taken"
            )

    return create_user(
        db,
        user_data.username,
        user_data.email,
        user_data.full_name,
        user_data.password,
    )


@router.post('/login', response_model=TokenDataSchema)
def login(response: Response, user_data: UserAuthSchema, db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials'
        )

    # Create access and refresh tokens
    access_token = create_auth_token(user.id, int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_auth_token(user.id, int(settings.REFRESH_TOKEN_EXPIRE_MINUTES))

    # Set 'refresh_token' in cookie with httponly=True
    max_age = settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60 # to seconds
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, max_age=max_age)

    # Return 'access_token' in the response
    return {'access_token': access_token, 'token_type': 'bearer'}
