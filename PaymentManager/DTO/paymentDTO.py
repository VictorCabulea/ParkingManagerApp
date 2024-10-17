from pydantic import BaseModel


class PaymentDTO(BaseModel):
    payment_id: int
    plate_number: str
    type_of_vehicle: int
    account_email: str
    price: float
    payment_date: str
