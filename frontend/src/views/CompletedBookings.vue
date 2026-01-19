<template>
  <div class="container mt-4">
    <h2 class="text-center text-success mb-4 fw-bold">Completed Services</h2>

    <!-- Loader -->
    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-success" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="alert alert-danger text-center">
      {{ error }}
    </div>

    <!-- Completed Services Table -->
    <div class="table-responsive" v-if="completedBookings.length > 0">
      <table class="table table-hover align-middle shadow-sm">
        <thead class="table-dark text-white">
          <tr>
            <th scope="col" class="text-center">Sl No</th>
            <th scope="col">Service Name</th>
            <th scope="col">Professional</th>
            <th scope="col">Contact</th>
            <th scope="col">Service Date</th>
            <th scope="col">Rating</th>
            <th scope="col">Feedback</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(booking, index) in completedBookings" :key="booking.id">
            <td class="text-center fw-bold">{{ index + 1 }}</td>
            <td>{{ booking.service_name }}</td>
            <td class="fw-semibold text-success">{{ booking.professional_name }}</td>
            <td>{{ booking.professional_contact }}</td>
            <td>{{ formatDate(booking.scheduled_date) }}</td>
            <td>
              <span v-if="booking.rating">⭐ {{ booking.rating }} / 5</span>
              <span v-else class="text-muted">No rating</span>
            </td>
            <td>
              <span v-if="booking.feedback">{{ booking.feedback }}</span>
              <span v-else class="text-muted">No feedback</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty State Message -->
    <div v-if="!loading && completedBookings.length === 0" class="text-center my-4">
      <p class="text-muted fw-semibold">No completed services found.</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  setup() {
    const completedBookings = ref([]);
    const loading = ref(true);
    const error = ref(null);

    const fetchCompletedBookings = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) return;

        const response = await axios.get("http://127.0.0.1:5000/completedbookings", {
          headers: { Authorization: `Bearer ${token}` },
        });

        completedBookings.value = response.data;
        console.log("Completed Bookings:", completedBookings.value);
      } catch (err) {
        error.value = "Failed to fetch completed services.";
      } finally {
        loading.value = false;
      }
    };

    const formatDate = (dateString) => {
      if (!dateString) return "Not Available";
      return new Date(dateString).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
    };

    onMounted(fetchCompletedBookings);

    return {
      completedBookings,
      loading,
      error,
      formatDate,
    };
  },
};
</script>

<style scoped>
.container {
  max-width: 1400px;
  margin: auto;
}

/* Improved table spacing */
.table th,
.table td {
  vertical-align: middle;
  text-align: center;
}

/* Loader spinner */
.spinner-border {
  width: 3rem;
  height: 3rem;
}

/* Status badges */
.badge {
  font-size: 0.9rem;
  padding: 6px 12px;
}

/* Table hover effect */
.table-hover tbody tr:hover {
  background-color: #f8f9fa;
}
</style>


