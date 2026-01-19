
import { createRouter, createWebHistory } from "vue-router";
import HomeView from '../views/HomeView.vue';
import CustomerSignup from "@/views/CustomerSignup.vue";
import Login from "@/views/Login.vue";
import SignUpOption from "@/views/SignUpOption.vue";
import ProfessionalSignup from "@/views/ProfessionalSignup.vue";
import AdminDashboard from "@/views/AdminDashboard.vue";
import CustomerDashboard from "@/views/CustomerDashboard.vue";
import ProfessionalDashboard from "@/views/ProfessionalDashboard.vue";
import store from "@/store";  // Ensure Vuex store is imported
import ApprovalPending from "@/views/ApprovalPending.vue";
import ManageService from "@/views/ManageService.vue";
import ManageProfessionals from "@/views/ManageProfessionals.vue";
import ManageCustomers from "@/views/ManageCustomers.vue";
import Profile from "@/views/Profile.vue";
import OngoingService from "@/views/OngoingService.vue";
import CompletedBookings from "@/views/CompletedBookings.vue";
import MyBookings from "@/views/MyBookings.vue";
import NewServiceRequests from "@/views/NewServiceRequests.vue";
import ProfessionlBookings from "@/views/ProfessionlBookings.vue";
import ProfessionalScheduledService from "@/views/ProfessionalScheduledService.vue";
import ProfessionalServiceHistory from "@/views/ProfessionalServiceHistory.vue";
import Feedback from "@/views/Feedback.vue";
import ContactUs from "@/views/ContactUs.vue";
import Payment from "@/views/Payment.vue";
import AdminBookingOverview from "@/views/AdminBookingOverview.vue";
import Analytics from "@/views/Analytics.vue";
import Blocked from "@/views/Blocked.vue";
import Search from "@/views/Search.vue";
import ProfessionalAnalytics from "@/views/ProfessionalAnalytics.vue";
// Define the routes
const routes = [
  { path: "/", name: "home", component: HomeView },
  { path: "/customersignup", name: "CustomerSignup", component: CustomerSignup },
  { path: "/login", name: "Login", component: Login },
  { path: "/signupoption", name: "Signup", component: SignUpOption },
  { path: "/professionalsignup", name: "ProfessionalSignup", component: ProfessionalSignup },
  { path: "/admindashboard", name: "AdminDashboard", component: AdminDashboard },
  { path: "/customerdashboard", name: "CustomerDashboard", component: CustomerDashboard },
  { path: "/professionaldashboard", name: "ProfessionalDashboard", component: ProfessionalDashboard },
  {path:"/approvalpending",name:"ApprovalPending",component:ApprovalPending},
  {path:"/manageservices",name:"ManageServie",component:ManageService},
  {path:"/manageprofessionals",name:"ManageProfessionals",component:ManageProfessionals},
  {path:"/managecustomers",name:"ManageCustomers",component:ManageCustomers},
  {path:"/adminbookingoverview",name:"AdminBookingOverView",component:AdminBookingOverview},
  {path:"/ongoingservice",name:"OngoingService",component:OngoingService},
  {path:"/completedbookings",name:"CompletedBookings",component:CompletedBookings},
  {path:"/mybookings",name:"Mybookings",component:MyBookings},
  {path:"/newservicerequest",name:"NewServiceRequest",component:NewServiceRequests},
  {path:"/professionalbookings",name:"ProfessionalBookings",component:ProfessionlBookings},
  {path:"/professionalscheduledservices",name:"ProfessionalScheduledService",component:ProfessionalScheduledService},
  {path:"/professionalservicehistory",name:"ProfessionalServiceHistory",component:ProfessionalServiceHistory},
  {path:"/feedback/:bookingId",name:"Feedback",component:Feedback,props: true },
  {path:"/myprofile",name:"Profile",component:Profile},
  {path:"/contactus",name:"ContactUs",component:ContactUs},
  {path:"/payments",name:"Payment",component:Payment},
  {path:"/analytics",name:"Analytics",component:Analytics,meta: { requiresAuth: true }},
  {path:"/blocked",name:"Blocked",component:Blocked},
  {path:"/search",name:"Search",component:Search},
  {path:"/professionalanalytics",name:"ProfessionalAnalytics",component:ProfessionalAnalytics}

];

// Create the router instance
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash, // Scroll to the section corresponding to the hash
        behavior: "smooth", // Smooth scrolling
      };
    }
    return savedPosition || { top: 0 }; // Default scroll behavior
  }
});

// Add the navigation guard to check role before entering a protected route
router.beforeEach((to, from, next) => {
  const token = store.state.token;
  const userRole = store.state.user ? store.state.user.role : null;
  const isApproved = store.state.user ? store.state.user.approved : false;

  if (!token) {
    if (!["/", "/login", "/signupoption", "/professionalsignup", "/customersignup", "/blocked", "/approvalpending"].includes(to.path)) {
      alert("Session expired. Please log in again.");
      next("/");
    } else {
      next(); 
    }
  } else if (to.name === "admindashboard" && userRole !== "admin") {
    alert("Unauthorized access.");
    next("/");
  } else if (to.name === "customerdashboard" && userRole !== "customer") {
    alert("Unauthorized access.");
    next("/");
  } else if (to.name === "professionaldashboard") {
    if (userRole !== "professional") {
      alert("Unauthorized access.");
      next("/");
    } else if (!isApproved) {
      alert("Your account is pending approval.");
      next("/approvalpending"); 
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;





