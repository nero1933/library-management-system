# Library Management System

## How to install:
1) Clone project
2) Rename .env_example to .env (no changes in the file)
3) Open the terminal in project directory and run following commands
4) docker compose build
5) docker compose run app sh -c "alembic revision --autogenerate -m "init""
6) docker compose run app sh -c "alembic upgrade head" 
7) Now you are ready to go!

***

## Features:
In progress...

***

## API Documentation
[View API Docs](https://nero1933.github.io/library-management-system/)

***

## Endpoints
### authors
GET /authors
*

POST /authors
*

GET /authors/{author_id}/books
*

##

### auth
POST /auth/register
* Creates a user.
* Checks that email is unique.
* Checks that username is unique.

POST /auth/login
*

POST /auth/refresh_token
*

##

### genres
GET /genres
*

POST /genres
*

##

### publishers
GET /publishers
*

POST /publishers
*

##

### books
GET /books
* Returns a list of books with related models.

POST /books
* Creates a book record.
* Cannot be two books with same title and author.
* Checks that ids of author, genre and publisher exists.
* Checks ISBN for correct format.
* Checks publish date for being in the past.
* Has filters by 'author', 'genre', 'publisher' (by theirs name, not id!), 'title'.
* Has Pagination (limit & offset).

GET /books/{book_id}
* Returns a certain book with related models.

GET /book/{book_id}/history
* Returns a list of transactions for a certain book.

##

### users
GET /users/me (authentication required)
* Returns user details.

GET /users/history (authentication required)
* Returns list of users transaction.
* Has filter 'active'. If 'True' returns only active borrows. If 'False' returns only completed ones.
* Has Pagination (limit & offset).

##

### book_transactions
GET /borrow (authentication required)
* Takes as a value a list od 'book_ids'.
* Checks each requested 'book.id' for existing.
* Checks each requested 'book.qty_in_library' to be more than one.
* Checks that the user does not exceed their borrowing limit (By default user can have no more than 3 active borrows. See 'MAX_BORROWS' in .env).
* Checks that the user cannot borrow same book twice if he didn't return first one.
* After user has successfully borrowed a book, qty of this book decreases by one. 

POST /return (authentication required)
* Takes as a value a list od 'book_ids'.
* Checks each requested 'book.id' for existing.
* Checks that each requested 'book.id' exists in active borrows.
* After user has successfully returned a book, qty of this book increases by one. 

***

## Database structure
![db structure](db_structure.png)
