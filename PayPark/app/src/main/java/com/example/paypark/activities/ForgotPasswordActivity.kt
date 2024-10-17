package com.example.paypark.activities

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import com.example.paypark.R
import com.example.paypark.services.AccountService
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class ForgotPasswordActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_forgot_password)

        val resetPasswordButton = findViewById<TextView>(R.id.buttonResetPassword)
        val backButton = findViewById<TextView>(R.id.buttonBackForgotPasswordActivity)

        resetPasswordButton.setOnClickListener {
            val emailEditText = findViewById<EditText>(R.id.editTextEmailAddressForgotPassword)
            val email = emailEditText.text.toString().trim()

            if (email.isNotEmpty()) {
                val retrofit = Retrofit.Builder()
                    .baseUrl("http://192.168.100.22:8000/api/parking_service/")
                    .addConverterFactory(GsonConverterFactory.create())
                    .build()

                val service = retrofit.create(AccountService::class.java)
                val call = service.resetPassword(email)

                call.enqueue(object : Callback<Void> {
                    override fun onResponse(call: Call<Void>, response: Response<Void>) {
                        if (response.isSuccessful) {
                            resetPasswordButton.isEnabled=false
                            showToast("Password reset email sent")
                            finish()
                        } else {
                            showToast("Failed to send reset email. Error code: ${response.code()}")
                        }
                    }

                    override fun onFailure(call: Call<Void>, t: Throwable) {
                        showToast("Network request failed: ${t.message}")
                    }
                })
            } else {
                showToast("Please enter your email address")
            }
        }

        backButton.setOnClickListener {
            finish()
        }
    }

    private fun showToast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }
}