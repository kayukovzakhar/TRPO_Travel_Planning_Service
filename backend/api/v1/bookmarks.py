from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.session      import get_db
from core.security   import get_current_user
from models.user     import User
from models.bookmark import Bookmark
from schemas.bookmark import BookmarkCreate, BookmarkResponse

router = APIRouter(
    prefix="/api/v1/bookmarks",
    tags=["bookmarks"],
)

# GET /api/v1/bookmarks/
@router.get("/", response_model=List[BookmarkResponse])
def read_bookmarks(
    current_user: User = Depends(get_current_user),
    db: Session      = Depends(get_db),
):
    return db.query(Bookmark).filter(Bookmark.user_id == current_user.id).all()

# POST /api/v1/bookmarks/
@router.post("/", response_model=BookmarkResponse, status_code=status.HTTP_201_CREATED)
def create_bookmark(
    bm_in: BookmarkCreate,
    current_user: User = Depends(get_current_user),
    db: Session      = Depends(get_db),
):
    # проверяем дубли
    exists = (
        db.query(Bookmark)
        .filter(Bookmark.user_id == current_user.id)
        .filter(Bookmark.route_slug == bm_in.route_slug)
        .first()
    )
    if exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Уже в закладках"
        )
    new = Bookmark(
        user_id    = current_user.id,
        route_slug = bm_in.route_slug
    )
    db.add(new); db.commit(); db.refresh(new)
    return new

# DELETE /api/v1/bookmarks/{bookmark_id}/
@router.delete("/{bookmark_id}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_bookmark(
    bookmark_id: int,
    current_user: User = Depends(get_current_user),
    db: Session      = Depends(get_db),
):
    bm = (
        db.query(Bookmark)
          .filter(Bookmark.id == bookmark_id)
          .filter(Bookmark.user_id == current_user.id)
          .first()
    )
    if not bm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не найдена закладка")
    db.delete(bm); db.commit()
