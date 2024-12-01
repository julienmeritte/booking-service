from pydantic import BaseModel
from datetime import datetime


class discountTypeRequestDto(BaseModel):
    name: str
