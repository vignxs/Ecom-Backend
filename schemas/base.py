from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

__all__ = ['BaseSchema']
