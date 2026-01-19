<template>
  <div class="payment-container">
    <h1>Fixify - Secure Payment</h1>
    <p>Complete your transaction securely.</p>

    <div class="receipt-box" v-if="booking">
      <h3>Service Payment</h3>
      <p><strong>Service:</strong> {{ booking.serviceName }}</p>
      <p><strong>Amount:</strong> ₹{{ booking.amount }}</p>
      <p><strong>Provider:</strong> {{ booking.professionalName }}</p>
    </div>

    <div class="payment-methods">
      <h3>Select Payment Method</h3>
      <label class="payment-option">
        <input type="radio" v-model="selectedPayment" value="COD" />
        <span>Cash on Delivery</span>
      </label>

      <label class="payment-option">
        <input type="radio" v-model="selectedPayment" value="UPI" />
        <span>UPI Payment</span>
      </label>
      <input v-if="selectedPayment === 'UPI'" v-model="upiId" placeholder="Enter UPI ID" />

      <label class="payment-option">
        <input type="radio" v-model="selectedPayment" value="Card" />
        <span>Credit/Debit Card</span>
      </label>
      <div v-if="selectedPayment === 'Card'" class="card-inputs">
        <input v-model="cardNumber" placeholder="Card Number" maxlength="16" />
        <input v-model="expiryDate" placeholder="MM/YY" maxlength="5" />
        <input v-model="cvv" placeholder="CVV" maxlength="3" type="password" />
      </div>
    </div>

    <button v-if="booking" @click="processPayment" :disabled="!isPaymentValid || isProcessing">
      Pay ₹{{ booking?.amount || 0 }}
    </button>

    <p v-if="isProcessing" class="processing-message">
      ⚠️ Do not close this tab. Your transaction is being processed...
    </p>
    <p v-if="paymentSuccess" class="success-message">
      ✅ Payment Successful! Redirecting...
    </p>
    <p v-if="bookingComplete" class="booking-message">
      🎉 Your booking has been successfully completed!
    </p>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import axios from "axios";

export default {
  name: "Payment",
  setup() {
    const route = useRoute();
    const router = useRouter();
    const selectedPayment = ref("");
    const upiId = ref("");
    const cardNumber = ref("");
    const expiryDate = ref("");
    const cvv = ref("");
    const isProcessing = ref(false);
    const paymentSuccess = ref(false);
    const bookingComplete = ref(false);
    const booking = ref(null);

    onMounted(() => {
      console.log("Route Query:", route.query);
      booking.value = {
        bookingId: route.query.bookingId || "",
        serviceName: route.query.serviceName || "Unknown Service",
        amount: route.query.amount || 0,
        professionalName: route.query.professionalName || "Unknown Provider",
      };
    });

    const isPaymentValid = computed(() => {
      if (selectedPayment.value === "COD") return true;
      if (selectedPayment.value === "UPI") return upiId.value.length > 5;
      if (selectedPayment.value === "Card") 
        return cardNumber.value.length === 16 && expiryDate.value.length === 5 && cvv.value.length === 3;
      return false;
    });

    const processPayment = async () => {
      if (!booking.value.bookingId) {
        alert("Invalid booking details!");
        return;
      }
      isProcessing.value = true;
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          alert("User not authenticated!");
          return;
        }

        const response = await axios.post(
          "http://127.0.0.1:5000/payments",
          {
            booking_id: booking.value.bookingId,
            amount: booking.value.amount,
            method: selectedPayment.value,
          },
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );

        alert(response.data.message);
        paymentSuccess.value = true;

        setTimeout(() => {
          paymentSuccess.value = false;
          bookingComplete.value = true;
          setTimeout(() => {
            router.push(`/feedback/${booking.value.bookingId}`);
          }, 2000);
        }, 3000);
      } catch (error) {
        console.error("Payment failed:", error);
        alert("Payment failed! Try again.");
      } finally {
        isProcessing.value = false;
      }
    };

    return {
      selectedPayment, upiId, cardNumber, expiryDate, cvv, processPayment,
      isProcessing, paymentSuccess, bookingComplete, isPaymentValid, booking,
    };
  },
};
</script>


<style scoped>
.payment-container {
  max-width: 400px;
  margin: auto;
  text-align: center;
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 1.5rem;
  color: #2c3e50;
}

.receipt-box {
  text-align: left;
  margin: 10px 0;
  padding: 10px;
  background: #f4f4f4;
  border-radius: 5px;
}

.payment-option {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 10px 0;
}

.payment-option input {
  margin: 0;
  width: 16px;
  height: 16px;
  cursor: pointer;
}

input {
  width: 100%;
  padding: 8px;
  margin: 5px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.card-inputs input {
  display: block;
  margin-bottom: 10px;
}

button {
  width: 100%;
  padding: 10px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

button:disabled {
  background: gray;
  cursor: not-allowed;
}
</style>





