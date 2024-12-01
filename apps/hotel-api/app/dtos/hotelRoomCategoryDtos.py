from pydantic import BaseModel


class hotelRoomRequestDto(BaseModel):
    hotel_id: int
    room_number: str
    category_id: int
