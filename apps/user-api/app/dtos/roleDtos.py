from pydantic import BaseModel


class roleRequestDto(BaseModel):
    name: str


class roleUserRequestDto(BaseModel):
    role_id: int
    user_id: int
