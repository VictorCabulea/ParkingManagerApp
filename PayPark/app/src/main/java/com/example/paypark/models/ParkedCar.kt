package com.example.paypark.models

data class ParkedCar(
    val plate_number: String,
    val type_of_vehicle: Int,
    val entry_time: String,
    val price_per_hour: Int
)

data class ParkedCarResponse(
    val parkedCar: ParkedCar,
    val links: Links
)
