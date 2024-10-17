package com.example.paypark.activities

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import com.example.paypark.R
import com.example.paypark.models.AccountResponse
import com.example.paypark.services.AccountService
import com.example.paypark.validation.AccountValidation
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import org.mindrot.jbcrypt.BCrypt


class LogInActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_log_in)

        val logInButton = findViewById<Button>(R.id.buttonLogIn)
        val forgotPasswordButton = findViewById<Button>(R.id.buttonForgotPassword)
        val backButton = findViewById<TextView>(R.id.buttonBackLogInActivity)

        logInButton.setOnClickListener {
            val emailEditText = findViewById<EditText>(R.id.editTextEmailAddressLogIn)
            val passwordEditText = findViewById<EditText>(R.id.editTextPasswordLogIn)

            val accountValidation = AccountValidation()

            val email = emailEditText.text.toString()
            val password = passwordEditText.text.toString()

            if(accountValidation.isValidEmail(email) and accountValidation.isValidPassword(password))
                {
                logInButton.isEnabled = false

                val retrofit = Retrofit.Builder()
                        .baseUrl("http://192.168.100.22:8000/api/parking_service/")
                        .addConverterFactory(GsonConverterFactory.create())
                        .build()
                val service = retrofit.create(AccountService::class.java)
                val call = service.getAccount(email)

                call.enqueue(object : Callback<AccountResponse> {
                    override fun onResponse(call: Call<AccountResponse>, response: Response<AccountResponse>) {
                        if (response.isSuccessful) {
                            val accountResponse = response.body()
                            if (accountResponse != null) {
                                val account = accountResponse.account

                                if (BCrypt.checkpw(password, account.password)) {
                                    val intent = Intent(this@LogInActivity, MainActivity::class.java)
                                    intent.putExtra("userName", "${account.first_name} ${account.last_name}")
                                    intent.putExtra("email", "${account.email}")

                                    showToast("Login successful")

                                    startActivity(intent)
                                    finish()
                                } else {
                                    showToast("Incorrect password")
                                    logInButton.isEnabled = true
                                }
                            } else {
                                showToast("Failed to find account")
                                logInButton.isEnabled = true
                            }
                        } else {
                            showToast("Failed to log in. Error code: ${response.code()}")
                            logInButton.isEnabled = true
                        }
                    }

                    override fun onFailure(call: Call<AccountResponse>, t: Throwable) {
                        logInButton.isEnabled = true
                        showToast("Nf: ${t.message}")
                    }
                })
                } else {
                showToast("Please enter valid email and password")
            }
        }

        forgotPasswordButton.setOnClickListener {
            val intent = Intent(this, ForgotPasswordActivity::class.java)
            startActivity(intent)
        }

        backButton.setOnClickListener {
            finish()
        }
    }

    private fun showToast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }
}
