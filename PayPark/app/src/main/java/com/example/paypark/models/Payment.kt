package com.example.paypark.models

data class Payment(
    val payment_id: Int,
    val plate_number: String,
    val type_of_vehicle: Int,
    val account_email: String,
    val price: Float,
    val payment_date: String
)

data class PaymentResponse(
    val payment: Payment,
    val links: Links
)

data class PaymentsResponse(
    val payments: List<Payment>,
)