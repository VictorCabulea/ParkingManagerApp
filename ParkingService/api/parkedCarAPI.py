from datetime import datetime
from fastapi import APIRouter, Response, HTTPException, status
from database.database import ParkedCar
from dto.parkedCarDTO import ParkedCarDTO

router = APIRouter()


@router.post("/api/parking_service/parkedCar", status_code=status.HTTP_201_CREATED)
async def create_parked_car(parkedCar: ParkedCarDTO, response: Response):
    if parkedCar.type_of_vehicle == 1:
        price_per_hour = 5
    elif parkedCar.type_of_vehicle == 2:
        price_per_hour = 3
    elif parkedCar.type_of_vehicle == 3:
        price_per_hour = 2
    else:
        price_per_hour = 1

    new_parked_car = ParkedCar.create(
        plate_number=parkedCar.plate_number,
        type_of_vehicle=parkedCar.type_of_vehicle,
        entry_time=parkedCar.entry_time,
        price_per_hour=price_per_hour
    )

    response.status_code = status.HTTP_201_CREATED

    return {
        "account": {
            "plate_number": new_parked_car.plate_number,
            "type_of_vehicle": new_parked_car.type_of_vehicle,
            "entry_time": new_parked_car.entry_time,
            "price_per_hour": new_parked_car.price_per_hour,
            "links": {
                "self": {
                    "href": f"/api/parking_service/parkedCar/plate_number/{new_parked_car.plate_number}",
                    "type": "GET"
                },
                "delete": {
                    "href": f"/api/parking_service/parkedCar/plate_number/{new_parked_car.plate_number}",
                    "type": "DELETE"
                }
            }
        }
    }


@router.get("/api/parking_service/parkedCar/plate_number/{plate_number}")
async def get_parked_car(plate_number: str, response: Response):
    try:
        parked_car = ParkedCar.get(plate_number=plate_number)

        response.status_code = status.HTTP_200_OK

        return {
            "parkedCar": {
                "plate_number": parked_car.plate_number,
                "type_of_vehicle": parked_car.type_of_vehicle,
                "entry_time": parked_car.entry_time,
                "price_per_hour": parked_car.price_per_hour,
                "links": {
                    "delete": {
                        "href": f"/api/parking_service/parkedCar/plate_number/{plate_number}",
                        "type": "DELETE"
                    }
                }
            },
        }

    except ParkedCar.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with plate number {plate_number} not found",
        )


@router.delete("/api/parking_service/parkedCar/plate_number/{plate_number}")
async def delete_parked_car(plate_number: str, response: Response):
    try:
        parked_car = ParkedCar.get(plate_number=plate_number)
        parked_car.delete_instance()

        response.status_code = status.HTTP_204_NO_CONTENT

        return None

    except ParkedCar.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with plate number {plate_number} not found",
        )
