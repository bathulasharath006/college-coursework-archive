<template>
    <div>
      <button class="btn btn-warning go-back-button" @click.prevent="goBack">Back
      </button><br>
      <ul class="nav nav-pills nav-fill">
        <li class="nav-item">
          <router-link :to="`/StatisticsHome`" class="btn btn-success">Overview</router-link>
        </li>
        <li class="nav-item">
          <a class="btn btn-primary">BookWise</a>
        </li>
        <li class="nav-item">
          <router-link :to="`/StatisticsSect`" class="btn btn-success" > Sections 
          </router-link>
        </li>
        <li class="nav-item">
          <router-link :to="`/TransActions`" class="btn btn-success">Transactions</router-link>
        </li>
      </ul><br>
  
      <div style="text-align: center;">
        <form @submit.prevent="GetDetails">
          <input type="text" v-model="searchBook_id" placeholder="Enter Book ID" required />&emsp;
          <input type="submit" class="btn btn-warning" value="Get Details" />
        </form>
      </div><br>
  
      <div v-if="book_id">
          <div class="row">
            <div class="col-md-7">
              <img :src="`/book_files/${book_id}.jpg`" alt="BOOK IMAGE NOT FOUND" class="book-image">
            </div>
            <div class="col-md-5">
              <img src="@/../../db_directory/plots/Accept_Vs_Reject.png" alt="FILE NOT FOUND" class="accept-reject-image"><br><br>
              <h3 class="err_msg">Ratings</h3><br>
              <img src="@/../../db_directory/plots/ratings.png" alt="FILE NOT FOUND" class="ratings-image">
            </div>
          </div>
      </div>
      <div v-else>
        <h3 class="err_msg">{{ message }}</h3>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '../axiosConfig';
  
  export default {
    name: 'BookWise',
    data() {
      return {
        message: "Enter Book ID Which is Present in the Library Base",
        searchBook_id: null,
        book_id: null
      }
    },
    methods: {
      async GetDetails() {
        await axios.get(`/bookStats/${this.searchBook_id}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("adm_token")}` },
        })
        .then(response => this.book_id = response.data.book_id)
        .catch(error => this.book_id = error.response.data.book_id);
      },
      goBack() { this.$router.push('/admin_home'); }
    }
  }
  </script>
  
  <style scoped>
  .book-image {
    width: 100%;
    max-width: 680px;
    max-height: 780px;
  }
  
  .accept-reject-image {
    width: 100%;
    max-width: 350px;
    max-height: 350px;
  }
  
  .ratings-image {
    width: 100%;
    max-width: 680px;
    max-height: 350px;
  }
  
  .container {
    display: flex;
    flex-wrap: wrap;
  }
  .go-back-button {
    position: absolute;
    top: 10px;
    right: 10px;
  }
</style>