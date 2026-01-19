<template>
  <div class="container mt-4">
    <h2 class="text-center text-primary mb-3 fw-bold">Manage Customers</h2>

    <!-- Table for Customer Management -->
    <div class="table-responsive">
      <table class="table table-hover align-middle shadow-sm">
        <thead class="table-dark text-white">
          <tr>
            <th scope="col" class="text-center">Sl No</th>
            <th scope="col">Username</th>
            <th scope="col">Phone</th>
            <th scope="col">Address</th>
            <th scope="col">Status</th>
            <th scope="col" class="text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(customer, index) in customers" :key="customer.id">
            <td class="text-center fw-bold">{{ index + 1 }}</td>
            <td class="fw-semibold">{{ customer.username }}</td>
            <td>{{ customer.phone_no }}</td>
            <td>{{ customer.address }}</td>
            <td>
              <span :class="customer.is_blocked ? 'badge bg-danger' : 'badge bg-success'">
                {{ customer.is_blocked ? 'Blocked' : 'Active' }}
              </span>
            </td>
            <td class="text-center">
              <!-- Block/Unblock Button -->
              <button 
                class="btn btn-sm me-2"
                :class="customer.is_blocked ? 'btn-success' : 'btn-danger'"
                @click="toggleBlockStatus(customer)">
                {{ customer.is_blocked ? 'Unblock' : 'Block' }}
              </button>

              <!-- Delete Button (Only when Blocked) -->
              <button 
                v-if="customer.is_blocked"
                class="btn btn-sm btn-outline-danger"
                @click="deleteCustomer(customer)">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty State Message -->
    <div v-if="customers.length === 0" class="text-center my-4">
      <p class="text-muted fw-semibold">No customers found.</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  name: "ManageCustomers",
  setup() {
    const customers = ref([]);

    const fetchCustomers = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5000/managecustomers");
        customers.value = response.data;
      } catch (error) {
        console.error("Error fetching customers:", error);
      }
    };

    const toggleBlockStatus = async (customer) => {
      console.log(`Toggling block status for user_id: ${customer.user_id}`);

      try {
        const response = await axios.put(`http://127.0.0.1:5000/managecustomers/${customer.user_id}`);
        alert(response.data.message);

        // Update UI instantly
        customer.is_blocked = !customer.is_blocked;
      } catch (error) {
        console.error("Error updating customer status:", error);
      }
    };

    const deleteCustomer = async (customer) => {
      if (!confirm(`Are you sure you want to delete ${customer.username}?`)) return;

      try {
        const response = await axios.delete(`http://127.0.0.1:5000/managecustomers/${customer.user_id}`);
        alert(response.data.message);

        // Remove deleted customer from list
        customers.value = customers.value.filter(c => c.id !== customer.id);
      } catch (error) {
        console.error("Error deleting customer:", error);
        alert(error.response?.data?.message || "Failed to delete customer");
      }
    };

    onMounted(fetchCustomers);

    return { customers, fetchCustomers, toggleBlockStatus, deleteCustomer };
  },
};
</script>




<style scoped>
.container {
  max-width: 1400px;
  margin: auto;
}

/* Improved table spacing */
.table th,
.table td {
  vertical-align: middle;
  text-align: center;
}

/* Hover effect */
.table-hover tbody tr:hover {
  background-color: #f8f9fa;
}

/* Status badges */
.badge {
  font-size: 0.9rem;
  padding: 6px 12px;
}

/* Button spacing */
.btn-sm {
  padding: 5px 10px;
  font-size: 0.875rem;
}
</style>
