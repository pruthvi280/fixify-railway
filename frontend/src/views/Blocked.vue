<template>
  <div class="blocked-page">
    <h1>Account Blocked</h1>
    <p>Your account has been blocked by the administrator. Please contact support for further assistance.</p>
    <router-link to="/" class="btn">Back to Home</router-link>
  </div>
</template>

<style scoped>
.blocked-page {
  text-align: center;
  margin-top: 50px;
}
.btn {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: red;
  color: white;
  text-decoration: none;
  border-radius: 5px;
}
</style>
