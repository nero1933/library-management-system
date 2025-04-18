from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from api.v1 import models
from api.v1 import schemas
from db import get_db

router = APIRouter(prefix='/publishers', tags=['publishers'])


@router.post('',
             response_model=schemas.PublisherResponseSchema,
             status_code=status.HTTP_201_CREATED)
async def create_publisher(publisher: schemas.PublisherSchema, db: Session = Depends(get_db)):
    existing_publisher = db.query(models.Publisher).filter(
        models.Publisher.name == publisher.name).first()

    if existing_publisher:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Publisher with this name already exists"
        )

    db_publisher = models.Publisher(
        name=publisher.name,
        established_year=publisher.established_year
    )
    db.add(db_publisher)
    db.commit()
    db.refresh(db_publisher)
    return db_publisher


@router.get('', response_model=list[schemas.PublisherResponseSchema])
def get_publisher(db: Session = Depends(get_db)):
    publisher = db.query(models.Publisher).all()
    return publisher
