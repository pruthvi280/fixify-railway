<template>
  <div class="container">
    <main class="main-content">
      <header class="my-4 text-center">
        <h1 class="welcome-text">"Hey {{ customerName }}, Let's Get Your Service Booked in Minutes!"</h1>
      </header>

      <section class="content">
        <div v-if="!selectedCategory" class="row">
          <div v-for="category in categories" :key="category.id" class="col-md-4 mb-4">
            <div class="card category-card">
              <div class="card-body">
                <h5 class="card-title">{{ category.name }}</h5>
                <p class="card-text">{{ category.description }}</p>
                <button @click="selectCategory(category)" class="btn btn-primary">View Services</button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="selectedCategory" class="row">
          <div class="col-12 mb-3">
            <h3 class="category-heading">Quality Services in "{{ selectedCategory.name }}" – Just for You!</h3>
            <button @click="selectedCategory = null" class="btn btn-secondary">Back to Categories</button>
          </div>
          
          <div v-for="service in selectedCategory.services" :key="service.id" class="col-md-4 mb-4">
            <div class="card service-card">
              <div class="card-body">
                <h5 class="card-title service-title">{{ service.name }}</h5>
                <p class="card-text">{{ service.description }}</p>
                <p class="card-text price-text"><strong>Price: </strong> ₹{{ service.base_price }}</p>

                <label :for="'date-' + service.id">Select Service Date:</label>
                <input 
                  :id="'date-' + service.id" 
                  type="date" 
                  v-model="service.selected_date" 
                  class="form-control mb-2" 
                  :min="todayDate" 
                />

                <button @click="requestService(service)" class="btn btn-success request-btn">Request Service</button>
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
import { useRouter } from "vue-router";
import axios from "axios";
import store from "@/store";

export default {
  name: "NewServiceRequest",
  setup() {
    const categories = ref([]);
    const selectedCategory = ref(null);
    // Removed global selectedDate = ref(""); 
    const router = useRouter();

    const customerName = computed(() => store.state.user ? store.state.user.username : "customer");
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
        
        //  Initialize 'selected_date' property for each service so Vue can track it individually
        selectedCategory.value.services = response.data.map(service => ({
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
        alert("You are not logged in. Please log in first.");
        router.push("/login");
        return;
      }

      //  Check the specific service's date
      if (!service.selected_date) {
        alert("Please select a service date for this service.");
        return;
      }

      try {
        const response = await axios.post(
          "/request_service",
          // Send the specific service's date
          { service_id: service.id, service_date: service.selected_date },
          { headers: { Authorization: `Bearer ${token}` } }
        );

        console.log("Service requested successfully:", response.data);
        alert(`Service '${service.name}' requested successfully for ${service.selected_date}!`);
        
        // Optional: Reset just this service's date after booking
        service.selected_date = ""; 
        
      } catch (error) {
        console.error("Error requesting service:", error.response);

        if (error.response && error.response.status === 401) {
          alert("Session expired. Please log in again.");
          router.push("/login");
        } else {
          alert("There was an issue with your request.");
        }
      }
    };

    onMounted(fetchCategories);

    return {
      categories,
      selectedCategory,
      // selectedDate, // Removed from return
      customerName,
      todayDate,
      selectCategory,
      requestService,
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


