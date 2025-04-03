from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.v1 import models
from api.v1 import schemas

from app import app
from db import get_db

router = APIRouter()


@app.post("/authors", response_model=schemas.AuthorBase, status_code=201)
async def create_author(author: schemas.AuthorBase, db: Session = Depends(get_db)):
    db_author = models.Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


@app.get("/authors", response_model=list[schemas.AuthorBase])
def get_authors(db: Session = Depends(get_db)):
    authors = db.query(models.Author).all()
    return authors


# @app.post("/books", response_model=Book, status_code=201)
# async def create_book(book: BookBase, db: db_dependency):
