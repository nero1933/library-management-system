import uvicorn

from api.v1.endpoints import books

from app import app

app.include_router(books.router, prefix="/authors", tags=["authors"])


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
