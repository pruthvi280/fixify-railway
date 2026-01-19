<template>
  <div class="container">
    <h2 class="text-xl font-semibold mb-4 text-center">Professional Performance</h2>

    <!-- Stats Card for Average Rating (Moved Above) -->
    <div class="stats-card mb-4">
      <div class="stat">
        <span class="label">My Rating:</span>
        <span class="value">{{ averageRating || "N/A" }}</span>
      </div>
    </div>

    <div class="chart-container">
      <Bar v-if="chartData" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted } from "vue";
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";
import axios from "axios";

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

export default defineComponent({
  components: { Bar },
  setup() {
    const chartData = ref(null);
    const averageRating = ref(null);
    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
      },
      scales: {
        y: { beginAtZero: true,
            ticks: {
            stepSize: 1,
          },
        },
      },
    };

    const fetchProfessionalStats = async () => {
      try {
        const response = await axios.get("http://localhost:5000/professionalstats", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });

        const data = response.data;
        averageRating.value = data.average_rating;

        chartData.value = {
          labels: ["New Requests", "Scheduled", "Rejected", "Completed"],
          datasets: [
            {
              label: "Services",
              data: [
                data.new_service_request,
                data.scheduled_services,
                data.rejected_bookings,
                data.completed_services,
              ],
              backgroundColor: ["#36A2EB", "#FFC107", "#FF6384", "#4CAF50"],
            },
          ],
        };
      } catch (error) {
        console.error("Error fetching professional stats:", error);
      }
    };

    onMounted(fetchProfessionalStats);

    return { chartData, chartOptions, averageRating };
  },
});
</script>

<style scoped>
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 15px;
}

.chart-container {
  width: 100%;
  height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.stats-card {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 18px;
}

.stat .label {
  font-weight: 500;
  color: #333;
}

.stat .value {
  font-weight: 700;
  color: #4CAF50;
}
</style>












