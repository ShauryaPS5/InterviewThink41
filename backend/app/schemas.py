from pydantic import BaseModel
from typing import Optional
import datetime

# Schema for incoming chat messages
class ChatRequest(BaseModel):
    user_message: str
    user_id: str
    conversation_id: Optional[int] = None

# Schema for individual messages in the history
class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime.datetime

    class Config:
        orm_mode = True # Helps Pydantic work with ORM objects

# Schema for the full conversation response
class ChatResponse(BaseModel):
    ai_response: str
    conversation_id: int
    history: list[Message]