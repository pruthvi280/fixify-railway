<template>
  <div class="container mt-4">
    <h2 class="text-center text-primary mb-3">Manage Services</h2>

    <!-- Buttons to Open Modals -->
    <div class="mb-3">
      <button class="btn btn-primary me-2" @click="openCategoryModal">Add Category</button>
      <button class="btn btn-success" @click="openServiceModal(null)">Add Service</button>
    </div>

    <!-- ✅ Categories Table -->
    <div class="table-responsive" style="max-height: 400px;">
      <table class="table">
        <thead class="table-primary">
          <tr>
            <th scope="col">Sl.No</th>
            <th scope="col">Category Name</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(category, index) in categories" :key="category.id">
            <td>{{ index + 1 }}</td>
            <td>{{ category.name }}</td>
            <td>
              <button class="btn btn-danger" @click="deleteCategory(category.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ✅ Services Table -->
    <div class="table-responsive" style="max-height: 400px;">
      <table class="table">
        <thead class="table-success">
          <tr>
            <th scope="col">Sl.No</th>
            <th scope="col">Service Name</th>
            <th scope="col">Category</th>
            <th scope="col">Description</th>
            <th scope="col">Price</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(service, index) in services" :key="service.id">
            <td>{{ index + 1 }}</td>
            <td>{{ service.name }}</td>
            <td>{{ getCategoryName(service.category_id) }}</td>
            <td>{{ service.description }}</td>
            <td>{{ service.base_price }}</td>
            <td>
              <button class="btn btn-warning me-2" @click="editServiceDetails(service)">Edit</button>
              <button class="btn btn-danger" @click="deleteService(service.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- ✅ Add Category Modal -->
    <div class="modal fade" id="categoryModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Category</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <input type="text" class="form-control" v-model="newCategory" placeholder="Enter Category Name" />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="addCategory">Add Category</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ✅ Add/Edit Service Modal -->
    <div class="modal fade" id="serviceModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ editingServiceId ? 'Edit Service' : 'Add Service' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">
            <select class="form-select mb-2" v-model="newService.category">
              <option value="" disabled>Select Category</option>
              <option v-for="category in categories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
            <input type="text" class="form-control mb-2" v-model="newService.name" placeholder="Enter Service Name" />
            <input type="text" class="form-control mb-2" v-model="newService.description" placeholder="Enter Service Description" />
            <input type="number" class="form-control" v-model="newService.base_price" placeholder="Enter Service Price" />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-success" @click="addOrUpdateService">
              {{ editingServiceId ? 'Update Service' : 'Add Service' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { Modal } from "bootstrap";
import axios from "axios";

export default {
  data() {
    return {
      categories: [],
      services: [],
      newCategory: "",
      newService: {
        name: "",
        description: "",
        base_price: null,
        category: "",
      },
      editingServiceId: null,
      categoryModal: null,
      serviceModal: null,
    };
  },

  mounted() {
    this.fetchCategories();
    this.fetchServices();
  },

  methods: {

    getCategoryName(categoryId) {
      const category = this.categories.find(cat => Number(cat.id) === Number(categoryId));
      return category ? category.name : "Unknown";
    },



    fetchCategories() {
      axios.get("/categories")
        .then(response => this.categories = response.data)
        .catch(error => console.error("Error fetching categories:", error));
    },


    fetchServices() {
      axios.get("/services")
        .then(response => this.services = response.data)
        .catch(error => console.error("Error fetching services:", error));
    },

 
    openCategoryModal() {
      if (!this.categoryModal) {
        this.categoryModal = new Modal(document.getElementById("categoryModal"));
      }
      this.categoryModal.show();
    },


    openServiceModal(service) {
      if (service) {
        this.newService = { ...service };
        this.editingServiceId = service.id;
      } else {
        this.resetServiceForm();
      }

      if (!this.serviceModal) {
        this.serviceModal = new Modal(document.getElementById("serviceModal"));
      }
        this.serviceModal.show();
    },



    async addCategory() {
      if (!this.newCategory.trim()) {
        alert(" Category name is required");
        return;
      }

      try {
        await axios.post("/categories", { name: this.newCategory });
        this.newCategory = "";
        this.categoryModal.hide();
        this.fetchCategories();
      } catch (error) {
        if (error.response && error.response.status === 409) {
          alert(" Category already exists!");
        } else {
          console.error("Error adding category:", error);
        }
      }
    },



    async addOrUpdateService() {
      if (!this.newService.name || !this.newService.description || !this.newService.base_price || !this.newService.category) {
        alert(" All fields are required!");
        return;
      }

      try {
        if (this.editingServiceId) {

          await axios.put(`/services/${this.editingServiceId}`, this.newService);
          alert(" Service updated successfully!");
        } else {

          await axios.post("/services", this.newService);
          alert(" Service added successfully!");
        }
        this.serviceModal.hide(); // Close modal after successful action
        this.fetchServices(); // Refresh services list
        this.resetServiceForm(); // Reset form after action
      } catch (error) {
        if (error.response && error.response.status === 409) {
          alert(" Service with the same name already exists under this category!");
        } else {
          console.error("Error adding/updating service:", error);
        }
      }
    },
    

    editServiceDetails(service) {
      this.newService = { 
        name: service.name, 
        description: service.description, 
        base_price: service.base_price, 
        category: Number(service.category_id) // Convert to number
      };
      this.editingServiceId = service.id;
      this.openServiceModal(service);
    },



    async deleteCategory(categoryId) {
      if (confirm("Are you sure you want to delete this category?")) {
        try {
          await axios.delete(`/categories/${categoryId}`);
          alert(" Category deleted successfully!");
          this.fetchCategories(); // Refresh category list
        } catch (error) {
          if (error.response && error.response.status === 400) {
            alert(" Cannot delete category with associated services!");
          } else {
            console.error("Error deleting category:", error);
            alert(" Failed to delete category. Please try again.");
          }
        }
      }
    },


    async deleteService(serviceId) {
      if (confirm("Are you sure you want to delete this service?")) {
        try {
          await axios.delete(`/services/${serviceId}`);
          alert(" Service deleted successfully!");
          this.fetchServices(); // Refresh after deletion
        } catch (error) {
          console.error("Error deleting service:", error);
          alert(" Failed to delete service. Please try again.");
        }
      }
    },


    // ✅ Reset Service Form
    resetServiceForm() {
      this.newService = { name: "", description: "", base_price: null, category: "" };
      this.editingServiceId = null;
    },
  }
};
</script>



<style>
/* Add any custom styling here */
</style>




