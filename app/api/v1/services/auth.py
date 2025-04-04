import jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from api.v1.models import User
from config import SECRET_KEY, ALGORITHM, MAX_BORROWS


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session,
                username: str,
                email: str,
                full_name: str,
                password: str) -> User:
    hashed_password = pwd_context.hash(password)
    user = User(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        max_borrows=int(MAX_BORROWS)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_auth_token(user_id: int, token_lifetime: int):
    print(datetime.utcnow() + timedelta(minutes=token_lifetime))
    expire = datetime.utcnow() + timedelta(minutes=token_lifetime)
    to_encode = {'sub': user_id, 'exp': expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the token and verify it
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")  # "sub" is typically used for the user ID in JWT
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is invalid")

        # Get the user from the database
        user = get_user_by_id(user_id)  # Assuming you have a function to retrieve a user by ID
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")


# Dummy function to simulate user retrieval
def get_user_by_id(user_id: str):
    # Implement this to query the database for the user by ID
    return User(id=user_id, username="test_user", email="test@example.com")