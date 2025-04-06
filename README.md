# Library Management System

## How to install:

1) Clone project.
2) Rename .env_example to .env (no changes in the file).
3) Open the terminal in project directory and run following commands.
4) docker compose build
5) docker compose run app sh -c "alembic revision --autogenerate -m "init""
6) docker compose run app sh -c "alembic upgrade head"
7) docker compose up
7) Now you are ready to go!

***

## Features:

How transactions work? 
<p>Each user has attribute 'max_borrows' so user is restricted to have more active borrows than the number of 'max_borrows' (active borrows are transactions with attribute 'returned_at' == None).</p>
<p>Each book has attribute 'qty_in_library' which decreases by one after user borrows a book and increases after user returns it. User can't borrow a book if quantity is less than one.</p>

***

## API Documentation
[View API Docs](https://nero1933.github.io/library-management-system/)

***

## Endpoints

### authors

GET /authors
* Returns a list of all authors.

POST /authors
* Creates an author record.
* Checks that name in unique. 
* Checks for 'birthdate' to be in the past.

GET /authors/{author_id}/books
* Returns a list of all books written by certain author.

##

### auth

POST /auth/register
* Creates a user record.
* Checks that email is unique.
* Checks that username is unique.

POST /auth/login
* Returns 'access_token' and sets 'refresh_token' to cookie with httponly=Ture.

POST /auth/refresh_token
* Retrieves 'refresh_token' from cookie, creates new 'access_token' an returns it.

##

### genres

GET /genres
* Returns a list of all genres.

POST /genres
* Creates a genre record.
* Checks that name in unique. 

##

### publishers

GET /publishers
* Returns a list of all genres.

POST /publishers
* Creates a publisher record.
* Checks that name in unique. 
* Checks for 'established_year' to be in the past.


##

### books

GET /books
* Returns a list of all books with related models.

POST /books
* Creates a book record.
* Cannot be two books with same title and author.
* Checks that ids of author, genre and publisher exists.
* Checks ISBN for correct format.
* Checks 'publish_date' for being in the past.
* Checks that 'qty_in_library' is positive integer.
* Has filters by 'author', 'genre', 'publisher' (by theirs name, not id!), 'title'.
* Has Pagination (limit & offset).

GET /books/{book_id}
* Returns a certain book with related models.

GET /book/{book_id}/history
* Returns a list of transaction for a certain book.
* Has filter 'active'. If 'True' returns only active borrows. If 'False' returns only completed ones.
* Has Pagination (limit & offset).

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
* After user has successfully borrowed a book, quantity of this book decreases by one. 

POST /return (authentication required)
* Takes as a value a list of 'book_ids'.
* Checks each requested 'book.id' for existing.
* Checks that each requested 'book.id' exists in active borrows of current user.
* After user has successfully returned a book, quantity of this book increases by one. 

***

## Database structure

![db structure](db_structure.png)

***

## Testing

To run tests execute command:
<p>docker compose run app sh -c "pytest tests/__init__.py"</p>

***

## Improvements which can be made

* Optimization of SQL queries.
* Storing expired tokens in database and block them.

***
