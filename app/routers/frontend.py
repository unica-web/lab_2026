"""
Frontend router: serves HTML pages using Jinja2 templates.
Each page is a shell; JavaScript in the template handles data fetching (AJAX)
and DOM manipulation.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "..", "templates")
)

frontend_router = APIRouter(tags=["frontend"])


@frontend_router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@frontend_router.get("/ui/users", response_class=HTMLResponse)
async def users_list(request: Request):
    return templates.TemplateResponse("users_list.html", {"request": request})


@frontend_router.get("/ui/users/{user_id}", response_class=HTMLResponse)
async def user_detail(request: Request, user_id: int):
    return templates.TemplateResponse(
        "user_detail.html", {"request": request, "user_id": user_id}
    )


@frontend_router.get("/ui/books", response_class=HTMLResponse)
async def books_list(request: Request):
    return templates.TemplateResponse("books_list.html", {"request": request})


@frontend_router.get("/ui/books/add", response_class=HTMLResponse)
async def add_book(request: Request):
    return templates.TemplateResponse("add_book.html", {"request": request})


@frontend_router.get("/ui/books/{book_id}", response_class=HTMLResponse)
async def book_detail(request: Request, book_id: int):
    return templates.TemplateResponse(
        "book_detail.html", {"request": request, "book_id": book_id}
    )

