<template>
  <div class="container mt-4">
    <h2 class="text-center text-primary mb-3 fw-bold">Manage Professionals</h2>

    <div class="table-responsive">
      <table class="table table-hover align-middle shadow-sm">
        <thead class="table-dark text-white">
          <tr>
            <th scope="col" class="text-center">Sl No</th>
            <th scope="col">Name</th>
            <th scope="col">Service Name</th>
            <th scope="col">Resume</th>
            <th scope="col">Status</th>
            <th scope="col" class="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(professional, index) in professionals" :key="professional.id">
            <td class="text-center fw-bold">{{ index + 1 }}</td>
            <td class="fw-semibold">{{ professional.name }}</td>
            <td>{{ professional.service }}</td>
            <td>
              <a v-if="professional.resume" :href="professional.resume" target="_blank" class="btn btn-sm btn-info">
                View Resume
              </a>
              <span v-else class="text-muted">No Resume</span>
            </td>
            <td>
              <span :class="statusClass(professional.status)">{{ professional.status }}</span>
            </td>
            <td class="text-center">
              <button 
                v-if="professional.status === 'Pending'" 
                @click="updateStatus(professional.id, 'Approved')" 
                class="btn btn-success btn-sm me-2">
                Accept
              </button>
              <button 
                v-if="professional.status === 'Pending'" 
                @click="deleteProfessional(professional.id)" 
                class="btn btn-danger btn-sm">
                Reject
              </button>
              <button 
                v-if="professional.status === 'Approved'" 
                @click="updateStatus(professional.id, 'Blocked')" 
                class="btn btn-warning btn-sm me-2">
                Block
              </button>
              <button 
                v-if="professional.status === 'Approved' || professional.status === 'Blocked'" 
                @click="deleteProfessional(professional.id)" 
                class="btn btn-danger btn-sm">
                Delete
              </button>
              <button 
                v-if="professional.status === 'Blocked'" 
                @click="updateStatus(professional.id, 'Approved')" 
                class="btn btn-success btn-sm me-2">
                Unblock
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="professionals.length === 0" class="text-center my-4">
      <p class="text-muted fw-semibold">No professionals found.</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  name: "ManageProfessionals",
  setup() {
    const professionals = ref([]);

    const fetchProfessionals = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/professionals");
        professionals.value = response.data;
      } catch (error) {
        console.error("Error fetching professionals:", error);
      }
    };

    const updateStatus = async (id, newStatus) => {
      try {
        await axios.put(`http://127.0.0.1:5000/professionals/${id}`, { status: newStatus });
        professionals.value = professionals.value.map(professional =>
          professional.id === id ? { ...professional, status: newStatus } : professional
        );
      } catch (error) {
        console.error("Error updating status:", error);
      }
    };

    const deleteProfessional = async (id) => {
      try {
        await axios.delete(`http://127.0.0.1:5000/professionals/${id}`);
        professionals.value = professionals.value.filter(professional => professional.id !== id);
      } catch (error) {
        console.error("Error deleting professional:", error);
      }
    };

    const statusClass = (status) => {
      return {
        "badge bg-warning text-dark": status === "Pending",
        "badge bg-success": status === "Approved",
        "badge bg-danger": status === "Blocked",
      };
    };

    onMounted(fetchProfessionals);

    return { professionals, fetchProfessionals, updateStatus, deleteProfessional, statusClass };
  },
};
</script>


<style scoped>
.container {
  max-width: 1400px;
  margin: auto;
}
.table th,
.table td {
  vertical-align: middle;
  text-align: center;
}
.table-hover tbody tr:hover {
  background-color: #f8f9fa;
}
.badge {
  font-size: 0.9rem;
  padding: 6px 12px;
}
.btn-sm {
  padding: 5px 10px;
  font-size: 0.875rem;
}
</style>