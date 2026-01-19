
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';


axios.interceptors.response.use(
  (response) => response,
  (error) => {
    // If the response status is 401, redirect to the login page
    if (error.response && error.response.status === 401) {
      router.push('/login'); 
    }
    return Promise.reject(error);
  }
);

const app = createApp(App)

app.use(router)
app.use(store)

app.mount('#app')
