<template>
    <BackButton />
    <div class="not-found">
      <h1>404 - Page Not Found</h1>
      <p>The URL you are looking for doesn't exist.</p>
    </div>
  </template>
  
  <script>
  export default {
    name: "NotFound",
  };
  </script>
  
<style scoped>
.not-found {
  background-color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  text-align: center;
  height: 100vh; /* Full viewport height */
}
</style>