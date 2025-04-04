from sqlalchemy.orm import Session
from sqlalchemy import desc
from api.v1.models import BookTransaction

def get_borrow_history(
        db: Session,
        book_id: int = None,
        user_id: int = None,
        active: bool = None,
        limit: int = 10,
        offset: int = 0
):

    query = db.query(BookTransaction)

    if book_id:
        query = query.filter(BookTransaction.book_id == book_id)
    if user_id:
        query = query.filter(BookTransaction.user_id == user_id)

    if active:
        query = query.filter(BookTransaction.returned_at == None)
    elif active is False:
        query = query.filter(BookTransaction.returned_at != None)

    # Sort: new first
    query = query.order_by(desc(BookTransaction.id))

    # Add pagination
    history = query.offset(offset).limit(limit).all()

    return history
