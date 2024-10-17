from peewee import *


db = MySQLDatabase('parkingdatabase', user='root', password='victor', host='localhost', port=3306)


class BaseModel(Model):
    class Meta:
        database = db


class Account(BaseModel):
    email = CharField(max_length=30, unique=True, primary_key=True)
    password = CharField(max_length=60)
    last_name = CharField(max_length=30)
    first_name = CharField(max_length=30)
    active_reservation = BooleanField(default=False)
    payments = CharField(null=True)


class Payment(BaseModel):
    payment_id = IntegerField(unique=True, primary_key=True)
    plate_number = CharField(max_length=12)
    type_of_vehicle = IntegerField()
    account_email = CharField(max_length=30)
    price = DoubleField()
    payment_date = DateTimeField()


class ParkedCar(BaseModel):
    plate_number = CharField(max_length=12, unique=True, null=False, primary_key=True)
    type_of_vehicle = IntegerField()
    entry_time = DateTimeField()
    price_per_hour = IntegerField()


class ParkingPlace(BaseModel):
    parking_place_id = CharField(max_length=3, unique=True, primary_key=True)
    type_of_vehicle = IntegerField()
    occupied = BooleanField(default=False)
    occupied_by = CharField(max_length=12, null=True)
    entry_time = DateTimeField(null=True)


db.connect()

if ParkingPlace.table_exists():
    ParkingPlace.drop_table()

if ParkedCar.table_exists():
    ParkedCar.drop_table()

db.create_tables([Account, Payment, ParkingPlace, ParkedCar], safe=True)
