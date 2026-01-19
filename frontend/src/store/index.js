import { createStore } from 'vuex';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import router from '@/router';

const store = createStore({
  state: {
    token: localStorage.getItem('token') || null,
    user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null,  
  },
  mutations: {
    setToken(state, token) {
      if (token) {
        const decodedToken = jwtDecode(token);
        const currentTime = Math.floor(Date.now() / 1000); // Current time in seconds

        if (decodedToken.exp < currentTime) {
          console.warn("Token expired! Logging out...");
          store.dispatch("logout");
          return;
        }

        state.token = token;
        localStorage.setItem('token', token);
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      } else {
        state.token = null;
        localStorage.removeItem('token');
        delete axios.defaults.headers.common["Authorization"];
      }
    },
    setUser(state, user) {
      state.user = user;
      localStorage.setItem('user', JSON.stringify(user));
    }
  },
  actions: {
    login({ commit }, { token, user }) {
      commit('setToken', token);
      commit('setUser', user);
    },
    async logout({ commit }) {
      try {
        const token = store.state.token;
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        await axios.post('http://127.0.0.1:5000/logout'); // Call logout API
      } catch (error) {
        console.error('Logout failed:', error);
      }
      
      commit('setToken', null);
      commit('setUser', null);
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      delete axios.defaults.headers.common["Authorization"];
      router.push('/');
    }
  },
  getters: {
    userRole(state) {
      return state.user ? state.user.role : null;
    }
  }
});

// ✅ Check token expiration at app startup
if (store.state.token) {
  const decodedToken = jwtDecode(store.state.token);
  const currentTime = Math.floor(Date.now() / 1000); // Get current time in seconds

  if (decodedToken.exp < currentTime) {
    console.warn("Token expired on page load! Logging out...");
    store.dispatch("logout");
  } else {
    axios.defaults.headers.common['Authorization'] = `Bearer ${store.state.token}`;
  }
}

export default store;
