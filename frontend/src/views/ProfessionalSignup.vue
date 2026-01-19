<template>
  <div class="signup-page">
    <section class="signup-form">
      <h2>Service Professional Signup</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-container">
          <div class="form-group">
            <label for="name">Enter Your Name</label>
            <input type="text" id="name" v-model="form.name" placeholder="Enter Your Name" required />
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" id="email" v-model="form.email" placeholder="Enter Your Email" required />
          </div>
          <div class="form-group">
            <label for="phone">Contact Number</label>
            <input type="tel" id="phone" v-model="form.phone" placeholder="Enter Your Contact Number" required />
          </div>

          <div class="form-group">
            <label for="service">Service Type</label>
            <select id="service" v-model="form.service" required>
              <option value="">Select Service</option>
              <option v-for="service in services" :key="service.id" :value="service.name">
                {{ service.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="form.password" placeholder="Enter Password" required />
          </div>
          <div class="form-group">
            <label for="cpassword">Confirm Password</label>
            <input type="password" id="cpassword" v-model="form.confirmPassword" placeholder="Re-enter Password" required />
          </div>
          <div class="form-group">
            <label for="document">Resume</label>
            <input type="file" id="document" @change="handleFileChanges" required />
          </div>
        </div>

        <!-- Address Section Below -->
        <div class="form-group full-width">
          <label for="address">Address</label>
          <input type="text" id="address" v-model="form.address" placeholder="Enter Your Address" required />
        </div>

        <!-- Submit Button -->
        <button type="submit" class="btn">Sign Up</button>
      </form>
    </section>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export default {
  name: "ServiceProfessionalSignup",
  setup() {
    const store = useStore();
    const router = useRouter();

    const form = ref({
      name: "",
      email: "",
      phone: "",
      password: "",
      confirmPassword: "",
      service: "",
      address: "",
      document: null
    });

    const services = ref([]);
    
    const fetchServices = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/services");
        services.value = response.data;
      } catch (error) {
        console.error("Error fetching services:", error);
        alert("Failed to load services. Please try again.");
      }
    };

    const handleFileChanges = (event) => {
      form.value.document = event.target.files[0];
      console.log("File selected:", form.value.document);
    };

    const handleSubmit = async () => {
      if (form.value.confirmPassword !== form.value.password) {
        alert("Passwords do not match!");
        return;
      }

      if (!form.value.service) {
        alert("Please select a service type.");
        return;
      }

      let formData = new FormData();
      formData.append("name", form.value.name);
      formData.append("email", form.value.email);
      formData.append("phone", form.value.phone);
      formData.append("password", form.value.password);
      formData.append("confirmPassword", form.value.confirmPassword);
      formData.append("service", form.value.service);
      formData.append("address", form.value.address);
      formData.append("role", "professional");

      if (form.value.document) {
        formData.append("document", form.value.document);
      }

      try {
        const response = await axios.post("http://127.0.0.1:5000/signup", formData, {
          headers: { "Content-Type": "multipart/form-data" }
        });

        console.log("Signup Success:", response.data);

        const user = {
          id: response.data.user_id,
          username: response.data.username,
          email: response.data.email,
          role: response.data.role || "unknown",
          // token: response.data.token,
        };

        // Save user token and details in Vuex store
        store.commit("setToken", null);
        store.commit("setUser", null);

        alert("Signup successful! Redirecting...");
        router.push("/approvalpending");

      } catch (error) {
        console.error("Signup Error:", error.response);
        alert(error.response?.data?.message || "Signup failed. Please try again.");
      }
    };

    onMounted(fetchServices);

    return {
      form,
      services,
      handleFileChanges,
      handleSubmit
    };
  }
};
</script>

<style scoped>
.signup-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f7f7f7;
  padding: 2rem;
}

.signup-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 700px;
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  font-size: 1.75rem;
  color: #333;
}

.form-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.full-width {
  grid-column: span 2;
}

label {
  font-weight: bold;
  margin-bottom: 0.5rem;
  color: #555;
}

input, select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
  background-color: #fff;
}

input:focus, select:focus {
  border-color: #ff6f61;
  outline: none;
  box-shadow: 0 0 4px rgba(255, 111, 97, 0.5);
}

/* Extra padding for file input to prevent overlap */
input[type="file"] {
  padding: 0.75rem 0.75rem 1.5rem 0.75rem; /* More padding at the bottom to prevent overlap */
  font-size: 1rem;
}

input[type="password"] {
  padding: 0.75rem;
}

.btn {
  width: 100%;
  background-color: #ff6f61;
  color: white;
  padding: 0.75rem;
  border: none;
  border-radius: 5px;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1.5rem;
}

.btn:hover {
  background-color: #e55b51;
}

@media (max-width: 768px) {
  .form-container {
    grid-template-columns: 1fr;
  }
  .signup-form {
    width: 100%;
    padding: 1.5rem;
  }
}
</style>

