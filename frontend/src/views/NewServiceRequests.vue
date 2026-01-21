<template>
  <div class="container">
    <main class="main-content">
      <header class="my-4 text-center">
        <h1 class="welcome-text">"Hey {{ customerName }}, Let's Get Your Service Booked!"</h1>
      </header>

      <section class="content">
        <div v-if="!selectedCategory" class="row">
          <div v-for="category in categories" :key="category.id" class="col-md-4 mb-4">
            <div class="card category-card h-100 shadow-sm">
              <div class="card-body text-center">
                <h5 class="card-title fw-bold">{{ category.name }}</h5>
                <p class="card-text text-muted">{{ category.description }}</p>
                <button @click="selectCategory(category)" class="btn btn-primary w-100">View Services</button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="selectedCategory" class="row">
          <div class="col-12 mb-4 d-flex justify-content-between align-items-center">
            <h3 class="category-heading text-primary">Services in "{{ selectedCategory.name }}"</h3>
            <button @click="selectedCategory = null" class="btn btn-outline-secondary">Back to Categories</button>
          </div>

          <div v-for="service in services" :key="service.id" class="col-md-4 mb-4">
            <div class="card service-card h-100 shadow">
              <div class="card-body d-flex flex-column">
                <h5 class="card-title fw-bold text-dark">{{ service.name }}</h5>
                <p class="card-text text-muted small">{{ service.description }}</p>
                <h4 class="text-success mb-3">₹{{ service.base_price }}</h4>

                <div class="mt-auto">
                  <label :for="'date-' + service.id" class="form-label fw-semibold">Select Date:</label>
                  
                  <input 
                    :id="'date-' + service.id"
                    type="date" 
                    class="form-control mb-3"
                    v-model="service.selected_date"
                    :min="todayDate"
                  />

                  <button @click="requestService(service)" class="btn btn-success w-100 fw-bold">
                    Request Service
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import store from "@/store";
import { useRouter } from "vue-router";

export default {
  name: "NewServiceRequest",
  setup() {
    const categories = ref([]);
    const selectedCategory = ref(null);
    const services = ref([]); // We use a simple ref array
    const router = useRouter();

    const customerName = computed(() => store.state.user ? store.state.user.username : "Customer");
    const todayDate = computed(() => new Date().toISOString().split("T")[0]);

    const fetchCategories = async () => {
      try {
        const response = await axios.get("/categories");
        categories.value = response.data;
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    };

    const selectCategory = async (category) => {
      selectedCategory.value = category;
      try {
        const response = await axios.get(`/getservices/${category.id}`);
        
        // FIX: Initialize the array. Add a 'selected_date' property to EVERY service object.
        // This ensures every service has its own independent date storage.
        services.value = response.data.map(service => ({
            ...service,
            selected_date: "" 
        }));
        
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    };

    const requestService = async (service) => {
      const token = localStorage.getItem("token");
      if (!token) {
        alert("Please log in first.");
        router.push("/login");
        return;
      }

      if (!service.selected_date) {
        alert("Please select a date first!");
        return;
      }

      try {
        // Send the specific service's date
        const response = await axios.post(
          "/request_service",
          { service_id: service.id, service_date: service.selected_date },
          { headers: { Authorization: `Bearer ${token}` } }
        );
        
        alert("Service requested successfully!");
        service.selected_date = ""; // Reset just this service's date
        
      } catch (error) {
        console.error("Request failed:", error);
        alert(error.response?.data?.message || "There was an issue with your request.");
      }
    };

    onMounted(fetchCategories);

    return {
      categories,
      selectedCategory,
      services,
      customerName,
      todayDate,
      selectCategory,
      requestService
    };
  },
};
</script>




<style scoped>

.container {
  padding: 2rem;
}

.main-content {
  padding: 2rem;
}

.welcome-text {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
}

/* Card Styling */
.category-card, .service-card {
  border-radius: 12px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: linear-gradient(to right, #ffffff, #f8f9fa);
}

.category-card:hover, .service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

/* Card Titles */
.card-title {
  font-size: 1.4rem;
  font-weight: 600;
  color: #343a40;
}

.service-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1d3557;
}

/* Price Text */
.price-text {
  font-size: 1.2rem;
  color: #e63946;
  font-weight: bold;
}

/* Category Header */
.category-heading {
  font-size: 1.8rem;
  font-weight: bold;
  color: #007bff;
  text-align: center;
  margin-bottom: 1.5rem;
}

/* Button Styling */
.btn-primary {
  background: linear-gradient(to right, #007bff, #0056b3);
  border: none;
  padding: 0.6rem 1.2rem;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 8px;
}

.btn-primary:hover {
  background: linear-gradient(to right, #0056b3, #004080);
}

.request-btn {
  background: linear-gradient(to right, #28a745, #218838);
  color: white;
  font-weight: bold;
  border-radius: 8px;
}

.request-btn:hover {
  background: linear-gradient(to right, #218838, #1e7e34);
}

/* Date Picker */
input[type="date"] {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
  margin-bottom: 0.5rem;
}
</style>


