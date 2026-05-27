from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers.books import books_router
from routers.users import users_router
from routers.frontend import frontend_router
from contextlib import asynccontextmanager
from data.db import init_database
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # on create
    init_database()
    yield
    # on close


app = FastAPI(lifespan=lifespan)

# Serve static files (CSS, JS, images)
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# API routers (existing, unmodified)
app.include_router(books_router)
app.include_router(users_router)

# New routers
app.include_router(frontend_router)

