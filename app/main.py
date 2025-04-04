import uvicorn

from api.v1.endpoints import books, auth

from app import app

app.include_router(books.router)
app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
