from pydantic import BaseModel


class hotelRequestDto(BaseModel):
    name: str
    address: str
    phone_number: str
