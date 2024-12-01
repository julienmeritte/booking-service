from pydantic import BaseModel
from datetime import datetime


class discountRequestDto(BaseModel):
    discount_type_id: int
    start_date: datetime
    end_date: datetime
