from pydantic import BaseModel, ConfigDict
from datetime import date

class CommentBase(BaseModel):
    comment_id: int
    comment: str
    create_by_id: int # current_user = Depends(get_current_user)
    sent_to_id: int
    date: date


class CommentDisplay(BaseModel):
    comment_id: int
    comment: str
    create_by_id: int
    sent_to_id: int
    date: date
    #advertisements: list = []

    model_config = ConfigDict(from_attributes=True)