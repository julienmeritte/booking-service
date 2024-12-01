from pydantic import BaseModel


class userRequestDto(BaseModel):
    mail: str
    password: str