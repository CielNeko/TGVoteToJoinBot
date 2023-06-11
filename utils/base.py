from pydantic import BaseModel
class join_request_details(BaseModel):
    user: int
    chat: int
