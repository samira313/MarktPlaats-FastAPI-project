from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.comments import CommentBase, CommentDisplay
from app.db.database import get_db
from app.db import db_comment
from typing import List


router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)

#create comment endpoint
@router.post("/", response_model=CommentDisplay)
def create_comment(request: CommentBase, db: Session = Depends(get_db)):
    return db_comment.create_comment(db, request)

#Read all comments endpoint
@router.get("/", response_model= List[CommentDisplay])
def get_all_comments(db: Session = Depends(get_db)):
    return db_comment.read_all_comments(db)


#Read comment endpoint
@router.get("/{id}", response_model= CommentDisplay)
def get_comment(id: int, db: Session = Depends(get_db)):
    return db_comment.read_comment(db, id)


#Update comment endpoint
@router.put("/{id}/update")
def update_comment(id: int, request: CommentBase, db: Session = Depends(get_db)):
    return db_comment.update_comment(db, id, request)


#Delete comment endpoint
@router.delete("/{id}/delete")
def delete_comment(id: int, db: Session = Depends(get_db)):
    return db_comment.delete_comment(db, id)

# @router.get("/ad/{ad_id}", response_model=List[CommentDisplay])
# def get_comments_by_ad(ad_id: int, db: Session = Depends(get_db)):
#     return db_comment.read_comments_by_ad(db, ad_id)