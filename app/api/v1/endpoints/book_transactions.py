from datetime import datetime

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from api.v1.models import User, BookTransaction, Book
from api.v1.schemas import BorrowResponseSchema, BorrowMultipleCreateSchema
from api.v1.services import get_user_from_token
from db import get_db

router = APIRouter(prefix='', tags=['book_transactions'])

@router.post("/borrow",
             response_model=list[BorrowResponseSchema],
             status_code=status.HTTP_201_CREATED)
def borrow_book(data: BorrowMultipleCreateSchema,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_user_from_token)):

    try:
        books = db.query(Book) \
            .filter(Book.id.in_(data.book_ids)) \
            .all()

        found_ids = {book.id for book in books}
        requested_ids = set(data.book_ids)
        missing_ids = requested_ids - found_ids

        # If requested ids of books are not in db -- raise error
        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book ids not found: {list(missing_ids)}"
            )

        # If any of requested books qty is < 1 -- raise error
        unavailable_books = [book.id for book in books if book.qty_in_library < 1]
        if unavailable_books:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No books left for the following ids: {unavailable_books}"
            )

        active_borrows = db.query(BookTransaction.book_id).filter(
            BookTransaction.user_id == current_user.id,
            BookTransaction.returned_at == None,
        ).all()

        active_borrowed_ids = {book_id for (book_id,) in active_borrows}

        # if user tries to borrow books over his limit raise error
        if (current_user.max_borrows - len(requested_ids) - len(active_borrowed_ids)) < 0:
            available_amount = current_user.max_borrows - len(active_borrowed_ids)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Exceeded limit of borrowing books. "
                       f"You can borrow only {available_amount} books for now."
            )

        # If user is trying to borrow books that he
        # already borrower and didn't return raise error
        already_borrowed = requested_ids & active_borrowed_ids
        if already_borrowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User already borrowed books: ids: {list(already_borrowed)}."
            )

        # Decrease qty of just borrowed books by one
        for book in books:
            book.qty_in_library -= 1

        # Create the transactions
        transactions = [
            BookTransaction(
                user_id=current_user.id,
                book_id=book.id,
                borrowed_at=datetime.utcnow(),
            )
            for book in books
        ]

        db.add_all(transactions)
        db.commit()

        return transactions  # Queries are nor optimized / Can be done by 2 queries / n+1

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the request. Error: {e}"
        )


@router.post("/return",
             response_model=list[BorrowResponseSchema],
             status_code=status.HTTP_201_CREATED)
def borrow_book(data: BorrowMultipleCreateSchema,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_user_from_token)):

    try:
        books = db.query(Book) \
            .filter(Book.id.in_(data.book_ids)) \
            .all()

        found_ids = {book.id for book in books}
        requested_ids = set(data.book_ids)
        missing_ids = requested_ids - found_ids

        # If requested ids of books are not in db -- raise error
        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book ids not found: {list(missing_ids)}"
            )

        active_borrows = db.query(BookTransaction) \
            .filter(
                # Same user who borrowed this book
                BookTransaction.user_id == current_user.id,
                # book ids from request
                BookTransaction.book_id.in_(requested_ids),
                # If borrow is still active (returned_at is None)
                BookTransaction.returned_at.is_(None)) \
            .all()

        # If user request to return book which he didn't borrow raise error
        active_borrows_ids = {active_borrow.book_id for active_borrow in active_borrows}
        not_borrowed = requested_ids - active_borrows_ids
        if not_borrowed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No books borrowed with following ids: {list(not_borrowed)}."
            )

        # After returning book update returned_at in transaction
        for transaction in active_borrows:
            transaction.returned_at = datetime.utcnow()

        # After returning book update qty in book
        for book in books:
            book.qty_in_library += 1

        db.commit()

        return active_borrows # Queries are nor optimized / Can be done by 2 queries / n+1


    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing the request. Error: {e}"
        )
