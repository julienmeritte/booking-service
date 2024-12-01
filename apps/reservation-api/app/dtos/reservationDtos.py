from pydantic import BaseModel
from datetime import datetime


class reservationRequestDto(BaseModel):
    hotel_id: int
    room_id: int
    user_id: int
    number_occupants: int
    start_date: datetime
    end_date: datetime
