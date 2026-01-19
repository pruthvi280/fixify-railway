<template>
  <div class="dashboard">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1>Professional Panel</h1>
      </div>
      <nav class="menu">
        <router-link to="/professionalbookings" class="menu-item">
          New Service Requests
        </router-link>
        <router-link to="/professionalscheduledservices" class="menu-item">
          Scheduled Services
        </router-link>
        <router-link to="/professionalservicehistory" class="menu-item">
          Service History
        </router-link>
        <router-link to="/professionalanalytics" class="menu-item">
          My Ratings/Reviews
        </router-link>
        <router-link to="/myprofile" class="menu-item">
          Profile
        </router-link>
        <router-link to="/contactus" class="menu-item">
          Support
        </router-link>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <header class="header">
        <h1>Welcome, {{ stats.name }}</h1>
      </header>

      <section class="content">
        <div class="stats">
          <div class="stat-card" v-for="(value, key) in statLabels" :key="key">
            <h3>{{ value }}</h3>
            <p>{{ stats[key] }}</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  setup() {
    const stats = ref({
      new_service_request: 0,
      scheduled_services: 0,
      rejected_bookings: 0,
      completed_services: 0,
      name: "Professional",
    });

    const statLabels = {
      new_service_request: "New Service Requests",
      scheduled_services: "Scheduled Services",
      rejected_bookings: "Rejected Requests",
      completed_services: "Completed Services",
    };

    const fetchStats = async () => {
      try {
        const token = localStorage.getItem("token");
        if (!token) return;

        const { data } = await axios.get("http://127.0.0.1:5000/professionalstats", {
          headers: { Authorization: `Bearer ${token}` },
        });

        stats.value = data;
      } catch (error) {
        console.error("Error fetching professional stats:", error);
      }
    };

    onMounted(fetchStats);

    return { stats, statLabels };
  },
};
</script>


<style scoped>

.dashboard {
  display: flex;
  height: 100vh;
  font-family: Arial, sans-serif;
  background-color: #f7f7f7;
}

/* Sidebar */
.sidebar {
  width: 250px;
  background-color: #333;
  color: white;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 1.5rem;
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
  background-color: #444;
  color: #fff;
}

.menu {
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

.menu-item {
  padding: 1rem;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  margin-bottom: 0.5rem;
  transition: background 0.3s;
}

.menu-item:hover {
  background-color: #555;
}

.menu-item.active {
  background-color: #ff6f61;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 2rem;
}

.header {
  background: #dbaadf;
  color: white;
  padding: 1rem 2rem;
  border-radius: 8px;
  margin-bottom: 2rem;
}

.header h1 {
  margin: 0;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
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

/* Recent Activity */
.recent-activity {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.recent-activity h2 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1rem;
}

.recent-activity ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.recent-activity li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #ddd;
  font-size: 1rem;
  color: #555;
}

.recent-activity li:last-child {
  border-bottom: none;
}
</style>