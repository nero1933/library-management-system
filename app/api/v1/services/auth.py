import jwt
from sqlalchemy import or_
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from datetime import datetime, timedelta
from api.v1.models import User
from config import SECRET_KEY, ALGORITHM, MAX_BORROWS

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def find_user(db: Session, email: str, username: str) -> User | None:
    existing_user = db.query(User).filter(
        or_(
            User.email == email,
            User.username == username
        )
    ).first()

    return existing_user


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

def create_auth_token(email: str, token_lifetime: int):
    expire = datetime.utcnow() + timedelta(days=token_lifetime)
    to_encode = {'sub': email, 'exp': expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
