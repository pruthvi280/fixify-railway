<template>
  <div class="login-page">
    <section class="login-form">
      <form @submit.prevent="handleLogin">
        <h1>Login</h1>

        <!-- Email -->
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" v-model="form.email" placeholder="Enter Your Email" required />
        </div>

        <!-- Password -->
        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="form.password" placeholder="Enter Your Password" required />
        </div>

        <!-- Error Message -->
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

        <!-- Submit Button -->
        <button type="submit" class="btn" :disabled="loading">
          {{ loading ? "Logging in..." : "Login" }}
        </button>

        <!-- Link to Sign Up Page -->
        <p class="signup-link">
          Don't have an account? <router-link to="/signupoption">Sign Up</router-link>
        </p>
      </form>
    </section>
  </div>
</template>

<script setup>
import axios from 'axios';
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import { useStore } from 'vuex';

const form = ref({ email: '', password: '' });
const errorMessage = ref('');
const loading = ref(false);
const router = useRouter();
const store = useStore();

const handleLogin = async () => {
  if (loading.value) return;
  loading.value = true;
  errorMessage.value = '';

  try {
    const response = await axios.post('http://127.0.0.1:5000/login', {
      email: form.value.email,
      password: form.value.password,
    });

    console.log("API Response:", response.data);

    if (response.data.blocked) {
      console.warn("Redirecting to blocked page...");
      router.push('/blocked');
      return;
    }

    if (!response.data.approved) {
      console.warn("Redirecting to Not Approved page...");
      router.push('/approvalpending');
      return;
    }

    const user = {
      id: response.data.user_id,
      username: response.data.username,
      role: response.data.role || 'unknown',
      token: response.data.token,
      approved: response.data.approved ?? false,
      blocked: response.data.blocked ?? false
    };

    store.commit('setToken', user.token);
    store.commit('setUser', user);

    console.log(user.role);

    if (user.role === 'admin') {
      router.push('/admindashboard');
    } else if (user.role === 'customer') {
      router.push('/customerdashboard');
    } else if (user.role === 'professional') {
      router.push(user.approved ? '/professionaldashboard' : '/approvalpending');
    } else {
      errorMessage.value = 'Invalid role detected';
    }
  } catch (error) {
    if (error.response) {
      console.error("Login Error:", error.response.data);
      
      // ✅ Handle 'User does not exist' case
      if (error.response.status === 401) {
        errorMessage.value = 'User does not exist';
      } else if (error.response.status === 403) {
        errorMessage.value = 'Incorrect password';
      } else {
        errorMessage.value = error.response.data.message || 'An error occurred during login.';
      }
    } else {
      errorMessage.value = 'An error occurred during login. Please try again later.';
    }
  } finally {
    loading.value = false;
  }
};

</script>



<style scoped>

/* Add styling for the login page */
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f7f7f7;
}

.login-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 500px;
}

.login-form h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
  text-align: center;
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

.signup-link {
  text-align: center;
  margin-top: 1rem;
}

.signup-link a {
  color: #ff6f61;
  text-decoration: none;
}

.signup-link a:hover {
  text-decoration: underline;
}
</style>