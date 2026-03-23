<template>
    <button class="btn btn-warning go-back-button" @click.prevent="goBack">Back
    </button><br>
    <ul class="nav nav-pills nav-fill">
      <li class="nav-item">
        <router-link :to="`/StatisticsHome`" class="btn btn-success"> Overview 
        </router-link>
      </li>
      <li class="nav-item">
        <router-link :to="`/BookWise`" class="btn btn-success" > BookWise 
        </router-link>
      </li>
      <li class="nav-item">
        <a class="btn btn-primary" > Sections  </a>
      </li>
      <li class="nav-item">
        <router-link :to="`/TransActions`" class="btn btn-success" > Transactions 
        </router-link>
      </li>
    </ul><br>

    <div style="text-align: center;">
        <h3 class="err_msg"> No. of Books Available in Each Section </h3><br>
        <img src="@/../../db_directory/plots/sections.png" alt="BOOK IMAGE NOT FOUND" class="sect-img"/>
    </div>
</template>

<script>
export default {
  name: 'StatisticsSect',
  methods: {  goBack() { this.$router.push('/admin_home'); }  }
}
</script>

<style scoped>
  .sect-img {
    width: 100%;
    max-width: 1800px;
    max-height: 750px;
  }

.go-back-button {
    position: absolute;
    top: 10px;
    right: 10px;
  }
</style>