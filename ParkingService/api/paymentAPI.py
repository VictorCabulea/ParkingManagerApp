import datetime
from fastapi import APIRouter, Response, HTTPException, status
from database.database import Payment, Account
from dto.paymentDTO import PaymentDTO
from emailGenerator import send_email

router = APIRouter()


@router.post("/api/parking_service/payment")
async def create_payment(payment: PaymentDTO, response: Response):
    new_payment = Payment.create(
        payment_id=payment.payment_id,
        plate_number=payment.plate_number,
        type_of_vehicle=payment.type_of_vehicle,
        account_email=payment.account_email,
        price=payment.price,
        payment_date=datetime.datetime.now()
    )

    if payment.account_email:
        try:
            account = Account.get(email=payment.account_email)
            if account:
                account.payments += ("Payment ID: " + str(payment.payment_id) + " - " + str(payment.plate_number) + ", "
                                     + str(payment.price) + " LEI\n on " + str(payment.payment_date) + "\n")
                account.save()

                email_body = (
                    f"Hello {account.first_name},\n\nYour new payment in value of {payment.price} LEI has been recorded!")
                send_email(account.email, "Payment Successfully Recorded", email_body)
        except Exception as e:
            print(f"No account found: {e}")
            email_body = (f"Hello!\n\nYour new payment in value of {payment.price} LEI has been recorded!")
            send_email(payment.account_email, "Payment Successfully Recorded", email_body)

    response.status_code = status.HTTP_201_CREATED

    return {
        "payment": {
            "payment_id": new_payment.payment_id,
            "plate_number": new_payment.plate_number,
            "type_of_vehicle": new_payment.type_of_vehicle,
            "account_email": new_payment.account_email,
            "price": new_payment.price,
            "payment_date": new_payment.payment_date,
            "links": {
                "self": {
                    "href": f"/api/parking_service/payment/plate_number/{new_payment.plate_number}", "type": "GET"
                },
            }
        },
    }

@router.get("/api/parking_service/payment/plate_number/{plate_number}")
async def get_payment(plate_number: str, response: Response):
    try:
        payments = Payment.filter(plate_number=plate_number)

        if not payments:
            raise Payment.DoesNotExist

        last_payment = payments[len(payments) - 1]

        response.status_code = status.HTTP_200_OK

        return {
            "payment": {
                "payment_id": last_payment.payment_id,
                "plate_number": last_payment.plate_number,
                "type_of_vehicle": last_payment.type_of_vehicle,
                "account_email": "account_email",
                "price": last_payment.price,
                "payment_date": last_payment.payment_date,
                "links": {
                }
            },
        }

    except Payment.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )


@router.get("/api/parking_service/payments")
async def get_all_payments(response: Response):
    try:
        payments = Payment.select()
        if not payments:
            raise Payment.DoesNotExist

        payment_list = []
        for payment in payments:
            payment_list.append({
                "payment_id": payment.payment_id,
                "plate_number": payment.plate_number,
                "type_of_vehicle": payment.type_of_vehicle,
                "account_email": "account_email",
                "price": payment.price,
                "payment_date": payment.payment_date,
                "links": {
                }
            })

        response.status_code = status.HTTP_200_OK

        return {
            "payments": payment_list
        }

    except Payment.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No payments found",
        )
