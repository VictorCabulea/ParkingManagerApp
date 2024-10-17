package com.example.paypark.models

data class ParkingPlaceResponse(
    val parkingPlace: ParkingPlace,
    val links: Links
)

data class ParkingPlace(
    val parking_place_id: String,
    val type_of_vehicle: Int,
    val occupied: Boolean,
    val occupied_by: String,
    val entry_time: String,
)

data class ParkingPlaceListResponse(
    val emptyParkingPlaces: List<ParkingPlaceResponse>
)
