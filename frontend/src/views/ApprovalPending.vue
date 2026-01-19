<template>
  <div class="approvalpending-page">
    <div class="card">
      <h1>Approval Pending</h1>
      <p>
        Your professional account is currently under review by our admin.
        Once approved, you will be able to access your dashboard and start
        receiving service requests.
      </p>

      <router-link to="/" class="btn">Back to Home</router-link>
    </div>
  </div>
</template>

<style scoped>
.approvalpending-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f4f6fb;
  padding: 1rem;
}

.card {
  background: white;
  padding: 2.5rem 2rem;
  max-width: 500px;
  width: 100%;
  text-align: center;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.card h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #1a1a2e;
  margin-bottom: 1rem;
}

.card p {
  color: #555;
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.btn {
  display: inline-block;
  padding: 12px 24px;
  background: #667eea;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: 600;
  transition: background 0.3s, transform 0.2s;
}

.btn:hover {
  background: #5a6fe0;
  transform: translateY(-2px);
}
</style>
