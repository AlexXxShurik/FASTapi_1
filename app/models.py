from uuid import UUID, uuid4
from typing import Optional
from pydantic import BaseModel, Field

class Task(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    description: Optional[str] = None
    completed: bool = False