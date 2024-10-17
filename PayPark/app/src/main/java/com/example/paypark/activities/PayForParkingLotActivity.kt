package com.example.paypark.activities

import PaymentValidation
import android.os.Build
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import com.example.paypark.PlateNumberValidation
import com.example.paypark.R
import com.example.paypark.models.ParkedCarResponse
import com.example.paypark.models.Payment
import com.example.paypark.models.PaymentResponse
import com.example.paypark.models.PaymentsResponse
import com.example.paypark.services.ParkedCarService
import com.example.paypark.services.PaymentService
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.lang.Integer.parseInt
import java.text.SimpleDateFormat
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter
import java.util.Date
import java.util.Locale

class PayForParkingLotActivity : AppCompatActivity() {
    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_pay_for_parking_lot)

        var price = 0.0f
        var typeOfVehicle = 0
        val email = intent.getStringExtra("email")

        val paymentValidation = PaymentValidation()
        val plateNumberValidation = PlateNumberValidation()

        val payButton = findViewById<Button>(R.id.buttonPay)
        val findCarButton = findViewById<Button>(R.id.buttonFindCar)
        val plateNumberEditText = findViewById<EditText>(R.id.editTextPlateNumber)

        val entryDateTextView = findViewById<TextView>(R.id.textViewEntryDate)
        val paymentDateTextView = findViewById<TextView>(R.id.textViewPaymentDate)
        val timeDifferenceTextView = findViewById<TextView>(R.id.textViewTimeDifference)
        val vehicleTypeTextView = findViewById<TextView>(R.id.textViewVehicleType)
        val pricePerHourTextView = findViewById<TextView>(R.id.textViewPricePerHour)

        val amountToBePaidTextView = findViewById<TextView>(R.id.textViewAmountToBePaid)

        val emailEditTextBox = findViewById<EditText>(R.id.editTextPayParkingPlaceEmail)

        if(email != null) {
            emailEditTextBox.setText(email)
        }

        val backButton = findViewById<TextView>(R.id.buttonBackPayForParkingLotActivity)

        val retrofit = Retrofit.Builder()
            .baseUrl("http://192.168.100.22:8000/api/parking_service/")
            .addConverterFactory(GsonConverterFactory.create())
            .build()

        val parkedCarService = retrofit.create(ParkedCarService::class.java)
        val paymentService = retrofit.create(PaymentService::class.java)

        findCarButton.setOnClickListener {
            val plateNumber = plateNumberEditText.text.toString()

            if (plateNumberValidation.validateNumber(plateNumber) == true) {
                val getCall = parkedCarService.getParkedCar(plateNumber)
                getCall.enqueue(object : Callback<ParkedCarResponse> {
                    override fun onResponse(
                        call: Call<ParkedCarResponse>,
                        response: Response<ParkedCarResponse>
                    ) {
                        if (response.isSuccessful) {
                            val parkedCarResponse = response.body()
                            if (parkedCarResponse != null) {
                                val parkedCar = parkedCarResponse.parkedCar

                                val inputDateFormat =
                                    SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault())
                                val outputDateFormat =
                                    SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault())

                                val getPayment = paymentService.getPayment(plateNumber)
                                getPayment.enqueue(object : Callback<PaymentResponse>{
                                    override fun onResponse(
                                        call: Call<PaymentResponse>,
                                        response: Response<PaymentResponse>
                                    ) {
                                        if (response.isSuccessful){
                                            val paymentResponse = response.body()
                                            if(paymentResponse != null) {
                                                var payment = paymentResponse.payment

                                                val currentDate = Date()
                                                val paymentDateString =
                                                    outputDateFormat.format(currentDate)

                                                entryDateTextView.text =
                                                    "Entry Time: " + outputDateFormat.format(
                                                        inputDateFormat.parse(payment.payment_date)
                                                    )

                                                paymentDateTextView.text =
                                                    "Payment Time: " + paymentDateString

                                                val entryDate =
                                                    inputDateFormat.parse(payment.payment_date)
                                                val paymentDate =
                                                    outputDateFormat.parse(paymentDateString)

                                                val timeDifferenceInMillis: Double = (paymentDate.time - entryDate.time).toDouble()
                                                val hoursDifference: Double = timeDifferenceInMillis / (1000.0 * 60 * 60)

                                                val formattedHoursDifference: String = String.format("%.2f", hoursDifference)
                                                val roundedHoursDifference: Double = formattedHoursDifference.toDouble()
                                                val timeDifferenceString = "$roundedHoursDifference hours"

                                                price =
                                                    (parkedCar.price_per_hour * roundedHoursDifference).toFloat()
                                                val formattedPrice : String = String.format("%.2f", price)
                                                price =  formattedPrice.toFloat()

                                                typeOfVehicle = parkedCar.type_of_vehicle

                                                timeDifferenceTextView.text =
                                                    "Total Time: " + timeDifferenceString
                                                vehicleTypeTextView.text =
                                                    "Type of vehicle: " + parkedCar.type_of_vehicle.toString()
                                                pricePerHourTextView.text =
                                                    "Price/Hour: " + parkedCar.price_per_hour.toString() + " LEI"

                                                amountToBePaidTextView.text =
                                                    "Amount: " + price.toString() + " LEI"
                                            }else{
                                                showToast("Failed to retrieve payment details")
                                            }
                                        }else{
                                            val currentDate = Date()
                                            val paymentDateString = outputDateFormat.format(currentDate)

                                            entryDateTextView.text = "Entry Time: " + outputDateFormat.format(
                                                inputDateFormat.parse(parkedCar.entry_time)
                                            )

                                            paymentDateTextView.text = "Payment Time: " + paymentDateString

                                            val entryDate = inputDateFormat.parse(parkedCar.entry_time)
                                            val paymentDate = outputDateFormat.parse(paymentDateString)

                                            val timeDifferenceInMillis = paymentDate.time - entryDate.time
                                            val hoursDifference = timeDifferenceInMillis / (1000.0 * 60 * 60)

                                            val formattedHoursDifference: String = String.format("%.2f", hoursDifference)
                                            val roundedHoursDifference: Double = formattedHoursDifference.toDouble()
                                            val timeDifferenceString = "$roundedHoursDifference hours"

                                            price = (parkedCar.price_per_hour * hoursDifference).toFloat()
                                            val formattedPrice : String = String.format("%.2f", price)
                                            price =  formattedPrice.toFloat()

                                            typeOfVehicle = parkedCar.type_of_vehicle

                                            timeDifferenceTextView.text = "Total Time: " + timeDifferenceString
                                            vehicleTypeTextView.text =
                                                "Type of vehicle: " + parkedCar.type_of_vehicle.toString()
                                            pricePerHourTextView.text =
                                                "Price/Hour: " + parkedCar.price_per_hour.toString() + " LEI"

                                            amountToBePaidTextView.text = "Amount: " + price.toString() + " LEI"
                                        }
                                    }

                                    override fun onFailure(
                                        call: Call<PaymentResponse>,
                                        t: Throwable
                                    ) {

                                    }
                                })
                            } else {
                                amountToBePaidTextView.text = "Amount: Not available"
                            }
                        } else {
                            showToast("Failed to retrieve car details")
                        }
                    }

                    override fun onFailure(call: Call<ParkedCarResponse>, t: Throwable) {
                        t.message?.let {
                            showToast("Network request failed: $it")
                        } ?: showToast("Network request failed")
                    }
                })
            }else{
                showToast("Incorrect plate number!")
            }
        }


        payButton.setOnClickListener {
            val plateNumber = plateNumberEditText.text.toString()

            val editTextCardNumber = findViewById<EditText>(R.id.editTextCardNumber)
            val editTextExpiryDate = findViewById<EditText>(R.id.editTextExpiryDate)
            val editTextCVC = findViewById<EditText>(R.id.editTextCVC)

            val cardNumber = editTextCardNumber.text.toString()
            val expiryDate = editTextExpiryDate.text.toString()
            val cvc = editTextCVC.text.toString()

            val currentDateTime = LocalDateTime.now()
            val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss")
            val formattedDateTime = currentDateTime.format(formatter)

            if (paymentValidation.validateCardNumber(cardNumber) &&
                paymentValidation.validateExpiryDate(expiryDate) &&
                paymentValidation.validateCvc(cvc)) {

                val getPayment = paymentService.getAllPayments()
                getPayment.enqueue(object : Callback<PaymentsResponse> {
                    override fun onResponse(
                        call: Call<PaymentsResponse>,
                        response: Response<PaymentsResponse>
                    ) {
                        if (response.isSuccessful) {
                            val paymentList = response.body()
                            if (paymentList != null) {
                                val listSize = paymentList.payments.size

                                val paymentCall = paymentService.createPayment(
                                    Payment(
                                        payment_id = listSize + 1,
                                        plate_number = plateNumber,
                                        type_of_vehicle = typeOfVehicle,
                                        account_email = emailEditTextBox.text.toString(),
                                        price = price,
                                        payment_date = formattedDateTime
                                    )
                                )
                                paymentCall.enqueue(object : Callback<PaymentResponse> {
                                    override fun onResponse(
                                        call: Call<PaymentResponse>,
                                        response: Response<PaymentResponse>
                                    ) {
                                        if (response.isSuccessful) {
                                            Log.d("TAG", "PaymentCall response: ${response.raw()}")
                                            payButton.isEnabled = false
                                            findCarButton.isEnabled = true

                                            showToast("Payment successfully made")
                                            finish()
                                        } else {
                                            showToast("Failed to create payment!")
                                        }
                                    }

                                    override fun onFailure(call: Call<PaymentResponse>, t: Throwable) {
                                        showToast("Network request failed: ${t.message}")
                                    }
                                })
                                showToast("Payment processing...")
                            } else {
                                showToast("Failed to fetch the payments list data!")
                            }
                        } else {
                            showToast("Failed to fetch the payments list data!")
                        }
                    }

                    override fun onFailure(call: Call<PaymentsResponse>, t: Throwable) {
                        showToast("${t.message}")
                        backButton.setText(t.message)
                    }
                })

            } else {
                showToast("Incorrect Card Details!")
            }
        }



        backButton.setOnClickListener {
            finish()
        }
    }

    private fun showToast(message: String) {
        Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
    }

    fun Float.toTwoDecimalPlaces(): Float {
        return String.format("%.2f", this).toFloat()
    }
}
