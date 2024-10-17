package com.example.paypark.activities

import android.os.Bundle
import android.util.Log
import android.widget.ArrayAdapter
import android.widget.Button
import android.widget.EditText
import android.widget.ListView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.paypark.R
import com.example.paypark.models.ParkedCar
import com.example.paypark.models.ParkedCarResponse
import com.example.paypark.models.ParkingPlaceListResponse
import com.example.paypark.models.ParkingPlaceResponse
import com.example.paypark.services.AccountService
import com.example.paypark.services.ParkedCarService
import com.example.paypark.services.ParkingPlaceService
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

class ReserveParkingLotActivity : AppCompatActivity() {

    private val parkingPlaces = mutableListOf<ParkingPlaceResponse>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_reserve_parking_lot)

        val email = intent.getStringExtra("email")

        val enteredPlateNumberEditText = findViewById<EditText>(R.id.editTextEnterPlateNumber)
        val emptyParkingPlacesList = findViewById<ListView>(R.id.listViewEmptyParkingPlaces)
        val reserveParkingPlaceButton = findViewById<Button>(R.id.buttonReserveParkingPlace)
        val backButton = findViewById<Button>(R.id.buttonBackReserveParkingPlace)

        val retrofit = Retrofit.Builder()
            .baseUrl("http://192.168.100.22:8000/api/parking_service/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val parkingPlaceService = retrofit.create(ParkingPlaceService::class.java)
        val parkedCarService = retrofit.create(ParkedCarService::class.java)
        val accountService = retrofit.create(AccountService::class.java)

        val call = parkingPlaceService.getAllEmptyParkingPlaces()

        call.enqueue(object : Callback<ParkingPlaceListResponse> {
            override fun onResponse(
                call: Call<ParkingPlaceListResponse>,
                response: Response<ParkingPlaceListResponse>
            ) {
                if (response.isSuccessful) {
                    val emptyParkingPlaces = response.body()?.emptyParkingPlaces
                    if (emptyParkingPlaces != null) {
                        parkingPlaces.clear()
                        parkingPlaces.addAll(emptyParkingPlaces)
                        updateListView(emptyParkingPlacesList)
                    }
                    Log.d("TAG", "emptyParkingPlaces response: $emptyParkingPlaces")
                } else {
                    showToast("Failed to fetch parking places. Error code: ${response.code()}")
                }
            }

            override fun onFailure(call: Call<ParkingPlaceListResponse>, t: Throwable) {
                showToast("Network request failed: ${t.message}")
            }
        })

        reserveParkingPlaceButton.setOnClickListener {
            val selectedPosition = emptyParkingPlacesList.checkedItemPosition
            if (selectedPosition != -1) {
                val selectedParkingPlace = parkingPlaces[selectedPosition].parkingPlace
                val enteredPlateNumber = enteredPlateNumberEditText.text.toString()

                val outputDateFormat =
                    SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault())
                val currentDate = Date()
                val paymentDateString =
                    outputDateFormat.format(currentDate)

                if (enteredPlateNumber.isNotEmpty()) {
                    val parkedCar = ParkedCar(
                        plate_number = enteredPlateNumber,
                        type_of_vehicle = selectedParkingPlace.type_of_vehicle,
                        entry_time = paymentDateString,
                        price_per_hour = 0
                    )

                    parkedCarService.createParkedCar(parkedCar).enqueue(object : Callback<ParkedCarResponse> {
                        override fun onResponse(call: Call<ParkedCarResponse>, response: Response<ParkedCarResponse>) {
                            if (response.isSuccessful) {
                                val updatePayload = mapOf(
                                    "occupied_by" to enteredPlateNumber
                                )

                                parkingPlaceService.updateParkingPlace(selectedParkingPlace.parking_place_id, updatePayload).enqueue(object : Callback<Void> {
                                    override fun onResponse(call: Call<Void>, response: Response<Void>) {
                                        if (response.isSuccessful) {

                                            if (email!=null){
                                                val updateAccountCall = accountService.update_account_active_reservation(email)

                                                updateAccountCall.enqueue(object : Callback<Void> {
                                                    override fun onResponse(
                                                        call: Call<Void>, response: Response<Void>
                                                    ) {
                                                        if (response.isSuccessful) {
                                                            showToast("Parking place reserved successfully")
                                                        } else {
                                                            showToast("Account could not be updated!. Error code: ${response.code()}")
                                                        }
                                                    }
                                                    override fun onFailure(call: Call<Void>, t: Throwable) {
                                                        showToast("Network request failed: ${t.message}")
                                                    }
                                                })

                                                finish()
                                            }
                                        } else {
                                            showToast("Failed to reserve parking place. Error code: ${response.code()}")
                                        }
                                    }

                                    override fun onFailure(call: Call<Void>, t: Throwable) {
                                        showToast("Failed to reserve parking place: ${t.message}")
                                    }
                                })
                            } else {
                                showToast("Failed to create parked car. Error code: ${response.code()}")
                            }
                        }

                        override fun onFailure(call: Call<ParkedCarResponse>, t: Throwable) {
                            showToast("Failed to create parked car: ${t.message}")
                        }
                    })
                } else {
                    showToast("Please enter a plate number")
                }
            } else {
                showToast("Please select a parking place")
            }
        }

        backButton.setOnClickListener {
            finish()
        }
    }

    private fun updateListView(listView: ListView) {
        val items = parkingPlaces.map {
            "ID: ${it.parkingPlace.parking_place_id}, Vehicle Type: ${it.parkingPlace.type_of_vehicle}"
        }
        val adapter = ArrayAdapter(this, android.R.layout.simple_list_item_single_choice, items)
        listView.adapter = adapter
        listView.choiceMode = ListView.CHOICE_MODE_SINGLE
    }

    private fun showToast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }
}
