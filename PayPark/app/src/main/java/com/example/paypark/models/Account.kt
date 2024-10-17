package com.example.paypark.models

data class Account(
    val email: String,
    val password: String,
    val last_name: String,
    val first_name: String,
    val active_reservation: Boolean,
    val payments: String
)

data class AccountResponse(
    val account: Account,
    val links: Links
)

data class Links(
    val self: String,
    val update_password: String,
    val update_sold: String,
    val delete_account: String
)
