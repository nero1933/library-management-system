from fastapi import APIRouter, status, HTTPException
from api.v1 import models
from api.v1 import schemas
from db import db_dependency

router = APIRouter(prefix='/authors', tags=['authors'])


@router.post('', response_model=schemas.AuthorResponseSchema, status_code=status.HTTP_201_CREATED)
def create_author(author: schemas.AuthorSchema, db: db_dependency):
    existing_author = db.query(models.Author).filter(models.Author.name == author.name).first()
    if existing_author:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Author with this name already exists"
        )

    db_author = models.Author(name=author.name, birthdate=author.birthdate)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@router.get('', response_model=list[schemas.AuthorResponseSchema])
def get_authors(db: db_dependency):
    authors = db.query(models.Author).all()
    return authors


# @app.post("/books", response_model=Book, status_code=201)
# async def create_book(book: BookBase, db: db_dependency):
