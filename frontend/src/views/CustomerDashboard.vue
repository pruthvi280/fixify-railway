<template>
  <div class="dashboard">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">Customer Panel</div>
      <nav class="menu">
        <router-link to="/newservicerequest" class="menu-item">New Service Requests</router-link>
        <router-link to="/ongoingservice" class="menu-item">Ongoing Services</router-link>
        <router-link to="/completedbookings" class="menu-item">Completed Services</router-link>
        <router-link to="/mybookings" class="menu-item">My Bookings</router-link>
        <router-link to="/myprofile" class="menu-item">My Profile</router-link>
        <router-link to="/contactus" class="menu-item">Contact Us</router-link>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <header class="header">
        <h1>Welcome, {{ stats.name || "Customer" }}!</h1>
      </header>

      <!-- Booking Stats -->
      <section class="content">
        <div class="stats">
          <div class="stat-card">
            <h3>Total Bookings</h3>
            <p>{{ stats.total_bookings }}</p>
          </div>
          <div class="stat-card">
            <h3>Pending Services</h3>
            <p>{{ stats.pending_services }}</p>
          </div>
          <div class="stat-card">
            <h3>Ongoing Services</h3>
            <p>{{ stats.ongoing_services }}</p>
          </div>
          <div class="stat-card">
            <h3>Completed Services</h3>
            <p>{{ stats.completed_services }}</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { computed, ref, onMounted, onBeforeUnmount } from "vue";
import axios from "axios";
import store from "@/store";

export default {
  name: "CustomerDashboard",
  setup() {
    const stats = ref({
      total_bookings: 0,
      pending_services: 0,
      ongoing_services: 0,
      completed_services: 0,
      name:"Customer",

    });

    const loading = ref(true);
    let autoRefresh;

    const fetchUserProfile = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) return;

        const response = await axios.get("/profile", {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (response.data) {
          store.commit("setUser", response.data); // Update store with latest user data
        }
      } catch (error) {
        console.error("Error fetching user profile:", error);
      }
    };

    // Fetch booking stats
    const fetchBookingStats = async () => {
      loading.value = true;
      try {
        const token = localStorage.getItem("token");
        if (!token) return;

        const response = await axios.get("/bookingstats", {
          headers: { Authorization: `Bearer ${token}` },
        });
        stats.value = {
          ...response.data,
          name: store.state.user ? store.state.user.username : "Customer"
        };
      } catch (error) {
        console.error("Error fetching booking stats:", error);
      } finally {
        loading.value = false;
      }
    };

    onMounted(() => {
      fetchUserProfile(); // Load user profile on mount
      fetchBookingStats();
      autoRefresh = setInterval(fetchBookingStats, 30000); // Auto-refresh every 30 sec
    });

    onBeforeUnmount(() => {
      clearInterval(autoRefresh);
    });

    return { stats, loading };
  },
};
</script>


<style scoped>
/* General Styles */
.dashboard {
  display: flex;
  height: 100vh;
  background-color: #f4f5f7;
  font-family: "Poppins", sans-serif;
}

/* Sidebar */
.sidebar {
  width: 260px;
  background: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

.sidebar-header {
  font-size: 1.4rem;
  font-weight: bold;
  text-align: center;
  padding: 1rem 0;
  border-bottom: 2px solid rgba(255, 255, 255, 0.2);
}

.menu {
  display: flex;
  flex-direction: column;
  margin-top: 1rem;
}

.menu-item {
  padding: 12px;
  color: white;
  text-decoration: none;
  font-size: 1rem;
  border-radius: 6px;
  transition: 0.3s;
  margin-bottom: 10px;
}

.menu-item:hover {
  background: #1abc9c;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 2rem;
}

.header {
  background: #3498db;
  color: white;
  padding: 1rem 2rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  text-align: center;
}

/* Stats Section */
.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stat-card h3 {
  font-size: 1.2rem;
  color: #555;
  margin-bottom: 0.5rem;
}

.stat-card p {
  font-size: 1.5rem;
  font-weight: bold;
  color: #ff6f61;
}
</style>