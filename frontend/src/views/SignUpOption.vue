<template>
  <div class="signup-page">
    <div class="signup-container">
      <div class="logo">Fixify</div>
      <h1>Join Fixify</h1>
      <p>Choose how you want to get started</p>

      <div class="options">
        <router-link to="/customersignup" class="option-card customer">
          <h2>I Need Services</h2>
          <p>Book trusted professionals for your home</p>
          <span class="arrow">→</span>
        </router-link>

        <router-link to="/professionalsignup" class="option-card professional">
          <h2>I Provide Services</h2>
          <p>Start earning by offering your expertise</p>
          <span class="arrow">→</span>
        </router-link>
      </div>

      <div class="login-link">
        Already have an account?
        <router-link to="/login">Log in</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
defineOptions({
  name: "SignUpOptions",
});
</script>

<style scoped>
.signup-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.signup-container {
  max-width: 900px;
  width: 100%;
  text-align: center;
}

.logo {
  font-size: 2.5rem;
  font-weight: 800;
  color: white;
  margin-bottom: 1rem;
}

h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 0.5rem;
}

.signup-container > p {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.1rem;
  margin-bottom: 3rem;
}

.options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.option-card {
  background: white;
  border-radius: 20px;
  padding: 3rem 2rem;
  text-decoration: none;
  color: #1a1a2e;
  transition: transform 0.3s, box-shadow 0.3s;
}

.option-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}

.option-card h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  color: #1a1a2e;
}

.option-card p {
  color: #666;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.arrow {
  font-size: 1.5rem;
  color: #667eea;
  display: inline-block;
}

.login-link {
  color: white;
  font-size: 1rem;
  margin-top: 2rem;
}

.login-link a {
  color: #FFD700;
  text-decoration: none;
  font-weight: 600;
}

.login-link a:hover {
  text-decoration: underline;
}

@media (max-width: 768px) {
  .options {
    grid-template-columns: 1fr;
  }

  h1 {
    font-size: 2rem;
  }

  .logo {
    font-size: 2rem;
  }
}
</style>
