from pydantic import BaseModel


class serviceRequestDto(BaseModel):
    name: str
    max_number: int
