from datetime import datetime

from fastapi import APIRouter, Response, HTTPException, status
from database.database import ParkingPlace

router = APIRouter()


@router.get("/api/parking_service/parkingPlace/occupied_by/{occupied_by}")
async def get_parking_place(occupied_by: str, response: Response):
    try:
        parking_place = ParkingPlace.get(ParkingPlace.occupied_by == occupied_by)
        response.status_code = status.HTTP_200_OK
        return {
            "parkingPlace": {
                "parking_place_id": parking_place.parking_place_id,
                "type_of_vehicle": parking_place.type_of_vehicle,
                "occupied": parking_place.occupied,
                "occupied_by": parking_place.occupied_by,
                "entry_time": parking_place.entry_time,
                "links": {
                    "update": {
                        "href": f"/api/parking_service/parkingPlace/parking_place_id/{parking_place.parking_place_id}",
                        "type": "PATCH"
                    }
                }
            },
        }
    except ParkingPlace.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Parking place occupied by {occupied_by} not found",
        )


@router.get("/api/parking_service/ParkingPlaces")
async def get_all_parking_places(response: Response):
    parking_places = ParkingPlace.select()

    if parking_places:
        response.status_code = status.HTTP_200_OK
        return {
            "ParkingPlaces": [
                {
                    "parkingPlace": {
                        "parking_place_id": parking_place.parking_place_id,
                        "type_of_vehicle": parking_place.type_of_vehicle,
                        "occupied": parking_place.occupied,
                        "occupied_by": parking_place.occupied_by,
                        "entry_time": parking_place.entry_time,
                        "links": {
                            "update": {
                                "href": f"/api/parking_service/parkingPlace/parking_place_id/{parking_place.parking_place_id}",
                                "type": "PATCH"
                            }
                        }
                    }
                }
                for parking_place in parking_places
            ]
        }
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": "No parking places found."}


@router.get("/api/parking_service/emptyParkingPlaces")
async def get_all_empty_parking_places(response: Response):
    empty_parking_places = ParkingPlace.select().where(ParkingPlace.occupied == False)

    if empty_parking_places:
        response.status_code = status.HTTP_200_OK
        return {
            "emptyParkingPlaces": [
                {
                    "parkingPlace": {
                        "parking_place_id": parking_place.parking_place_id,
                        "type_of_vehicle": parking_place.type_of_vehicle,
                        "occupied": parking_place.occupied,
                        "occupied_by": parking_place.occupied_by,
                        "entry_time": parking_place.entry_time,
                        "links": {
                            "update": {
                                "href": f"/api/parking_service/parkingPlace/parking_place_id/{parking_place.parking_place_id}",
                                "type": "PATCH"
                            }
                        }
                    }
                }
                for parking_place in empty_parking_places
            ]
        }
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": "No empty parking places available."}


@router.patch("/api/parking_service/parkingPlace/parking_place_id/{parking_place_id}")
async def update_parking_place(parking_place_id: str, payload: dict, response: Response):
    try:
        parking_place = ParkingPlace.get(ParkingPlace.parking_place_id == parking_place_id)
        if parking_place.occupied:
            parking_place.occupied = False
            parking_place.occupied_by = None
            parking_place.entry_time = None
        else:
            parking_place.occupied = True
            parking_place.occupied_by = parking_place.occupied = payload['occupied_by']
            parking_place.entry_time = datetime.now()

        parking_place.save()

        response.status_code = status.HTTP_204_NO_CONTENT
        return None

    except ParkingPlace.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Parking place with id {id} not found",
        )
