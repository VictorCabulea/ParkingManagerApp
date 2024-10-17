import re
from datetime import datetime


def validate_cvc(cvc: str) -> bool:
    if len(cvc) != 3 or not re.match(r"^\d+$", cvc):
        print(f"CVC {cvc}")
        return False
    return True


def validate_expiry_date(expiry_date: str) -> bool:
    if len(expiry_date) != 5 or expiry_date[2] != '/':
        return False
    try:
        expiry_month = int(expiry_date[:2])
        expiry_year = int(expiry_date[3:])
        correct_expiry_year = int(f"20{expiry_year}")
        current_month = datetime.now().month
        current_year = datetime.now().year
        if correct_expiry_year < current_year or (correct_expiry_year == current_year and expiry_month < current_month):
            return False
    except ValueError:
        print("Invalid date format")
        return False
    return True


def validate_card_number(card_number: str) -> bool:
    pattern = re.compile(r"^\d{4}\s\d{4}\s\d{4}\s\d{4}$")
    if not pattern.match(card_number):
        print("Invalid card number format")
        return False
    return True
