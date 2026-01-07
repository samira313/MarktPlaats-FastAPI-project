from sqlalchemy.orm.session import Session
from app.models.comments import DbComment
from app.schemas.comments import CommentBase


def create_comment(db: Session, request: CommentBase):
    new_comment = DbComment(
        comment=request.comment,
        create_by_id=request.create_by_id,
        sent_to_id=request.sent_to_id,
        date=request.date
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def read_all_comments(db:Session):
    return db.query(DbComment).all()

def read_comment(db:Session, id: int):
    return db.query(DbComment).filter(DbComment.comment_id == id).first()


def update_comment(db: Session, id: int, request: CommentBase):
    comment = db.query(DbComment).filter(DbComment.comment_id == id)
    comment.update({
        DbComment.comment_id: request.comment_id,
        DbComment.comment: request.comment,
        DbComment.create_by_id: request.create_by_id,
        DbComment.sent_to_id: request.sent_to_id,
        DbComment.date: request.date
    })
    db.commit()
    #db.refresh(comment)
    return comment


def delete_comment(db: Session, id: int):
    comment = db.query(DbComment).filter(DbComment.comment_id == id).first()
    db.delete(comment)
    db.commit()
    return {"detail": "Comment deleted successfully"}



# def read_comments_by_ad(db: Session, ad_id: int):
#     return db.query(DbComment).filter(DbComment.ad_id == ad_id).all()
