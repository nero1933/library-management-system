import uvicorn
from fastapi import FastAPI

from api.v1.endpoints import authors, auth, genres, publishers, books, users, book_transactions

app = FastAPI()

app.include_router(authors.router)
app.include_router(auth.router)
app.include_router(genres.router)
app.include_router(publishers.router)
app.include_router(books.router)
app.include_router(users.router)
app.include_router(book_transactions.router)


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
