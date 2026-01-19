<template>
  <div class="signup-page">
    <section class="signup-form">
      <form @submit.prevent="handleSubmit">
        <!-- Name -->
        <div class="form-group">
          <label for="name">Full Name</label>
          <input type="text" id="name" v-model="form.name" placeholder="Enter Your Name" required />
        </div>

        <!-- Email -->
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="form.email" placeholder="Enter Your Email" required />
        </div>

        <!-- Password -->
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="form.password" placeholder="Enter Password" required />
        </div>

        <!-- Confirm Password -->
        <div class="form-group">
          <label for="cpassword">Confirm Password</label>
          <input type="password" id="cpassword" v-model="form.confirmPassword" placeholder="Re-Enter Your Password" required />
        </div>

        <!-- Phone Number -->
        <div class="form-group">
          <label for="phone">Contact Number</label>
          <input type="tel" id="phone" v-model="form.phone" placeholder="Enter Your Contact Number" required />
        </div>

        <!-- Address -->
        <div class="form-group">
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
import { ref } from "vue";
import { useRouter } from "vue-router";
import axios from "axios";
import store from "../store";

export default {
  name: "CustomerSignup",
  setup() {
    const router = useRouter();

    const form = ref({
      name: "",
      email: "",
      phone: "",
      password: "",
      confirmPassword: "",
      address: "",
    });

    const handleSubmit = async () => {
      if (form.value.password !== form.value.confirmPassword) {
        alert("Passwords do not match!");
        return;
      }

      try {
        let formData = new FormData();
        formData.append("name", form.value.name);
        formData.append("email", form.value.email);
        formData.append("phone", form.value.phone);
        formData.append("password", form.value.password);
        formData.append("confirmPassword", form.value.confirmPassword);
        formData.append("address", form.value.address);
        formData.append("role", "customer");

        const response = await axios.post("http://127.0.0.1:5000/signup", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        console.log("Signup Response:", response.data);

        const user = {
          id: response.data.user_id,
          username: response.data.username,
          email: response.data.email,
          role: response.data.role || "unknown",
          token: response.data.token,
        };

        // Save token and user details in Vuex store
        store.commit("setToken", user.token);
        store.commit("setUser", user);

        alert("Signup successful! Redirecting...");
        router.push("/customerdashboard");
      } catch (error) {
        console.error("Signup Error:", error);
        alert("Signup failed. Please try again.");
      }
    };

    return { form, handleSubmit };
  },
};
</script>


<style scoped>
/* Add padding to the main content to prevent overlap with navbar/footer */
.signup-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh; /* Make sure the content takes full screen height */
  padding-top: 80px; /* To prevent overlap with navbar */
  padding-bottom: 60px; /* To prevent overlap with footer */
  background-color: #f7f7f7;
}

.signup-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}

.signup-form h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
  text-align: center;
}

.signup-form p {
  text-align: center;
  margin-bottom: 2rem;
  color: #555;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.form-group input:focus {
  border-color: #ff6f61;
  outline: none;
  box-shadow: 0 0 4px rgba(255, 111, 97, 0.5);
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
}

.btn:hover {
  background-color: #e55b51;
}
</style>


