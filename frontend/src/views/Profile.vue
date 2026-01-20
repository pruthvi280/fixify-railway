<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-10">
        <!-- Profile Update Card -->
        <div class="card shadow-sm">
          <div class="card-header bg-primary text-white">
            <h3 class="mb-0">Update Your Profile</h3>
          </div>
          <div class="card-body">
            <form @submit.prevent="updateProfile">
              <div class="row">
                <!-- Full Name Field -->
                <div class="col-md-6 mb-3">
                  <label for="fullName" class="form-label">Full Name</label>
                  <input
                    v-model="profile.fullName"
                    type="text"
                    class="form-control"
                    id="fullName"
                    placeholder="Enter your full name"
                    required
                  />
                </div>

                <!-- Phone Number Field -->
                <div class="col-md-6 mb-3">
                  <label for="phone" class="form-label">Phone Number</label>
                  <input
                    v-model="profile.phone"
                    type="tel"
                    class="form-control"
                    id="phone"
                    placeholder="Enter your phone number"
                    required
                  />
                </div>

                <!-- Email Field (Disabled) -->
                <div class="col-md-6 mb-3">
                  <label for="email" class="form-label">Email</label>
                  <input
                    v-model="profile.email"
                    type="email"
                    class="form-control"
                    id="email"
                    placeholder="Enter your email"
                    required
                    disabled
                  />
                </div>

                <!-- Address Field -->
                <div class="col-md-6 mb-3">
                  <label for="address" class="form-label">Address</label>
                  <textarea
                    v-model="profile.address"
                    class="form-control"
                    id="address"
                    rows="3"
                    placeholder="Enter your address"
                    required
                  ></textarea>
                </div>

                <!-- Role Display -->
                <div class="col-md-12 mb-3">
                  <label class="form-label">Role</label>
                  <input
                    v-model="profile.role"
                    type="text"
                    class="form-control"
                    disabled
                  />
                </div>
              </div>

              <!-- Submit Button -->
              <button type="submit" class="btn btn-primary w-100 mt-3">Update Profile</button>
            </form>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="alert alert-danger mt-3">
          {{ errorMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import axios from "axios";

export default {
  setup() {
    const profile = ref({
      fullName: "",
      email: "",
      phone: "",
      address: "",
      role: "", 
    });

    const errorMessage = ref("");

    // Fetch Profile Data
    const fetchProfile = async () => {
      try {
        //  FIX: Use relative path (works on both Localhost and Railway)
        const response = await axios.get("/profile", {
          headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
        });

        profile.value = {
          fullName: response.data.fullName,
          email: response.data.email,
          phone: response.data.phone || "",
          address: response.data.address || "",
          role: response.data.role, 
        };
      } catch (error) {
        console.error(error); // Log error to see what happens
        errorMessage.value = "Failed to load profile. Please try again.";
      }
    };

    // Update Profile
    const updateProfile = async () => {
      try {
        //  Use relative path here too
        await axios.put(
          "/profile",
          {
            fullName: profile.value.fullName, 
            phone: profile.value.phone,
            address: profile.value.address,
          },
          {
            headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
          }
        );
        alert("Profile updated successfully!");
      } catch (error) {
        console.error(error);
        errorMessage.value = "Failed to update profile. Please try again.";
      }
    };

    onMounted(fetchProfile);

    return {
      profile,
      errorMessage,
      updateProfile,
    };
  },
};
</script>


<style scoped>
.container {
  max-width: 1000px;
}

.card {
  border-radius: 10px;
}

.card-header {
  font-size: 1.5rem;
}

.form-label {
  font-weight: 500;
}

button {
  font-size: 1rem;
  padding: 12px;
}

textarea {
  resize: vertical;
}

.row .col-md-6 {
  padding-right: 15px;
  padding-left: 15px;
}

@media (max-width: 767px) {
  .col-md-6 {
    margin-bottom: 15px;
  }
  button {
    font-size: 1.1rem;
  }
}
</style>
