from datetime import datetime
from pydantic import BaseModel


class ParkedCarDTO(BaseModel):
    plate_number: str
    type_of_vehicle: int
    entry_time: datetime
    price_per_hour: int
