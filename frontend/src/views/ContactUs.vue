<template>
  <div class="contact-us">
    <!-- <h1>{{ pageTitle }}</h1> -->
    <p>{{ pageDescription }}</p>

    <!-- FAQ Section -->
    <div class="faq-section">
      <h2>Frequently Asked Questions</h2>
      <div v-for="(faq, index) in filteredFaqs" :key="index" class="faq-item">
        <button class="faq-question" @click="toggleFAQ(index)">
          {{ faq.question }}
          <span>{{ activeFAQ === index ? "▲" : "▼" }}</span>
        </button>
        <p v-if="activeFAQ === index" class="faq-answer">{{ faq.answer }}</p>
      </div>
    </div>

    <!-- Contact Us Section -->
    <div class="contact-section">
      <h2>Still Need Help?</h2>
      <p>If you have further questions, feel free to contact us.</p>
      <button @click="sendEmail" class="contact-button">Contact Support</button>
    </div>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import store from "@/store"; // Assuming the role is stored in Vuex store

export default {
  name: "ContactUs",
  setup() {
    const activeFAQ = ref(null);

    const userRole = computed(() => store.state.user?.role || "customer"); // Get user role from Vuex

    // Customer FAQs
    const customerFaqs = [
      { question: "How do I book a service?", answer: "You can book a service from the 'New Service Request' page after logging in." },
      { question: "How do I track my ongoing services?", answer: "Go to 'Ongoing Services' in your dashboard to check the status." },
      { question: "How can I update my profile information?", answer: "You can update your name, phone, and address in the 'My Profile' section." },
      { question: "What if I need to cancel a service?", answer: "You can cancel a booking from the 'My Bookings' section before it starts." }
    ];

    // Professional FAQs
    const professionalFaqs = [
      { question: "How do I accept a service request?", answer: "You can check and accept new service requests from the 'New Requests' section in your dashboard." },
      { question: "Where can I find accepted services?", answer: "Once you accept the new services, it will be available in scheduled services section." },
      { question: "Where can I see my progress activity?", answer: "You can check out in MyReviews/Rating section."},
      { question: "How can I update my availability?", answer: "You can update your service availability in the 'Profile' section of your dashboard." }
    ];

    // Choose FAQs based on the user's role
    const filteredFaqs = computed(() => {
      return userRole.value === "professional" ? professionalFaqs : customerFaqs;
    });

    // // Dynamic Page Titles Based on Role
    // const pageTitle = computed(() => {
    //   return userRole.value === "professional"
    //     ? "Support for PROFESSIONALS"
    //     : "Support for CUSTOMERS";
    // });

    const pageDescription = computed(() => {
      return userRole.value === "professional"
        ? "Find answers to your questions as a professional service provider."
        : "Find answers to your questions as a customer using our platform.";
    });

    const toggleFAQ = (index) => {
      activeFAQ.value = activeFAQ.value === index ? null : index;
    };

    const sendEmail = () => {
      window.location.href = "mailto:support@fixify.com?subject=Support Request";
    };

    return { userRole,  pageDescription, filteredFaqs, activeFAQ, toggleFAQ, sendEmail };
  },
};
</script>

<style scoped>
.contact-us {
  text-align: center;
  padding: 20px;
  max-width: 600px;
  margin: auto;
}

/* FAQ Section */
.faq-section {
  text-align: left;
  margin-top: 20px;
}

.faq-item {
  margin-bottom: 10px;
}

.faq-question {
  width: 100%;
  text-align: left;
  background: #f8f9fa;
  border: none;
  padding: 10px;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  justify-content: space-between;
}

.faq-answer {
  background: #f1f1f1;
  padding: 10px;
  margin-top: 5px;
  border-left: 4px solid #007bff;
}

/* Contact Us Section */
.contact-section {
  margin-top: 30px;
}

.contact-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
  margin-top: 10px;
}

.contact-button:hover {
  background-color: #0056b3;
}
</style>
