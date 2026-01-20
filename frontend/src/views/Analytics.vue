<template>
  <div class="analytics">
    <h2>Admin Analytics</h2>

    <div class="chart-container">
      <!-- Customers vs Professionals -->
      <div class="chart-box">
        <h3>Customers vs Professionals</h3>
        <canvas ref="userChart"></canvas>
      </div>

      <!-- Service Category Distribution -->
      <div class="chart-box">
        <h3>Service Category Distribution</h3>
        <canvas ref="serviceChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";
import Chart from "chart.js/auto";

export default {
  setup() {
    // Refs for storing API data
    const userStats = ref({});
    const serviceStats = ref({});

    // Refs for canvas elements
    const userChart = ref(null);
    const serviceChart = ref(null);

    // Fetch API Data
    const fetchData = async () => {
      try {
        const userResponse = await axios.get("/admin/user-stats");
        userStats.value = userResponse.data;

        const serviceResponse = await axios.get("/admin/service-stats");
        serviceStats.value = serviceResponse.data;

        renderCharts(); // Render charts after fetching data
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    // Render Charts
    const renderCharts = () => {
      // ✅ Customers vs Professionals Bar Graph
      if (userChart.value) {
        new Chart(userChart.value, {
          type: "bar",
          data: {
            labels: ["Customers", "Professionals"],
            datasets: [
              {
                label: "Count",
                data: [userStats.value.customers, userStats.value.professionals],
                backgroundColor: ["#3498db", "#e74c3c"],
              },
            ],
          },
          options: {
            scales: {
              y: {
                ticks: {
                  stepSize: 1, // ✅ Force integer values on y-axis
                  callback: function (value) {
                    if (Number.isInteger(value)) {
                      return value;
                    }
                  },
                },
              },
            },
          },
        });
      }

      // ✅ Service Category Pie Chart
      if (serviceChart.value) {
        new Chart(serviceChart.value, {
          type: "pie",
          data: {
            labels: serviceStats.value.labels,
            datasets: [
              {
                data: serviceStats.value.counts,
                backgroundColor: ["#f39c12", "#9b59b6", "#1abc9c", "#2ecc71", "#e74c3c"],
              },
            ],
          },
        });
      }
    };

    onMounted(fetchData); // Fetch data when component mounts

    return {
      userStats,
      serviceStats,
      userChart,
      serviceChart,
    };
  },
};
</script>

<style scoped>
.analytics {
  padding: 20px;
}

.chart-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: space-between;
}

.chart-box {
  width: 45%;
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

canvas {
  width: 100% !important;
  height: 300px !important;
}
</style>
