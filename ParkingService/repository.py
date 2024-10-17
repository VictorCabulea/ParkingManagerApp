from datetime import datetime
from database.database import ParkingPlace, ParkedCar, Payment
import datetime
import random
import string


def read_valid_regions():
    with open("resources/valid_romanian_regions.txt", "r") as file:
        VALID_ROMANIAN_REGIONS = [line.strip() for line in file]

    return VALID_ROMANIAN_REGIONS


def create_pairs_type_of_vehicle_and_parking_place_id():
    values = [1] * 20 + [2] * 30 + [3] * 20 + [4] * 10
    pairs = []

    for vehicle_type in range(1, 5):
        count = 0
        for value in values:
            if value == vehicle_type:
                pairs.append((vehicle_type, count))
                count += 1

    return pairs


def get_price_per_hour(type_of_vehicle):
    prices = {
        1: 5,
        2: 3,
        3: 2,
    }
    return prices.get(type_of_vehicle, 1)


def get_correct_column_for_parking_place(index):
    section = chr(65 + index // 10)
    position = index % 10 + 1
    return f"{section}{position}"


def create_data_to_populate_parkingPlaces_and_parkedCar_tables():
    types_of_vehicle = [1] * 20 + [2] * 30 + [3] * 20 + [4] * 10

    occupied_places = [1] * 77 + [0] * 3
    random.shuffle(occupied_places)

    for i in range(80):
        price_per_hour = get_price_per_hour(types_of_vehicle[i])

        if occupied_places[i] == 1:
            parking_place_id = get_correct_column_for_parking_place(i)
            plate_number = generate_plate_number()
            entry_time = generate_random_datetime()
            parkedCar = ParkedCar.create(
                plate_number=plate_number,
                type_of_vehicle=types_of_vehicle[i],
                entry_time=entry_time,
                price=0,
                price_per_hour=price_per_hour,
            )
            ParkingPlace.create(
                parking_place_id=parking_place_id,
                type_of_vehicle=types_of_vehicle[i],
                price_per_hour=price_per_hour,
                occupied_by=parkedCar.plate_number,
                occupied=True,
                entry_time=entry_time,
                price=0,
            )
        else:
            ParkingPlace.create(
                parking_place_id=get_correct_column_for_parking_place(i),
                type_of_vehicle=types_of_vehicle[i],
                price_per_hour=price_per_hour,
                occupied_by=None,
                occupied=False,
                entry_time=None,
                price=0,
            )


def create_data_to_populate_payment_table():
    if Payment.select().count() == 0:
        for i in range(15):
            plate_number = generate_plate_number()
            type_of_vehicle = random.randint(1, 4)
            account_email = ""
            price = round(random.uniform(1.0, 100.0), 2)
            payment_date = generate_random_datetime()

            Payment.create(
                payment_id=i + 1,
                plate_number=plate_number,
                type_of_vehicle=type_of_vehicle,
                account_email=account_email,
                price=price,
                payment_date=payment_date,
            )


def generate_plate_number():
    valid_regions = read_valid_regions()
    region = random.choice(valid_regions)
    country = "RO"

    if region == "B":
        number = random.randint(1, 999)
    else:
        number = random.randint(1, 99)

    while True:
        letter_combination = ''.join(random.choices(string.ascii_uppercase.replace('Q', ''), k=3))
        if not (letter_combination.startswith("I") or letter_combination.startswith("O") or
                letter_combination == "III" or letter_combination == "OOO"):
            break

    if number < 10:
        plate_number = country + " " + region + " 0" + str(number) + " " + letter_combination
    else:
        plate_number = country + " " + region + " " + str(number) + " " + letter_combination

    return plate_number


def generate_random_datetime():
    current_date = datetime.datetime.now()

    start_date = current_date - datetime.timedelta(days=1)
    end_date = current_date

    total_seconds = int((end_date - start_date).total_seconds())

    random_seconds = random.randint(0, total_seconds)
    random_date = start_date + datetime.timedelta(seconds=random_seconds)

    return random_date
