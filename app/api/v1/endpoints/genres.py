from fastapi import APIRouter, status, HTTPException
from api.v1 import models
from api.v1 import schemas
from db import db_dependency

router = APIRouter(prefix='/genres', tags=['genres'])


@router.post('', response_model=schemas.GenreResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_genre(genre: schemas.GenreSchema, db: db_dependency):
    existing_genre = db.query(models.Genre).filter(models.Genre.name == genre.name).first()
    if existing_genre:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Genre with this name already exists"
        )

    db_genre = models.Genre(name=genre.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


@router.get('', response_model=list[schemas.GenreResponseSchema])
def get_genre(db: db_dependency):
    genre = db.query(models.Genre).all()
    return genre
