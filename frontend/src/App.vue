<template>
  <div id="app" class="app-container">
    <!-- Navigation Bar -->
    <header>
      <nav class="navbar">
        <!-- App Name on Left -->
        <div class="app-name" @click="navigateToDashboard">
          <img src="@/assets/fixify.png" alt="Fixify Logo" class="fixify-logo" />
          FIXIFY
        </div>

        <!-- Navigation Links on Right -->
        <div class="nav-links">
          <router-link to="/" class="home">Home</router-link>

          <!-- Hide all other icons if on Approval, Blocked, or Login page -->
          <template v-if="!isRestrictedPage">
            <template v-if="!IsUserLoggedIn">
              <router-link to="#services">Services</router-link>
              <!-- <router-link to="#about">About</router-link> -->
              <router-link to="#contact">Contact</router-link>
            </template>

            <!-- Search Button -->
            <div v-if="IsUserLoggedIn && reactiveRole !== 'professional'" class="search-container" @click="goToSearch">
              <button class="search-button">
                <img src="@/assets/search.png" alt="Search" class="search-icon" />
              </button>
            </div>

            <!-- Show Login if user is NOT logged in -->
            <router-link v-if="!IsUserLoggedIn" to="/login" class="login-container">
              <img src="@/assets/Login.png" alt="Login" class="login-icon">
              Login/Sign-Up
            </router-link>

            <!-- Show Logout if user IS logged in -->
            <button v-if="IsUserLoggedIn" @click="UserLogout" class="logout-container">
              <img src="@/assets/log-out.png" alt="Logout" class="logout-icon">
            </button>
          </template>
        </div>
      </nav>
    </header>

    <!-- Main Content -->
    <main>
      <RouterView />
    </main>

    <!-- Footer -->
    <!-- <footer>
      <p>&copy; 2025 Fixify. All rights reserved.</p>
    </footer> -->
  </div>
</template>

<script setup>
import { RouterView, RouterLink, useRoute, useRouter } from "vue-router";
import { watch, onMounted, computed, ref } from "vue";
import store from "./store";
import { jwtDecode } from "jwt-decode";

const router = useRouter();
const route = useRoute();
const reactiveRole = ref(null);

//  Check if the current route is Approval, Blocked, or Login page
const isRestrictedPage = computed(() => 
  route.path === "/approvalpending" || route.path === "/blocked" || route.path === "/login" || route.path === "/signupoption" || route.path === "/customersignup" || route.path === "/professionalsignup"
);

// Logout function
async function UserLogout() {
  await store.dispatch("logout");
  router.push("/"); // Redirect to home after logout
}

// Check if user is logged in
const IsUserLoggedIn = computed(() => !!store.state.token);
const UserRole = computed(() => {
  if (!store.state.token) return null;
  try {
    const decoded = jwtDecode(store.state.token);
    return decoded?.sub?.role || null;
  } catch (error) {
    console.error("Error decoding token:", error);
    return null;
  }
});

// Navigate to Search.vue when clicking the search button
const goToSearch = () => {
  router.push({ name: "Search", query: { role: UserRole.value } });
};

// Navigate to the correct dashboard when clicking the logo
const navigateToDashboard = () => {
  if (!IsUserLoggedIn.value) {
    router.push("/");
  } else if (UserRole.value === "admin") {
    router.push("/admindashboard");
  } else if (UserRole.value === "customer") {
    router.push("/customerdashboard");
  } else if (UserRole.value === "professional") {
    router.push("/professionaldashboard");
  }
};

watch(UserRole, (newRole) => {
  reactiveRole.value = newRole;
}, { immediate: true });

onMounted(() => {
  console.log("UserRole on mount:", UserRole.value);
});
</script>

<style scoped>

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Main content should take up available space */
main {
  flex-grow: 1;
  padding: 20px;
}

/* Navbar Styling */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #393d68;
  padding: 15px 20px;
  color: rgb(218, 158, 192);
}


.app-name {
  display: flex;
  align-items: center;
  font-size: 2em;
  font-weight: bold;
  color: white;
  letter-spacing: 2px;
  text-transform: uppercase;
  gap: 10px; /* Space between logo and text */
}

.fixify-logo {
  width: 50px; 
  height: auto;
}


/* Navigation Links */
.nav-links {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-links a {
  color: rgb(242, 237, 237);
  text-decoration: none;
  font-size: 1.1em;
  padding: 8px 12px;
}

.nav-links a:hover {
  text-decoration: underline;
  color: #EDCD1F;
}

/* Search Button */
.search-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease-in-out;
}
/* Click Animation */
.search-button.active {
  transform: scale(0.85);
}

/* Hover Effect */
.search-button:hover {
  transform: scale(1.1); 
}

.search-icon {
  width: 30px; /* Adjust size as needed */
  height: 30px;
}


.login-container {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgb(242, 237, 237);
  text-decoration: none;
  font-size: 1.1em;
  padding: 8px 12px;
}

.login-container:hover {
  color: #EDCD1F;
  text-decoration: underline;
}

.login-icon {
  width: 25px;
  height: 25px;
}

.logout-container {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  color: rgb(242, 237, 237);
  font-size: 1.1em;
  cursor: pointer;
  padding: 8px 12px;
}

.logout-container:hover {
  color: #EDCD1F;
  text-decoration: underline;
}


.logout-icon {
  width: 25px; 
  height: 25px;
}

footer {
  background-color: #908c8c;
  color: white;
  text-align: center;
  padding: 10px;
  width: 100%;
}
</style>




