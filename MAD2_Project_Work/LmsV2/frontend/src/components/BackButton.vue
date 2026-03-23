<template>
  <button type="button" class="btn btn-warning go-back-button" @click.prevent="goBack">Back</button>
</template>
  
<script>
  export default {
    name: 'BackButton',
    methods: {
      goBack() {
        this.$router.go(-1);
      },
    },
  };
</script>
  
<style scoped>
  .go-back-button {
    position: absolute;
    top: 10px;
    right: 10px;
  }
</style>
  