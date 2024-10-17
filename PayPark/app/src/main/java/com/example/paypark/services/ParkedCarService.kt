package com.example.paypark.services;


import com.example.paypark.models.Account
import com.example.paypark.models.ParkedCar
import com.example.paypark.models.ParkedCarResponse;

import retrofit2.Call;
import retrofit2.http.Body
import retrofit2.http.DELETE;
import retrofit2.http.GET;
import retrofit2.http.PATCH;
import retrofit2.http.POST;
import retrofit2.http.Path;

interface ParkedCarService {
    @POST("parkedCar")
    fun createParkedCar(@Body parkedCar: ParkedCar): Call<ParkedCarResponse>

    @GET("parkedCar/plate_number/{plate_number}")
    fun getParkedCar(@Path("plate_number")plateNumber: String): Call<ParkedCarResponse>
}
