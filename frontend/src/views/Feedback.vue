<template>
  <div class="container mt-5">
    <div class="feedback-card mx-auto p-4 shadow-lg">
      <h2 class="text-center text-primary mb-4">We Value Your Feedback! ⭐</h2>

      <div v-if="loading" class="text-center text-muted">
        <p>Loading booking details...</p>
      </div>

      <div v-else>
        <div class="card p-4 rounded-4 border-0 shadow-sm">
          <div>
            <h5 class="mb-1 text-dark">{{ booking.service_name }}</h5>
            <p class="text-muted mb-0">
              <strong>Professional:</strong> {{ booking.professional_name }}
            </p>
          </div>

          <!-- Rating Section -->
          <div class="mt-4">
            <label class="form-label fw-semibold">Rate the Service:</label>
            <div class="rating-container">
              <span 
                v-for="num in 5" 
                :key="num" 
                @click="rating = num"
                @mouseover="hoverRating = num"
                @mouseleave="hoverRating= rating"
                class="star"
                :class="{ 'selected': num <= rating, 'hovered': num <= hoverRating }"
              >
                ★
              </span>
            </div>
          </div>

          <!-- Feedback Section -->
          <div class="mt-3">
            <label class="form-label fw-semibold">Your Feedback:</label>
            <textarea 
              v-model="feedback" 
              class="form-control rounded-3 shadow-sm" 
              rows="3" 
              placeholder="Tell us about your experience..."
            ></textarea>
          </div>

          <!-- Submit Button -->
          <button class="btn btn-primary w-100 mt-4" @click="submitReview">
            <i class="fas fa-paper-plane me-2"></i> Submit Review
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";

const props = defineProps(["bookingId"]);
const router = useRouter();

const rating = ref(0);
const hoverRating = ref(0);

const feedback = ref("");
const loading = ref(false);
const booking = ref({});

const fetchBookingDetails = async () => {
  loading.value = true;
  try {
    const token = localStorage.getItem("token");
    if (!token) return;

    const response = await axios.get(`http://127.0.0.1:5000/booking/${props.bookingId}`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    booking.value = response.data;
  } catch (error) {
    console.error("Error fetching booking details:", error);
  } finally {
    loading.value = false;
  }
};

const submitReview = async () => {
  if (!rating.value || !feedback.value.trim()) {
    alert("Please provide a rating and feedback before submitting.");
    return;
  }

  try {
    const token = localStorage.getItem("token");
    if (!token) return;

    const response = await axios.post(
      `http://127.0.0.1:5000/feedback/${props.bookingId}`,
      { rating:rating.value, feedback:feedback.value },
      { headers: { Authorization: `Bearer ${token}` } }
    );

    console.log("API Response:", response.data);

    alert("Thank you for your feedback! 🎉");
    router.push("/customerdashboard"); // Redirect after review
  } catch (error) {
    console.error("Error submitting feedback:", error.response?.data || error);
    alert(error.response?.data?.error || "Something went wrong. Please try again.");
  }
};

onMounted(() => {
  console.log("Booking ID received in Feedback.vue:", props.bookingId);
  fetchBookingDetails();
});
</script>


<style scoped>
.feedback-card {
  max-width: 500px;
  background: #ffffff;
  border-radius: 15px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.rating-container {
  display: flex;
  font-size: 24px;
  cursor: pointer;
}

.star {
  transition: color 0.2s;
  color: #ccc;
  padding: 5px;
}

.star.selected {
  color: #ffc107;
}

.star.hovered {
  color: #ff9800;
}
</style>

