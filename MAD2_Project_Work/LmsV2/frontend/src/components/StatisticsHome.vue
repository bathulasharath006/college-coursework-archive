<template>
    <button class="btn btn-warning go-back-button" @click.prevent="goBack">Back
    </button><br>
    <ul class="nav nav-pills nav-fill">
      <li class="nav-item">
        <a class="btn btn-primary" > Overview </a>
      </li>
      <li class="nav-item">
        <router-link :to="`/BookWise`" class="btn btn-success" > BookWise 
        </router-link>
      </li>
      <li class="nav-item">
        <router-link :to="`/StatisticsSect`" class="btn btn-success" > Sections 
        </router-link>
      </li>
      <li class="nav-item">
        <router-link :to="`/TransActions`" class="btn btn-success" > Transactions 
        </router-link>
      </li>
    </ul><br>

  <div>
    <div class="top-row">
      <div >
        <h3 class="err_msg">Top 10 Most Issued Books (Popular Books)</h3>
        <img src="@/../../db_directory/plots/popular_books.png" alt="Rectangle Image 1" class="top-image">
      </div>
      <div >
        <h3 class="err_msg">Top 10 Frequent Book Borrowers</h3>
        <img src="@/../../db_directory/plots/popular_borrowers.png" alt="Rectangle Image 2" class="top-image">
      </div>
    </div><br>
    <div class="bottom-row">
      <h3 class="err_msg">Scatterplot for Past 10 Days with Accept and Reject Actions</h3><br>
      <img src="@/../../db_directory/plots/scatter.png" alt="Rectangle Image 3" class="bottom-image">
    </div>
  </div>
</template>

<script>

export default {
  name: 'StatisticsHome',
  methods: { goBack() { this.$router.push('/admin_home'); } }
}
</script>

<style scoped>
.top-row {
  display: flex;
  width: 100%;
}

.top-image {
  height: auto;
  max-width: 80%;
}

.bottom-row {
  width: 100%;
}

.bottom-image {
  width: 100%;
  height: auto;
}

.go-back-button {
    position: absolute;
    top: 10px;
    right: 10px;
  }
</style>