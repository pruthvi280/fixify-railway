<template>
  <div class="container mt-4">
    <h2 class="text-center text-primary mb-4 fw-bold">My Bookings</h2>

    <!-- Loader -->
    <div v-if="loading" class="text-center my-4">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="alert alert-danger text-center">
      {{ error }}
    </div>

    <!-- Booking Table -->
    <div class="table-responsive" v-if="bookings.length > 0">
      <table class="table table-hover align-middle shadow-sm">
        <thead class="table-dark text-white">
          <tr>
            <th scope="col" class="text-center">Sl No</th>
            <th scope="col">Service Name</th>
            <th scope="col">Assigned Professional</th>
            <th scope="col">Booking Date</th>
            <th scope="col">Service Date</th>
            <th scope="col">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(booking, index) in bookings" :key="booking.id">
            <td class="text-center fw-bold">{{ index + 1 }}</td>
            <td>{{ booking.service_name }}</td>
            <td>
              <span v-if="booking.professional_name !== 'Not Assigned'" class="text-success fw-semibold">
                {{ booking.professional_name }}
              </span>
              <span v-else class="text-danger">Not Assigned</span>
            </td>
            <td>{{ formatDate(booking.date) }}</td>
            <td>
              <span v-if="booking.service_date !== 'Not Scheduled'">{{ formatDate(booking.service_date) }}</span>
              <span v-else class="text-danger">Not Scheduled</span>
            </td>
            <td>
              <span class="badge rounded-pill" :class="statusClass(booking.status)">
                {{ booking.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty State Message -->
    <div v-if="!loading && bookings.length === 0" class="text-center my-4">
      <p class="text-muted fw-semibold">No bookings found.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const bookings = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchBookings = async () => {
  try {
    const token = localStorage.getItem("token");
    const response = await axios.get("http://127.0.0.1:5000/mybookings", {
      headers: { Authorization: `Bearer ${token}` },
    });
    bookings.value = response.data;
    console.log("Bookings Data:", JSON.parse(JSON.stringify(bookings.value)));
  } catch (err) {
    error.value = "Failed to fetch bookings.";
  } finally {
    loading.value = false;
  }
};

const statusClass = (status) => {
  switch (status) {
    case "Pending":
      return "bg-warning text-dark";
    case "Confirmed":
      return "bg-success text-white";
    case "Cancelled":
      return "bg-danger text-white";
    default:
      return "bg-secondary text-white";
  }
};

const formatDate = (dateString) => {
  if (!dateString) return "Not Available";
  const date = new Date(dateString);
  return date.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
};

onMounted(fetchBookings);
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
}

/* Styling for the edit button */
.btn-outline-warning {
  border: none;
  transition: 0.3s ease-in-out;
}
.btn-outline-warning:hover {
  background-color: #ffc107;
  color: #000;
}

/* Status badges */
.badge {
  font-size: 0.9rem;
  padding: 6px 12px;
}
</style>
