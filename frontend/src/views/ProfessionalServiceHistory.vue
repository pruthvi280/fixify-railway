<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">Completed Services</h2>

    <div v-if="loading" class="text-center text-secondary">Loading...</div>
    <div v-else-if="completedServices.length === 0" class="text-center text-secondary">
      No completed services found.
    </div>

    <div v-else>
      <div class="table-responsive">
        <table class="table table-bordered table-striped table-hover">
          <thead class="table-dark">
            <tr>
              <th>S.No.</th>
              <th>Service Name</th>
              <th>Customer Name</th>
              <th>Phone Number</th>
              <th>Address</th>
              <th>Service Date</th>
              <th>Status</th>
              <th>Ratings</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(service, index) in completedServices" :key="index">
              <td class="text-center">{{ index + 1 }}</td>
              <td class="text-center">{{ service.service_name }}</td>
              <td class="text-center">{{ service.customer_name }}</td>
              <td class="text-center">{{ service.customer_phone }}</td>
              <td class="text-center">{{ service.customer_address }}</td>
              <td class="text-center">{{ service.service_date }}</td>
              <td class="text-center text-success fw-bold">{{ service.status }}</td>
              <td class="text-center fw-bold">
                <span v-if="service.rating !== 'Not Rated'" class="text-warning">
                  ⭐ {{ service.rating }}/5
                </span>
                <span v-else class="text-muted">Not Rated</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  setup() {
    const completedServices = ref([]);
    const loading = ref(true);

    const fetchCompletedServices = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("/servicehistory", {
          headers: { Authorization: `Bearer ${token}` },
        });
        console.log("API Response:", response.data);
        completedServices.value = response.data.completed_services;
      } catch (error) {
        console.error("Error fetching completed services:", error);
      } finally {
        loading.value = false;
      }
    };

    onMounted(fetchCompletedServices);

    return { completedServices, loading };
  },
};
</script>

<style scoped>
.container {
  max-width: 1100px;
}
</style>
