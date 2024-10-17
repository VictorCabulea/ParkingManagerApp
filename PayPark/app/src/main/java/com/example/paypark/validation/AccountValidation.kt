package com.example.paypark.validation
import java.util.regex.Pattern

class AccountValidation {
    fun isValidName(name: String): Boolean {
        return name.length >= 3 && name[0].isUpperCase()
    }

    fun isValidEmail(email: String): Boolean {
        val emailPattern = Pattern.compile("^([\\w\\.-]+)@([a-zA-Z\\d\\.-]+)\\.([a-zA-Z]{2,})$")
        return emailPattern.matcher(email).matches()
    }

    fun isValidPassword(password: String): Boolean {
        return password.length >= 8 && Regex("[!@#\$%^&*(),.?\":{}|<>]").containsMatchIn(password)
    }

    fun isValidAccount(lastName: String, firstName: String, email: String, password: String): Boolean {
        return isValidName(lastName) && isValidName(firstName) && isValidEmail(email) && isValidPassword(password)
    }
}