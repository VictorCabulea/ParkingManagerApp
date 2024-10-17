package com.example.paypark.activities

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.paypark.R
import com.example.paypark.models.Account
import com.example.paypark.models.AccountResponse
import com.example.paypark.services.AccountService
import com.example.paypark.validation.AccountValidation
import org.mindrot.jbcrypt.BCrypt
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class MyAccountActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_my_account)

        val searchAccountButton = findViewById<TextView>(R.id.buttonSearchAccountMyAccount)
        val updateAccountButton = findViewById<TextView>(R.id.buttonUpdateAccount)
        val deleteAccountButton = findViewById<TextView>(R.id.buttonDeleteAccount)

        val backButton = findViewById<TextView>(R.id.buttonBackMyAccountActivity)

        val firstNameEditText = findViewById<EditText>(R.id.editTextFirstNameMyAccount)
        val lastNameEditText = findViewById<EditText>(R.id.editTextLastNameMyAccount)
        val currentPasswordEditText = findViewById<EditText>(R.id.editTextCurrentPasswordMyAccount)
        val newPasswordEditText = findViewById<EditText>(R.id.editTextNewPasswordMyAccount)
        val newPasswordRetypeEditText = findViewById<EditText>(R.id.editTextNewPasswordRetypeMyAccount)
        val paymentsTextView = findViewById<TextView>(R.id.textViewPayments)

        var email = intent.getStringExtra("email")

        var currentPasswordReceivedFromServer = ""
        var activeReservation = false
        var payments = ""

        val accountValidation = AccountValidation()

        if (email != null) {
            searchAccountButton.setOnClickListener {
                if (accountValidation.isValidEmail(email)) {
                    val retrofit = Retrofit.Builder()
                        .baseUrl("http://192.168.100.22:8000/api/parking_service/")
                        .addConverterFactory(GsonConverterFactory.create())
                        .build()

                    val service = retrofit.create(AccountService::class.java)
                    val getAccountCall = service.getAccount(email)

                    getAccountCall.enqueue(object : Callback<AccountResponse> {
                        override fun onResponse(
                            call: Call<AccountResponse>,
                            response: Response<AccountResponse>
                        ) {
                            if (response.isSuccessful) {
                                val accountResponse = response.body()
                                if (accountResponse != null) {
                                    Log.d("TAG", "Account response: ${response.body()}")
                                    val account = accountResponse.account
                                    lastNameEditText.setText(account.last_name)
                                    firstNameEditText.setText(account.first_name)
                                    currentPasswordReceivedFromServer = account.password
                                    paymentsTextView.setText(paymentsTextView.text.toString() +
                                            "\n" + account.payments)
                                    activeReservation = account.active_reservation
                                    payments = account.payments
                                } else {
                                    showToast("Failed to retrieve account details")
                                }
                            } else {
                                showToast("Failed to retrieve account. Error code: ${response.code()}")
                            }
                        }

                        override fun onFailure(call: Call<AccountResponse>, t: Throwable) {
                            showToast("Network request failed: ${t.message}")
                        }
                    })
                }
            }
        }

        updateAccountButton.setOnClickListener {
            val lastName = lastNameEditText.text.toString()
            val firstName = firstNameEditText.text.toString()
            val currentPassword = currentPasswordEditText.text.toString()
            val newPassword = newPasswordEditText.text.toString()
            val newPasswordRetype = newPasswordRetypeEditText.text.toString()

            if(BCrypt.checkpw(currentPassword, currentPasswordReceivedFromServer)) {
                if (newPassword == newPasswordRetype) {
                    if (email != null){
                    if (accountValidation.isValidAccount(lastName, firstName, email, newPassword)) {
                        val newPasswordHashed = BCrypt.hashpw(newPassword, BCrypt.gensalt())
                        val updatedAccount =
                            Account(email, newPasswordHashed, lastName, firstName, activeReservation, payments)

                        val retrofit = Retrofit.Builder()
                            .baseUrl("http://192.168.100.22:8000/api/parking_service/")
                            .addConverterFactory(GsonConverterFactory.create())
                            .build()

                        val service = retrofit.create(AccountService::class.java)
                        val updateAccountCall = service.updateAccount(email, updatedAccount)

                        updateAccountCall.enqueue(object : Callback<Void> {
                            override fun onResponse(
                                call: Call<Void>, response: Response<Void>
                            ) {
                                if (response.isSuccessful) {
                                    showToast("Account successfully updated!")
                                } else {
                                    showToast("Account could not be updated!. Error code: ${response.code()}")
                                }
                            }

                            override fun onFailure(call: Call<Void>, t: Throwable) {
                                showToast("Network request failed: ${t.message}")
                            }
                        })
                    }
                    }else{
                        showToast("Invalid account data!")
                    }
                }else{
                    showToast("Current Password is not correct!")
                }
            }else{
                showToast("Insert a valid password!")
            }
        }

        deleteAccountButton.setOnClickListener {
            if (email != null) {
                val retrofit = Retrofit.Builder()
                    .baseUrl("http://192.168.100.22:8000/api/parking_service/")
                    .addConverterFactory(GsonConverterFactory.create())
                    .build()

                val service = retrofit.create(AccountService::class.java)
                val deleteAccountCall = service.deleteAccount(email)
                val getAccountCall = service.getAccount(email)

                getAccountCall.enqueue(object : Callback<AccountResponse> {
                    override fun onResponse(
                        call: Call<AccountResponse>,
                        response: Response<AccountResponse>
                    ) {
                        if (response.isSuccessful) {
                            val accountResponse = response.body()
                            if (accountResponse != null) {
                                val account = accountResponse.account
                                activeReservation = account.active_reservation

                                if(activeReservation == false){
                                    deleteAccountCall.enqueue(object : Callback<Void> {
                                        override fun onResponse(
                                            call: Call<Void>, response: Response<Void>
                                        ) {
                                            if (response.isSuccessful) {
                                                val intent =
                                                    Intent(this@MyAccountActivity, MainActivity::class.java)
                                                intent.putExtra("userName", "")
                                                intent.putExtra("email", "")

                                                showToast("Account successfully deleted!")

                                                startActivity(intent)
                                                finish()
                                            } else {
                                                showToast("Account could not be deleted!. Error code: ${response.code()}")
                                            }
                                        }

                                        override fun onFailure(call: Call<Void>, t: Throwable) {
                                            showToast("Network request failed: ${t.message}")
                                        }
                                    })
                                }
                                else{
                                    showToast("The account cannot be deleted because it has an active reservation!")
                                }
                            } else {
                                showToast("Failed to retrieve account details")
                            }
                        } else {
                            showToast("Failed to retrieve account. Error code: ${response.code()}")
                        }
                    }

                    override fun onFailure(call: Call<AccountResponse>, t: Throwable) {
                        showToast("Network request failed: ${t.message}")
                    }
                })
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
