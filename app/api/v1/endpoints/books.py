from fastapi import APIRouter, status
from api.v1 import models
from api.v1 import schemas
from app import app
from db import db_dependency

router = APIRouter()


@app.post("/authors", response_model=schemas.AuthorBase, status_code=status.HTTP_201_CREATED)
async def create_author(author: schemas.AuthorBase, db: db_dependency):
    db_author = models.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@app.get("/authors", response_model=list[schemas.AuthorBase])
def get_authors(db: db_dependency):
    authors = db.query(models.Author).all()
    return authors


# @app.post("/books", response_model=Book, status_code=201)
# async def create_book(book: BookBase, db: db_dependency):
