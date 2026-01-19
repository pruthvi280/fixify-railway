
<template>
  <div class="dashboard">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <h2>Admin Panel</h2>
      </div>
      <nav class="menu">
        <router-link to="/managecustomers" class="menu-item">
          Manage Customers
        </router-link>
        <router-link to="/manageprofessionals" class="menu-item">
          Manage Professionals
        </router-link>
        <router-link to="/manageservices" class="menu-item">
          Manage Services
        </router-link>
        <router-link to="/adminbookingoverview" class="menu-item">
          All Bookings Overview
        </router-link>
        <router-link to="/analytics" class="menu-item">
          Analytics
        </router-link>
        <!-- CSV Download Button -->
        <a href="javascript:void(0)" @click="generateCSV" class="menu-item">
          {{ generating ? "Generating CSV..." : "Download Service Report" }}
        </a>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <header class="header">
        <h1>Admin Dashboard</h1>
      </header>

      <section class="content">
        <div class="stats">
          <div class="stat-card">
            <h3>Total Customers</h3>
            <p>{{ totalCustomers }}</p>
          </div>
          <div class="stat-card">
            <h3>Total Services</h3>
            <p>{{ totalServices }}</p>
          </div>
          <div class="stat-card">
            <h3>New Bookings</h3>
            <p>{{ newBookings }}</p>
          </div>
          <div class="stat-card">
            <h3>Popular Services</h3>
            <ul v-if="popularServices.length">
              <li v-for="service in popularServices" :key="service.id">
                {{ service.name }}
              </li>
            </ul>
            <p v-else>No Data</p>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import { mapState } from "vuex";
import axios from "axios";

export default {
  data() {
    return {
      totalCustomers: 0,
      totalServices: 0,
      newBookings: 0,
      popularServices: [],
      generating: false,
      taskId: null,
      fileName: null,
    };
  },
  created() {
    this.fetchDashboardStats();
    this.fetchPopularService();
  },
  methods: {
    // ✅ Fetch Dashboard Stats
    async fetchDashboardStats() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/adminstats");
        this.totalCustomers = response.data.total_customers;
        this.totalServices = response.data.total_services;
        this.newBookings = response.data.new_bookings;
      } catch (error) {
        console.error("Error fetching dashboard stats:", error);
      }
    },

    // ✅ Fetch Popular Services
    async fetchPopularService() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/most_popular_service");
        this.popularServices = response.data.most_popular_services || [];
      } catch (error) {
        console.error("Error fetching popular service:", error);
        this.popularServices = [];
      }
    },

    // ✅ Trigger CSV Generation
    async generateCSV() {
      this.generating = true;
      this.taskId = null;
      this.fileName = null;

      try {
        const response = await axios.get("http://127.0.0.1:5000/create-csv");
        this.taskId = response.data.task_id;
        this.checkCSVStatus();
      } catch (error) {
        console.error("Error generating CSV:", error);
        this.generating = false;
        alert("Failed to start CSV generation. Try again.");
      }
    },

    // ✅ Check Task Status (Polling)
    async checkCSVStatus() {
      const interval = setInterval(async () => {
        try {
          const response = await axios.get(`http://127.0.0.1:5000/get-csv-data/${this.taskId}`);

          if (response.status === 200) {
            clearInterval(interval);
            const contentDisposition = response.headers['content-disposition'];
            if (contentDisposition) {
              this.fileName = contentDisposition.split('filename=')[1].replace(/"/g, '');
            }
            this.downloadCSV(response.request.responseURL);
          } else if (response.status === 202) {
            console.log("CSV generation in progress...");
          } else {
            clearInterval(interval);
            console.error("Error fetching CSV:", response.data);
            this.generating = false;
            alert("Error fetching CSV. Try again.");
          }
        } catch (error) {
          console.error("Error checking CSV status:", error);
          clearInterval(interval);
          this.generating = false;
          alert("Failed to fetch CSV status.");
        }
      }, 3000);
    },

    // ✅ Download CSV Once Ready
    downloadCSV(fileURL) {
      const link = document.createElement("a");
      link.href = fileURL;
      link.setAttribute("download", this.fileName || "Service_Report.csv"); 
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      this.generating = false;
      this.taskId = null;
      this.fileName = null;
    },
  },
  computed: {
    ...mapState(["user"]),
  },
  mounted() {
    const role = this.$store.getters.userRole;
    if (role !== "admin") {
      this.$router.push("/");
    }
  },
};
</script>




<style scoped>
/* General Styles */
.dashboard {
  display: flex;
  height: 100vh;
  font-family: Arial, sans-serif;
  background-color: #f7f7f7;
}

/* Sidebar */
.sidebar {
  width: 250px;
  background-color: #1e2a3a;
  color: white;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 1.5rem;
  text-align: center;
  font-size: 1.5rem;
  font-weight: bold;
  background-color: #16202d;
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
  background-color: #2a3b4d;
}

.menu-item.active {
  background-color: #007bff;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 2rem;
}

.header {
  background: #007bff;
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
  color: #007bff;
}
</style>


