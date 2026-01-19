<template>
  <div class="container mt-4">
    <h2 class="text-center mb-4 text-primary">Ongoing Services</h2>

    <div v-if="loading" class="text-center text-muted">
      <p>Loading ongoing services...</p>
    </div>

    <div v-else-if="ongoingBookings.length === 0" class="text-center text-muted">
      <p>No ongoing services found.</p>
    </div>

    <div v-else class="grid-container">
      <div v-for="booking in ongoingBookings" :key="booking.id" class="service-card shadow">
        <div class="card-content">
          <h5 class="card-title text-dark">{{ booking.service_name }}</h5>

          <div class="details">
            <p><strong>Professional:</strong> {{ booking.professional_name || "Not Assigned" }}</p>
            <p><strong>Contact:</strong> {{ booking.professional_contact || "N/A" }}</p>
            <p><strong>Booking Date:</strong> {{ formatDate(booking.date) }}</p>
            <p><strong>Scheduled Date:</strong> {{ formatDate(booking.scheduledDate) }}</p>
            <p><strong>Status:</strong> 
              <span class="badge" :class="{
                'bg-warning text-dark': booking.status === 'Pending',
                'bg-success': booking.status === 'Accepted',
                'bg-danger': booking.status === 'Cancelled'
              }">{{ booking.status }}</span>
            </p>
            <p><strong>Rating:</strong> 
              <span v-if="booking.professional_rating > 0">
                ⭐ {{ booking.professional_rating }} / 5
              </span>
              <span v-else class="text-muted">No ratings yet</span>
            </p>
          </div>

          <div class="actions d-flex gap-2">
            <template v-if="booking.status === 'Pending'">
              <div class="position-relative">
                <button class="btn btn-outline-primary btn-sm" @click="toggleDatePicker(booking.id)">
                  Reschedule
                </button>
                <input 
                  v-if="showDatePicker === booking.id" 
                  type="date" v-model="newScheduledDate" 
                  class="form-control small-datepicker" 
                  @change="updateScheduledDate(booking.id)" 
                />
              </div>
              <button class="btn btn-outline-danger btn-sm" @click="cancelBooking(booking.id)">
                Cancel
              </button>
            </template>
            <template v-else-if="booking.status === 'Accepted'">
              <button class="btn btn-outline-success btn-sm" @click="navigateToPayment(booking)">
                Pay Now
              </button>
              <button 
                v-if="!booking.professional_name || booking.professional_name === 'Not Assigned'" 
                class="btn btn-outline-danger btn-sm" 
                @click="cancelBooking(booking.id)">
                Cancel
              </button>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

export default {
  setup() {
    const ongoingBookings = ref([]);
    const loading = ref(true);
    const newScheduledDate = ref("");
    const showDatePicker = ref(null);
    const router = useRouter();

    const fetchOngoingServices = async () => {
      loading.value = true;
      try {
        const token = localStorage.getItem("token");
        if (!token) return;

        const response = await axios.get("http://127.0.0.1:5000/ongoingservices", {
          headers: { Authorization: `Bearer ${token}` }
        });

        ongoingBookings.value = response.data;
      } catch (error) {
        console.error("Error fetching ongoing services:", error);
      } finally {
        loading.value = false;
      }
    };

    const toggleDatePicker = (bookingId) => {
      showDatePicker.value = showDatePicker.value === bookingId ? null : bookingId;
    };

    const updateScheduledDate = async (bookingId) => {
      if (!newScheduledDate.value) return;
      try {
        const token = localStorage.getItem("token");
        if (!token) return;

        await axios.put(`http://127.0.0.1:5000/bookings/${bookingId}/update-date`,
          { scheduled_date: newScheduledDate.value },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        alert("Scheduled date updated successfully!");
        showDatePicker.value = null;
        await fetchOngoingServices();
      } catch (error) {
        console.error("Error updating scheduled date:", error);
        alert("Failed to update date. Please try again.");
      }
    };

    const cancelBooking = async (bookingId) => {
      if (!confirm("Are you sure you want to cancel this booking?")) return;
      try {
        const token = localStorage.getItem("token");
        if (!token) return;

        await axios.post(`http://127.0.0.1:5000/cancelbooking/${bookingId}`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        });

        alert("Booking cancelled successfully!");
        fetchOngoingServices();
      } catch (error) {
        console.error("Error cancelling booking:", error);
        alert("Failed to cancel booking. Please try again.");
      }
    };

    const navigateToPayment = (booking) => {
      if (!booking.amount) {
        alert("Amount not available! Defaulting to 0.");
        booking.amount = 0;
      }
      router.push({
        name: "Payment",
        query: {
          bookingId: booking.id,
          serviceName: booking.service_name,
          amount: booking.amount || 0,
          professionalName: booking.professional_name || "Unknown",
        },
      });
    };

    const formatDate = (dateString) => {
      if (!dateString) return "N/A";
      return new Date(dateString).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
    };

    onMounted(fetchOngoingServices);

    return {
      ongoingBookings,
      loading,
      newScheduledDate,
      showDatePicker,
      fetchOngoingServices,
      toggleDatePicker,
      updateScheduledDate,
      cancelBooking,
      navigateToPayment,
      formatDate
    };
  }
};
</script>

<style scoped>
.container {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 10px;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 15px;
}

.service-card {
  background: white;
  border-radius: 10px;
  padding: 15px;
  transition: transform 0.2s;
  border-left: 5px solid #007bff;
}

.service-card:hover {
  transform: translateY(-5px);
}

.badge {
  padding: 6px 10px;
  font-size: 0.9rem;
  border-radius: 5px;
}

.actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn {
  border-radius: 20px;
  font-size: 0.85rem;
  padding: 8px 12px;
  transition: background 0.2s;
}

.btn-outline-primary:hover {
  background: #007bff;
  color: white;
}

.btn-outline-danger:hover {
  background: #dc3545;
  color: white;
}

.small-datepicker {
  margin-top: 5px;
  font-size: 0.85rem;
  padding: 5px;
}
</style>