from fastapi import APIRouter, HTTPException
from data.db import SessionDep
from schemas.users import UserDB, UserPublic
from schemas.book import BookPublic, BookDB
from schemas.book_user_link import BookUserLink
from sqlmodel import select


users_router = APIRouter(prefix="/users")


@users_router.get("/")
def get_all_users(session: SessionDep) -> list[UserPublic]:
    """Returns all users"""
    users = session.exec(select(UserDB)).all()
    return users


@users_router.get("/{id}")
def get_user_by_id(id: int, session: SessionDep) -> UserPublic:
    """Returns the user with the given ID."""
    user = session.get(UserDB, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@users_router.delete("/{id}")
def delete_user(id: int, session: SessionDep):
    """Deletes the user with the given ID."""
    user = session.get(UserDB, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return "User deleted successfully"


@users_router.get("/{id}/books")
def get_user_books(
    id: int,
    session: SessionDep
) -> list[BookPublic]:
    """Returns all books held by the given user."""
    user = session.get(UserDB, id)
    if not user:
        raise HTTPException(404, detail="User not found.")
    statement = select(BookDB).join(BookUserLink).where(
        BookUserLink.user_id == id
    )
    result = session.exec(statement).all()
    return result
