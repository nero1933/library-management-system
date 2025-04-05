# Library Management System

***

## How to install:
1) Clone project
2) Rename .env_example to .env (no changes in the file)
3) Open the terminal in project directory and run following commands
4) docker compose build
5) docker compose run app sh -c "alembic revision --autogenerate -m "init""
6) docker compose run app sh -c "alembic upgrade head" 
7) Now you are ready to go!

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

***

### auth
POST /auth/register
*

POST /auth/login
*

POST /auth/refresh_token
*

***

### genres
GET /genres
*

POST /genres
*

***

### publishers
GET /publishers
*

POST /publishers
*

***

### books
GET /books
* Returns list of books with related models.

POST /books
* Cannot be two books with same title and same authors.
* Checks that ids of author, genre and publisher exists.
* Checks ISBN for correct format.
* Checks publish date for being in the past.

GET /books/{book_id}
* Returns a certain book with related models.

GET /book/{book_id}/history
* Returns a transaction history for certain book

***

### users
GET /users/me
*

POST /users/history
*

***

### book_transactions
GET /borrow
*

POST /return
*

***

## Database structure
![db structure](db_structure.png)
