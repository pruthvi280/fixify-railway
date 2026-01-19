<template>
  <div class="container mt-4">
    <h2 class="text-center text-primary mb-3">Service Requests</h2>


    <div v-if="serviceRequests.length === 0" class="alert alert-info text-center">
      No service requests available.
    </div>

    <div class="row">
      <div v-for="request in serviceRequests" :key="request.id" class="col-md-4 mb-3">
        <div class="card shadow-sm p-3">
          <h5 class="text-primary">{{ request.customerName }}</h5>
          <p><strong>Address:</strong> {{ request.address }}</p>
          <p><strong>Phone:</strong> {{ request.phone }}</p>
          <p><strong>Scheduled Date:</strong> {{ request.scheduledDate }}</p>
          <p><strong>Service:</strong> {{ request.serviceName }}</p>

          <div class="d-flex justify-content-between mt-3">
            <button class="btn btn-success btn-sm" @click="updateStatus(request.id, 'Accepted')">
              Accept
            </button>
            <button class="btn btn-danger btn-sm" @click="updateStatus(request.id, 'Rejected')">
              Reject
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watchEffect } from "vue";
import axios from "axios";
import { useStore } from "vuex";

export default {
  setup() {
    const store = useStore();
    const serviceRequests = ref([]);

    // Get the professional ID from Vuex store
    const professionalId = computed(() => store.state.user?.id || null);

    // Fetch service requests for the professional
    const fetchServiceRequests = async () => {
      if (!professionalId.value) return;

      try {
        console.log(`Fetching service requests for Professional ID: ${professionalId.value}`);
        const response = await axios.get("http://127.0.0.1:5000/professional/bookings", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }, // Send JWT token
        });
        console.log("Service Requests Data:", response.data);
        serviceRequests.value = response.data;
      } catch (error) {
        console.error("Error fetching service requests:", error);
      }
    };

    // Update booking status
    const updateStatus = async (bookingId, status) => {
      try {
        const response = await axios.put(
          `http://127.0.0.1:5000/professional/bookings/update/${bookingId}`,
          { status },
          {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }, // Send JWT token
          }
        );
        alert(response.data.message);

        // Remove updated booking from list
        serviceRequests.value = serviceRequests.value.filter(
          (request) => request.id !== bookingId
        );
      } catch (error) {
        console.error("Error updating booking status:", error);
        alert("Failed to update status. Please try again.");
      }
    };

    // Automatically fetch service requests when professionalId changes
    watchEffect(fetchServiceRequests);

    return {
      serviceRequests,
      updateStatus,
    };
  },
};
</script>




