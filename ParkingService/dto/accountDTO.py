from pydantic import BaseModel


class AccountDTO(BaseModel):
    email: str
    password: str
    last_name: str
    first_name: str
    active_reservation: bool
    payments: str


