from fastapi import APIRouter, HTTPException, status, Response, Depends

from api.v1.models import User
from db import db_dependency
from api.v1.schemas import TokenDataSchema, UserResponseSchema, UserCreateSchema, UserAuthSchema
from api.v1.services import create_user, verify_password, create_auth_token, get_user_by_email, get_user_from_token
from config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix='/auth', tags=['auth'])
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


@router.post('/register',
             response_model=UserResponseSchema,
             status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreateSchema, db: db_dependency):
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
def login(response: Response, user_data: UserAuthSchema, db: db_dependency):
    user = get_user_by_email(db, user_data.email)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials'
        )

    # Create access and refresh tokens
    access_token = create_auth_token(user.id, int(ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_auth_token(user.id, int(REFRESH_TOKEN_EXPIRE_MINUTES))

    # Set 'refresh_token' in cookie with httponly=True
    max_age = REFRESH_TOKEN_EXPIRE_MINUTES * 60 # to seconds
    response.set_cookie(key='refresh_token', value=refresh_token, httponly=True, max_age=max_age)

    # Return 'access_token' in the response
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get("/user/{user_id}", response_model=UserResponseSchema)
def get_user_profile(user_id: int,
                     db: db_dependency,
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