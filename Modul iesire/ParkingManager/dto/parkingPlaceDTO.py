from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ParkingPlaceDTO(BaseModel):
    parking_place_id: str
    type_of_vehicle: int
    occupied: bool
    occupied_by: Optional[str]
    entry_time: Optional[datetime]
