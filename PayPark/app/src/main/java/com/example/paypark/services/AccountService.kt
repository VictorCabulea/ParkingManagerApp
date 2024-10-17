package com.example.paypark.services

import com.example.paypark.models.*
import retrofit2.Call
import retrofit2.http.*

interface AccountService {
    @POST("account")
    fun createAccount(@Body account: Account): Call<AccountResponse>

    @GET("account/email/{email}")
    fun getAccount(@Path("email") email: String): Call<AccountResponse>

    @PATCH("account/email/{email}")
    fun updateAccount(@Path("email") email: String, @Body updatedAccount: Account): Call<Void>

    @PATCH("account/email/{email}/active_reservation")
    fun update_account_active_reservation(@Path("email") email: String): Call<Void>

    @POST("account/email/{email}/reset_password")
    fun resetPassword(@Path("email") email: String): Call<Void>

    @DELETE("account/email/{email}")
    fun deleteAccount(@Path("email") email: String): Call<Void>

}
