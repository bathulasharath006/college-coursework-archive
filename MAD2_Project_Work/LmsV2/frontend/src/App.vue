<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

body {
  background-image: url('./assets/user_home_page.avif');
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.err_msg {
    display: inline-block;
    text-align: center;
    font-weight: bold;
    background-color: white;
    padding: 10px;
    border-radius: 5px;
}

</style>
