<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">
      {{ userRole === "admin" ? "Search Professionals" : "Search Services" }}
    </h2>

    <!-- Search Filters -->
    <div class="bg-white p-4 shadow-sm rounded-lg d-flex flex-column flex-md-row align-items-center gap-3">
      <select v-model="searchType" class="form-select w-100 w-md-25">
        <option value="">Select Search Type</option>
        <template v-if="userRole === 'admin'">
          <option value="name">Search by Name</option>
          <option value="service">Search by Service</option>
          <option value="status">Search by Status</option>
          <option value="rating">Search by Rating (≤ 2)</option>
        </template>
        <template v-else>
          <option value="service_name">Search by Service</option>
          <option value="location">Search by Location</option>
        </template>
      </select>

      <input v-if="searchType === 'name' && userRole === 'admin'" v-model="searchParams.name" type="text" placeholder="Enter Name" class="form-control w-100 w-md-25" />

      <select v-if="searchType === 'service' || searchType === 'service_name'" v-model="searchParams.service_name" class="form-select w-100 w-md-25">
        <option value="">Select a Service</option>
        <option v-for="service in services" :key="service.id" :value="service.name">{{ service.name }}</option>
      </select>

      <select v-if="searchType === 'status' && userRole === 'admin'" v-model="searchParams.status" class="form-select w-100 w-md-25">
        <option value="">All Status</option>
        <option value="Blocked">Blocked</option>
        <option value="Unblocked">Unblocked</option>
      </select>



      <input v-if="searchType === 'location' && userRole === 'customer'" v-model="searchParams.location" type="text" placeholder="Enter Location" class="form-control w-100 w-md-25" />

      <button @click="search" class="btn btn-primary">Search</button>
    </div>

    <p v-if="results.length === 0" class="text-center text-danger mt-4">No results found.</p>
    <p v-else class="text-center text-success mt-4">✅ Found {{ results.length }} {{ userRole === "admin" ? "professionals" : "services" }}.</p>

    <!-- Admin Results: Professionals -->
    <div v-if="userRole === 'admin' && results.length > 0" class="mt-4">
      <div class="table-responsive">
        <table class="table table-bordered table-striped table-hover">
          <thead class="table-dark">
            <tr>
              <th>S.No.</th>
              <th>Name</th>
              <th>Email</th>
              <th>Service</th>
              <th>Completed Bookings</th>
              <th>Rating</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(professional, index) in results" :key="professional.id">
              <td class="text-center">{{ index + 1 }}</td>
              <td class="text-center">{{ professional.name }}</td>
              <td class="text-center">{{ professional.email }}</td>
              <td class="text-center">{{ professional.service }}</td>
              <td class="text-center text-success fw-bold">{{ professional.completed_bookings }}</td>
              <td class="text-center text-warning fw-bold">{{ professional.rating }}</td>
              <td class="text-center">
                <span :class="professional.status === 'Blocked' ? 'text-danger fw-bold' : 'text-success fw-bold'">
                  {{ professional.status }}
                </span>
              </td>
              <td class="text-center">
                <button @click="toggleBlockStatus(professional)" class="btn" :class="professional.status === 'Blocked' ? 'btn-success' : 'btn-danger'">
                  {{ professional.status === 'Blocked' ? 'Unblock' : 'Block' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Customer Results: Services -->
    <div v-if="userRole === 'customer' && results.length > 0" class="mt-4">
      <div class="table-responsive">
        <table class="table table-bordered table-striped table-hover">
          <thead class="table-dark">
            <tr>
              <th>S.No.</th>
              <th>Service Name</th>
              <th>Description</th>
              <th>Base Price</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(service, index) in results" :key="service.id">
              <td class="text-center">{{ index + 1 }}</td>
              <td class="text-center">{{ service.service_name }}</td>
              <td class="text-center">{{ service.description }}</td>
              <td class="text-center text-success fw-bold">₹{{ service.base_price }}</td>
              <td class="text-center">
                <button class="btn btn-primary" @click="bookService(service)">Book Now</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useRoute, useRouter } from "vue-router";

const userRole = ref("");
const searchType = ref("");
const searchParams = ref({ name: "", service_name: "", status: "", location: "" });
const results = ref([]);
const services = ref([]);
const route = useRoute();
const router = useRouter();

const search = async () => {
  try {
    let url, queryParams = {};
    if (userRole.value === "admin") {
      url = "http://127.0.0.1:5000/searchprofessionals";
      if (searchType.value === "name") queryParams.name = searchParams.value.name;
      if (searchType.value === "service") queryParams.service_name = searchParams.value.service_name;
      if (searchType.value === "status") queryParams.status = searchParams.value.status;
      if (searchType.value === "rating")queryParams.max_rating = "2"; 
    } else {
      url = "http://127.0.0.1:5000/searchservices";
      if (searchType.value === "service_name") queryParams.service_name = searchParams.value.service_name;
      if (searchType.value === "location") queryParams.location = searchParams.value.location;
    }
    const response = await axios.get(url, { params: queryParams });
    results.value = response.data.professionals || response.data.services || [];
  } catch (error) {
    console.error("🚨 Error fetching search results:", error);
    results.value = [];
  }
};

const fetchServices = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:5000/getservices");
    services.value = Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error("🚨 Error fetching services:", error);
  }
};

const toggleBlockStatus = async (professional) => {
  try {
    // Toggle status
    const newStatus = professional.status === "Blocked" ? "Approved" : "Blocked";

    // Send PUT request to update status
    const response = await axios.put(`http://127.0.0.1:5000/professionals/${professional.id}`, {
      status: newStatus
    });

    if (response.status === 200) {
      // Update UI dynamically
      professional.status = newStatus;
    } else {
      alert("Failed to update status. Try again.");
    }
  } catch (error) {
    console.error("🚨 Error updating professional status:", error);
    alert("Error occurred while updating status.");
  }
};
const bookService = (service) => {
  console.log("Booking service:", service);
  

  router.push({
    path: "/newservicerequest",
    query: { service_id: service.id }
  });
};



onMounted(() => {
  userRole.value = route.query.role;
  fetchServices();
});
</script>

<style scoped>
.container {
  max-width: 1100px;
}
</style>
