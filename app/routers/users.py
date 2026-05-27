from fastapi import APIRouter
from data.db import SessionDep
from schemas.users import UserDB, UserPublic
from schemas.book import BookPublic, BookDB
from sqlmodel import select


users_router = APIRouter(prefix="/users")


@users_router.get("/")
def get_all_users(session: SessionDep) -> list[UserPublic]:
    """Returns all users"""
    users = session.exec(select(UserDB)).all()
    return users


@users_router.get("/{id}/books")
def get_user_books(
    id: int,
    session: SessionDep
) -> list[BookPublic]:
    """Returns all books held by the given user."""
    statement = select(BookDB).join(UserDB).where(UserDB.id == id)
    result = session.exec(statement).all()
    return result
