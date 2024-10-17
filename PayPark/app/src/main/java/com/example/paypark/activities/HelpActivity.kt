package com.example.paypark.activities

import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.EditText
import android.widget.TextView
import com.example.paypark.R

class HelpActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_help)


        val helpLoginTextView = findViewById<TextView>(R.id.textViewHelpLogin).apply {
            text = "Sectiunea \"LogIn\" va ajuta sa va autentificati in contul dvs."
        }

        val helpSignInTextView = findViewById<TextView>(R.id.textViewHelpSignIn).apply {
            text = "Sectiunea \"SignUp\" va ajuta sa creati un cont nou."
        }

        val helpMyAccountTextView = findViewById<TextView>(R.id.textViewHelpMyAccount).apply {
            text = "Sectiune \"MyAccount\" va ofera ajutor pentru gestionarea contului " +
                    "dumneavoastra. Poate fi accesata doar dupa autentificare."
        }

        val helpPaymentTextView = findViewById<TextView>(R.id.textViewHelpPayment).apply {
            text = "Sectiunea \"Pay For Parking Lot\" poate fi utilizata pentru a plati taxa de " +
                    "parcare, introducand numarul de inmatriculare al masinii pentru care doriti " +
                    "sa faceti plata."
        }

        val helpReservationTextView = findViewById<TextView>(R.id.textViewHelpReservation).apply {
            text = "Sectiunea \"Reserve A Parking Lot\" va ajuta sa faceti o rezervare a unui loc" +
                    " de parcare. Locul de parcare va fi rezervat din momentul in care faceti" +
                    " rezervarea, neputand fi ocupat de alte vehicule"
        }


        val backButton = findViewById<TextView>(R.id.buttonBackHelpActivity)

        backButton.setOnClickListener {
            finish()
        }
    }
}