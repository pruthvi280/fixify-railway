<template>
  <div class="container mt-4">
    <h2 class="text-center text-primary mb-3">Scheduled Services</h2>

    <div v-if="scheduledServices.length === 0" class="text-center alert alert-info">
      <p>No scheduled services found.</p>
    </div>

    <div class="row">
      <div v-for="service in scheduledServices" :key="service.id" class="col-md-4 mb-3">
        <div class="card shadow-sm p-3">
          <h5 class="text-primary">{{ service.customerName }}</h5>
          <p><strong>Address:</strong> {{ service.address }}</p>
          <p><strong>Phone:</strong> {{ service.phone }}</p>
          <p><strong>Scheduled Date:</strong> {{ service.scheduledDate }}</p>
          <p><strong>Service:</strong> {{ service.serviceName }}</p>
          <span class="badge bg-success">Accepted</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted } from "vue";
import { useStore } from "vuex";
import axios from "axios";

export default {
  setup() {
    const store = useStore();
    const scheduledServices = ref([]);

    const professionalId = computed(() => store.state.user?.id || null);

    const fetchScheduledServices = async () => {
      if (!professionalId.value) {
        console.warn("Professional ID is not available.");
        return;
      }
      try {
        console.log(`Fetching scheduled services for Professional ID: ${professionalId.value}`);
        const response = await axios.get("/professional/scheduled_bookings");
        console.log("Scheduled Services Data:", response.data);
        scheduledServices.value = response.data;
      } catch (error) {
        console.error("Error fetching scheduled services:", error);
      }
    };

    watch(professionalId, (newId) => {
      if (newId) {
        fetchScheduledServices();
      }
    });

    onMounted(() => {
      if (professionalId.value) {
        fetchScheduledServices();
      }
    });

    return { scheduledServices };
  },
};
</script>

