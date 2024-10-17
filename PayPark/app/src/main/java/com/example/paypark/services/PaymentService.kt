package com.example.paypark.services

import com.example.paypark.models.Payment
import com.example.paypark.models.PaymentResponse
import com.example.paypark.models.PaymentsResponse

import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.DELETE
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.PUT
import retrofit2.http.Path

interface PaymentService {
    @POST("payment")
    fun createPayment(@Body payment: Payment): Call<PaymentResponse>

    @GET("payment/plate_number/{plate_number}")
    fun getPayment(@Path("plate_number") plateNumber: String): Call<PaymentResponse>

    @GET("payments")
    fun getAllPayments(): Call<PaymentsResponse>

    @PUT("payment/{payment_id}")
    fun updatePayment(
        @Path("payment_id") paymentId: Int,
        @Body payment: Payment
    ): Call<PaymentResponse>

    @DELETE("payment/{payment_id}")
    fun deletePayment(@Path("payment_id") paymentId: Int): Call<Void>
}
