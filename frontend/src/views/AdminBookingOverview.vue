<template>
  <div class="container mt-4">
    <h2 class="text-center text-primary mb-3">All Bookings & Activities</h2>

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
            <th scope="col">Sl No</th>
            <th scope="col">Customer Name</th>
            <th scope="col">Service Name</th>
            <th scope="col">Professional Name</th>
            <th scope="col">Requested Date</th>
            <th scope="col">Status</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(booking, index) in bookings" :key="booking.id">
            <td class="fw-bold">{{ index + 1 }}</td>
            <td>{{ booking.customer_name }}</td>
            <td class="fw-semibold">{{ booking.service_name }}</td>
            <td class="text-success">{{ booking.professional_name }}</td>
            <td>{{ formatDate(booking.booking_date) }}</td>
            <td>
              <span :class="getStatusClass(booking.status)">
                {{ booking.status }}
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- No Data Message -->
    <div v-if="!loading && bookings.length === 0" class="text-center my-4">
      <p class="text-muted fw-semibold">No bookings or activities found.</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      bookings: [],
      loading: true,
      error: null,
    };
  },
  methods: {
    async fetchBookings() {
      try {
        const response = await axios.get("/bookingsoverview")
        this.bookings = response.data.bookings;
      } catch (err) {
        this.error = "Failed to fetch bookings.";
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return "Not Available";
      return new Date(dateString).toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "short",
        year: "numeric",
      });
    },
    getStatusClass(status) {
      return {
        "badge bg-success": status === "Completed",
        "badge bg-warning text-dark": status === "Accepted",
        "badge bg-danger": status === "Cancelled",
      };
    }
  },
  mounted() {
    this.fetchBookings();
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

/* Table hover effect */
.table-hover tbody tr:hover {
  background-color: #f8f9fa;
}

/* Badge styling */
.badge {
  font-size: 0.9rem;
  padding: 6px 12px;
}
</style>
