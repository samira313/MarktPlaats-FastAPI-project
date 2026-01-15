from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.database import get_db
from app import models

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

ADMIN_TOKEN = "admin_full_access_123"


def check_admin(token: str):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Not authorized")


@router.get("/users")
def get_users(
        db: Session = Depends(get_db),
        token: str = Header(None)
):
    check_admin(token)
    return db.query(models.User).all()


@router.post("/users")
def create_user(
        username: str,
        email: str,
        password: str,
        db: Session = Depends(get_db),
        token: str = Header(None)
):
    check_admin(token)

    user = models.User(
        username=username,
        email=email,
        password=password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put("/users/{user_id}")
def update_user(
        user_id: int,
        username: str,
        email: str,
        db: Session = Depends(get_db),
        token: str = Header(None)
):
    check_admin(token)

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = username
    user.email = email
    db.commit()
    return user


@router.delete("/users/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        token: str = Header(None)
):
    check_admin(token)

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted"}


@router.get("/posts")
def get_posts(
        db: Session = Depends(get_db),
        token: str = Header(None)
):
    check_admin(token)
    return db.query(models.Post).all()


@router.delete("/posts/{post_id}")
def delete_post(
        post_id: int,
        db: Session = Depends(get_db),
        token: str = Header(None)
):
    check_admin(token)

    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()


@router.get("/chats")
def get_chats(
        db: Session = Depends(get_db),
        token: str = Header(None)
):
    check_admin(token)
    return db.query(models.Chat).all()
