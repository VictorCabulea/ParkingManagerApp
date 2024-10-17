import android.os.Build
import androidx.annotation.RequiresApi
import java.time.LocalDate
import java.util.regex.Pattern

class PaymentValidation {

    fun validateCvc(cvc: String): Boolean {
        if (cvc.length != 3 || !cvc.matches(Regex("\\d+"))) {
            return false
        }
        return true
    }

    @RequiresApi(Build.VERSION_CODES.O)
    fun validateExpiryDate(expiryDate: String): Boolean {
        if (expiryDate.length != 5 || expiryDate[2] != '/') {
            return false
        }
        try {
            val expiryMonth = expiryDate.substring(0, 2).toInt()
            val expiryYear = expiryDate.substring(3).toInt()
            val correctExpiryYear = "20$expiryYear"
            val currentMonth = LocalDate.now().monthValue
            val currentYear = LocalDate.now().year
            if (correctExpiryYear.toInt() < currentYear || (expiryYear == currentYear && expiryMonth < currentMonth)) {
                return false
            }
        } catch (e: NumberFormatException) {
            return false
        }
        return true
    }

    fun validateCardNumber(cardNumber: String): Boolean {
        val pattern: Pattern = Pattern.compile("^\\d{4}\\s\\d{4}\\s\\d{4}\\s\\d{4}$")
        return pattern.matcher(cardNumber).matches()
    }
}
