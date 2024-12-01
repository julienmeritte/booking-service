from pydantic import BaseModel
from datetime import datetime


class reservationServiceRequestDto(BaseModel):
    reservation_id: int
    additional_service_id: int
