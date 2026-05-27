from fastapi import APIRouter, Path, HTTPException, Query
from schemas.book import BookCreate, BookPublic, BookDB
from schemas.users import UserPublic, UserDB
from schemas.book_user_link import BookUserLink
from typing import Annotated
from schemas.review import Review
from data.db import SessionDep
from sqlmodel import select, delete


books_router = APIRouter(prefix="/books", tags=["books"])


@books_router.get("/")
def get_all_books(
    session: SessionDep,
    sort: Annotated[bool, Query(description="Sort books by their review")] = False,
) -> list[BookPublic]:
    """Returns the list ok available books."""
    books = session.exec(select(BookDB)).all()
    if sort:
        return sorted(books, key=lambda book: book.review)
    else:
        return list(books)


@books_router.get("/{id}")
def get_book_by_id(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the book to retrieve")]
) -> BookPublic:
    """Returns the book with the given id."""
    book = session.get(BookDB, id)
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")


@books_router.post("/{id}/review")
def add_review(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the book to retrieve")],
    review: Review
):
    """Add a review to the book with the given ID"""
    book = session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.review = review.review
    session.add(book)
    session.commit()
    return "Review added successfully"


@books_router.post("/")
def add_book(session: SessionDep, book: BookCreate):
    """Adds a new book."""
    book_entry = BookDB.model_validate(book)
    session.add(book_entry)
    session.commit()
    return "Book added successfully"


@books_router.put("/{id}")
def replace_book(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the book to replace")],
    new_book: BookCreate
):
    """Replaces the book with the given ID."""
    book = session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.title = new_book.title
    book.author = new_book.author
    book.review = new_book.review
    session.add(book)
    session.commit()
    return "Book replaced successfully"


@books_router.delete("/")
def delete_all_books(session: SessionDep):
    """Deletes all the stored books."""
    session.exec(delete(BookDB))
    session.commit()
    return "All books deleted successfully"


@books_router.delete("/{id}")
def delete_book(
    session: SessionDep,
    id: Annotated[int, Path(description="The ID of the book to delete")]
):
    """Deletes the book with the given ID."""
    book = session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return "Book deleted successfully"


@books_router.get("/{id}/users")
def get_book_users(id: int, session: SessionDep) -> list[UserPublic]:
    """Returns all users associated with the given book."""
    book = session.get(BookDB, id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    statement = select(UserDB).join(BookUserLink).where(BookUserLink.book_id == id)
    return list(session.exec(statement).all())

