package com.example.paypark.activities

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.view.View
import android.widget.TextView
import com.example.paypark.R



class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val logInButton = findViewById<TextView>(R.id.buttonLogInActivity)
        val signUpButton = findViewById<TextView>(R.id.buttonSignUpActivity)
        val myAccountButton = findViewById<TextView>(R.id.buttonMyAccountActivity)
        val helpButton = findViewById<TextView>(R.id.buttonHelpActivity)
        val payForParkingLotButton = findViewById<TextView>(R.id.buttonPayForParkingLotActivity)
        val reserveParkingLotButton = findViewById<TextView>(R.id.buttonReserveParkingLotActivity)
        val logOutButton = findViewById<TextView>(R.id.buttonLogOut)
        reserveParkingLotButton.isEnabled=true

        val userName = intent.getStringExtra("userName")
        val email = intent.getStringExtra("email")

        if (userName != null) {
            logInButton.isEnabled=false
            logInButton.isClickable=false

            signUpButton.isEnabled= false
            signUpButton.isClickable= false

            logOutButton.isEnabled=true
            logOutButton.isClickable=true

            myAccountButton.isEnabled=true
            myAccountButton.isClickable=true

            reserveParkingLotButton.isEnabled=true
            reserveParkingLotButton.isClickable=true

            myAccountButton.text = userName
        }else{
            logInButton.isEnabled=true
            logInButton.isClickable=true

            signUpButton.isEnabled= true
            signUpButton.isClickable= true

            logOutButton.isEnabled=false
            logOutButton.isClickable=false

            myAccountButton.isEnabled=false
            myAccountButton.isClickable=false

            reserveParkingLotButton.isEnabled=false
            reserveParkingLotButton.isClickable=false

            myAccountButton.text = "My Account"
        }

        logInButton.setOnClickListener {
            val intent = Intent(this, LogInActivity::class.java)
            startActivity(intent)
        }

        signUpButton.setOnClickListener {
            val intent = Intent(this, SignUpActivity::class.java)
            startActivity(intent)
        }

        myAccountButton.setOnClickListener {
            val intent = Intent(this, MyAccountActivity::class.java)
            intent.putExtra("email", "$email")
            startActivity(intent)
        }

        helpButton.setOnClickListener {
            val intent = Intent(this, HelpActivity::class.java)
            startActivity(intent)
        }

        payForParkingLotButton.setOnClickListener {
            val intent = Intent(this, PayForParkingLotActivity::class.java)
            intent.putExtra("email", "$email")
            startActivity(intent)
        }

        reserveParkingLotButton.setOnClickListener {
            val intent = Intent(this, ReserveParkingLotActivity::class.java)
            intent.putExtra("email", "$email")
            startActivity(intent)
        }

        logOutButton.setOnClickListener {
            myAccountButton.setText("My Account")

            logInButton.isEnabled=true
            signUpButton.isEnabled= true
            logOutButton.isEnabled=false
            myAccountButton.isEnabled=false
            reserveParkingLotButton.isEnabled=false
        }
    }

    fun onExitButtonClick(view: View) {
        finish()
    }
}