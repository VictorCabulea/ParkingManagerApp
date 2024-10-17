import random
import string

from fastapi import APIRouter, Response, HTTPException, status
from database.database import Account
from dto.accountDTO import AccountDTO
from passlib.context import CryptContext
from emailGenerator import send_email

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for i in range(length))


@router.post("/api/parking_service/account")
async def create_account(account: AccountDTO, response: Response):
    existing_account_email = Account.get_or_none(email=account.email)
    if existing_account_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="An account with this email already exists")

    new_account = Account.create(
        email=account.email,
        password=account.password,
        last_name=account.last_name,
        first_name=account.first_name,
        active_reservation=account.active_reservation,
        payments=account.payments
    )

    email_body = (f"Hello {account.first_name},\n\nYour new account has been successfully created!")
    send_email(account.email, "Account Created Successfully", email_body)

    response.status_code = status.HTTP_201_CREATED

    return {
        "account": {
            "email": new_account.email,
            "password": new_account.password,
            "last_name": new_account.last_name,
            "first_name": new_account.first_name,
            "active_reservation": new_account.active_reservation,
            "payments": new_account.payments,
            "links": {
                "reset_password": {
                    "href": f"/api/parking_service/account/email/{new_account.email}/reset_password", "type": "POST"
                },
                "update_account": {
                    "href": f"/api/parking_service/account/email/{new_account.email}", "type": "PATCH"
                },
                "update_active_reservation": {
                    "href": f"/api/parking_service/account/email/{account.email}/active_reservation", "type": "PATCH"
                },
                "delete_account": {
                    "href": f"/api/parking_service/account/email/{new_account.email}", "type": "DELETE"
                }
            }
        }
    }


@router.get("/api/parking_service/account/email/{email}")
async def get_account(email: str, response: Response):
    try:
        account = Account.get(email=email)
        if account:
            response.status_code = status.HTTP_200_OK
            return {
                "account": {
                    "email": account.email,
                    "password": account.password,
                    "last_name": account.last_name,
                    "first_name": account.first_name,
                    "active_reservation": account.active_reservation,
                    "payments": account.payments,
                    "links": {
                        "reset_password": {
                            "href": f"/api/parking_service/account/email/{account.email}/reset_password", "type": "POST"
                        },
                        "update_account": {
                            "href": f"/api/parking_service/account/email/{account.email}", "type": "PATCH"
                        },
                        "update_active_reservation": {
                            "href": f"/api/parking_service/account/email/{account.email}/active_reservation", "type": "PATCH"
                        },
                        "delete_account": {
                            "href": f"/api/parking_service/account/email/{account.email}", "type": "DELETE"
                        }
                    }
                }
            }
    except Account.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )


@router.patch("/api/parking_service/account/email/{email}")
async def update_account(email: str, updated_account: AccountDTO, response: Response):
    try:
        account = Account.get(email=email)

        if updated_account.first_name != "":
            account.first_name = updated_account.first_name
        if updated_account.last_name != "":
            account.last_name = updated_account.last_name
        if updated_account.password != "":
            account.password = updated_account.password

        account.save()

        response.status_code = status.HTTP_204_NO_CONTENT

        return None

    except Account.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )


@router.patch("/api/parking_service/account/email/{email}/active_reservation")
async def update_account_active_reservation(email: str, response: Response):
    try:
        account = Account.get(email=email)

        if account.active_reservation == False:
            account.active_reservation = True
        else:
            account.active_reservation = False

        account.save()

        response.status_code = status.HTTP_204_NO_CONTENT

        return None

    except Account.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )


@router.post("/api/parking_service/account/email/{email}/reset_password")
async def reset_password(email: str, response: Response):
    try:
        account = Account.get(email=email)
        new_password = generate_random_password()
        hashed_password = pwd_context.hash(new_password)

        account.password = hashed_password
        account.save()

        email_body = (f"Hello {account.first_name},\n\nYour new password is: {new_password}\n\nPlease change your "
                      f"password after logging in.")
        send_email(email, "Reset Password", email_body)

        response.status_code = status.HTTP_200_OK
        return {
            "message": "A new password has been sent to your email address",
            "links": {
                "self": {
                    "href": f"/api/parking_service/account/email/{account.email}", "type": "GET"
                },
                "reset_password": {
                    "href": f"/api/parking_service/account/email/{account.email}/reset_password", "type": "POST"
                },
                "update_account": {
                    "href": f"/api/parking_service/account/email/{account.email}", "type": "PATCH"
                },
            }
        }

    except Account.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )


@router.delete("/api/parking_service/account/email/{email}")
async def delete_account(email: str, response: Response):
    try:
        account = Account.get(email=email)
        account.delete_instance()

        response.status_code = status.HTTP_204_NO_CONTENT

        return None

    except Account.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )
