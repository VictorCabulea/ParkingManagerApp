package com.example.paypark.activities

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import com.example.paypark.R
import com.example.paypark.models.Account
import com.example.paypark.models.AccountResponse
import com.example.paypark.services.AccountService
import com.example.paypark.validation.AccountValidation
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import org.mindrot.jbcrypt.BCrypt


class SignUpActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_sign_up)

        val signUpButton = findViewById<Button>(R.id.buttonSignUp)

        signUpButton.setOnClickListener {
            val firstNameEditText = findViewById<EditText>(R.id.editTextFirstNameSignUp)
            val lastNameEditText = findViewById<EditText>(R.id.editTextLastNameSignUp)
            val emailEditText = findViewById<EditText>(R.id.editTextEmailSignUp)
            val passwordEditText = findViewById<EditText>(R.id.editTextPasswordSignUp)
            val passwordRetypedEditText = findViewById<EditText>(R.id.editTextPassword2SignUp)

            val firstName = firstNameEditText.text.toString()
            val lastName = lastNameEditText.text.toString()
            val email = emailEditText.text.toString()
            val password = passwordEditText.text.toString()
            val passwordRetyped = passwordRetypedEditText.text.toString()

            val accountValidation = AccountValidation()

            if (password == passwordRetyped) {
                if(accountValidation.isValidAccount(lastName, firstName, email, password)) {
                    val hashedPassword = BCrypt.hashpw(password, BCrypt.gensalt(12))

                    val account = Account(email, hashedPassword, lastName, firstName, false, "")

                    val retrofit = Retrofit.Builder()
                        .baseUrl("http://192.168.100.22:8000/api/parking_service/")
                        .addConverterFactory(GsonConverterFactory.create())
                        .build()

                    val service = retrofit.create(AccountService::class.java)
                    val call = service.createAccount(account)

                    call.enqueue(object : Callback<AccountResponse> {
                        override fun onResponse(
                            call: Call<AccountResponse>,
                            response: Response<AccountResponse>
                        ) {
                            if (response.isSuccessful) {
                                showToast("Account created successfully")

                                val intent = Intent(this@SignUpActivity, MainActivity::class.java)
                                startActivity(intent)
                                finish()
                            } else {
                                showToast("Failed to create account. Error code: ${response.code()}")
                            }
                        }

                        override fun onFailure(call: Call<AccountResponse>, t: Throwable) {
                            showToast("Network request failed: ${t.message}")
                        }
                    })
                } else {
                    showToast("Invalid input. Please check your details.")
                }
            } else {
                showToast("Passwords do not match")
            }
        }

        val backButton = findViewById<TextView>(R.id.buttonBackSignUpActivity)

        backButton.setOnClickListener {
            finish()
        }
    }

    private fun showToast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }
}
