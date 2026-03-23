<template>
    <div class="background">
      <div class="card" style="width: 18rem;">
        <img src="../assets/success.gif" class="card-img-top" />
        <div class="card-body" style="text-align: center;">
          <h5 class="card-title"><b>{{ heading }}</b></h5><br>
          <p class="card-text">{{ message }}</p>
          <b>{{ ending }}</b><br><br>

          <router-link v-if="url" :to="url">
            <button class="btn btn-success">Go Back</button>
        </router-link>

        </div>
      </div>
    </div>
</template>

<script>
import axios from '../axiosConfig';

export default {
  name: 'SuccessPage',
    data() {
      return { heading: null,
        message: null,
        ending: null,
        url: null,
        succ_id: null,
      }
    },
    mounted() {
      this.succ_id = this.$route.params.succ_id;
      this.loadPage();
    },
    methods: {
      async loadPage() {
        axios.get(`/success_page/${this.succ_id}`)
        .then(response => {
          const data = response.data;
          this.heading = data.heading;
          this.message = data.message;
          this.ending = data.ending;
          this.url = data.url;
        })
      }
    }
  };
</script>

<style scoped>
  .background {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    margin: 0;
    padding: 0;
    background-image: url("../assets/success_bg.avif");
  }
  .card-body {
    text-align: center;
  }
</style>