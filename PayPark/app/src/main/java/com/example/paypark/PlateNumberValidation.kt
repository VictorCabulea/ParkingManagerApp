package com.example.paypark

class PlateNumberValidation {

    val regions = listOf(
        "B", "BZ", "IL", "BR", "IF", "BV", "HR", "CV", "CJ", "AB",
        "TM", "BH", "HD", "CS", "GR", "CL", "TL", "CT", "VN", "GL",
        "BC", "VS", "NT", "IS", "SV", "BT", "MS", "SM", "DJ", "GJ",
        "SB", "VL", "OT", "PH"
    )

    fun validateNumber(plateNumber: String): Boolean {
        val splitPlateNumber = plateNumber.split(" ")
        if (splitPlateNumber.size == 4) {
            if (splitPlateNumber[0] == "RO") {
                if (splitPlateNumber[1] in regions) {
                    if (splitPlateNumber[2].isDigitsOnly() && splitPlateNumber[3].isAlphaOnly() && splitPlateNumber[3].length == 3) {
                        return true
                    }
                }
            }
        }
        return false
    }

    // Extension function to check if a string contains only digits
    fun String.isDigitsOnly(): Boolean {
        return this.all { it.isDigit() }
    }

    // Extension function to check if a string contains only alphabetic characters
    fun String.isAlphaOnly(): Boolean {
        return this.all { it.isLetter() }
    }

}