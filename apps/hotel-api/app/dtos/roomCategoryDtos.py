from pydantic import BaseModel


class roomCategoryRequestDto(BaseModel):
    name: str
    max_occupancy: int
