package com.example.paypark.services

import com.example.paypark.models.ParkingPlaceListResponse
import com.example.paypark.models.ParkingPlaceResponse
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.PATCH
import retrofit2.http.Path

interface ParkingPlaceService {
    @GET("parkingPlace/{occupied_by}")
    fun getParkedCar(@Path("occupied_by") occupiedBy: String): Call<ParkingPlaceResponse>

    @GET("ParkingPlaces")
    fun getAllParkingPlaces(): Call<ParkingPlaceListResponse>

    @GET("emptyParkingPlaces")
    fun getAllEmptyParkingPlaces(): Call<ParkingPlaceListResponse>

    @PATCH("parkingPlace/parking_place_id/{parking_place_id}")
    fun updateParkingPlace(@Path("parking_place_id") parkingPlaceId: String, @Body payload: Map<String, String>): Call<Void>

    @DELETE("parkingPlace/{occupied_by}")
    fun deleteParkingPlace(@Path("occupied_by") occupiedBy: String): Call<Void>
}
