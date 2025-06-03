from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class Category(BaseModel):
    id: Optional[str] = None
    name: str


class QAItem(BaseModel):
    id: Optional[str] = None
    category_id: str
    question: str
    answer: str
