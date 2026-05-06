from fastapi import FastAPI
from routers.books import books_router
from contextlib import asynccontextmanager
from data.db import init_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # on create
    init_database()
    yield
    # on close


app = FastAPI(lifespan=lifespan)
app.include_router(books_router)
