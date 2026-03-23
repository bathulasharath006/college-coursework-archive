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
          <router-link :to="`/StatisticsSect`" class="btn btn-success" > Sections 
          </router-link>
        </li>
        <li class="nav-item">
          <a class="btn btn-primary" > Transactions </a>
        </li>
      </ul><br>

      <!-- PAGINATION LINKS -->
      <ul class="pagination justify-content-center mb-0">
        <li :class="['page-item', { disabled: !pagination.has_prev }]">
          <a class="page-link"
            @click.prevent="changePage(pagination.prev_num)"
            :disabled="!pagination.has_prev">Previous</a>
        </li>

        <li v-for="page_num in pages" :key="page_num" class="page-item">
          <template v-if="page_num">
            <a href="#"
              v-if="page_num !== pagination.page"
              class="page-link"
              @click.prevent="changePage(page_num)"
              >{{ page_num }}</a
            >
            <a v-else class="page-link current active">{{ page_num }}</a>
          </template>
          <template v-else>
            <span class="ellipsis">...</span>
          </template>
        </li>

        <li :class="['page-item', { disabled: !pagination.has_next }]">
          <a
            class="page-link"
            @click.prevent="changePage(pagination.next_num)"
            :disabled="!pagination.has_next"
            >Next</a
          >
        </li>
      </ul>

<div class="container text-center">
<br>
<div class="row justify-content-between">
    <table class="table table-striped">
        <thead>
            <tr>
            <th scope="col">#</th>
            <th scope="col">Email ID</th>      
            <th scope="col">Book ID</th>
            <th scope="col">Action</th>
            <th scope="col">Issued Date</th>
            <th scope="col">Return Date</th>
            </tr>
        </thead>
        <tbody>
            <tr  v-for="row in entries" :key="row.id">
                <th scope="row">{{ row.id }}</th>
                <td>{{ row.email }}</td>
                <td>{{ row.book_id }}</td>
                <td>{{ row.action }}</td>
                <td>{{ row.issue_date }}</td>
                <td>{{ row.return_date }}</td>
            </tr>
        </tbody>
    </table>
</div>

<div>
    <button class="btn btn-warning" @click="triggerExport">Export CSV </button>  &emsp;
    <div class="err_msg" v-if="status === 'Processing'">Processing...</div>
      <a class="btn btn-primary" v-if="status === 'Success'" :href="downloadUrl" download="transactions.csv">Download CSV</a>
    <div class="err_msg" v-if="status === 'Failed'">Failed to generate the CSV. Please try again.</div>
</div>
<br>
</div>
</template>

<script>
import axios from '../axiosConfig';

export default {
    name:'TransActions',
    data() {
        return {
            entries: [],
            pagination: {
                page: 1,
                total_pages: 1,
                has_next: false,
                has_prev: false,
                next_num: null,
                prev_num: null,
            },
            pages: [],
            status: '',
            downloadUrl: ''
        }
    },
    methods: {
        async fetchData(page=1) {
            await axios.get(`/transactions/?page=${page}`, {
                headers: { Authorization: `Bearer ${localStorage.getItem("adm_token")}` },
            })
            .then(response => {
                this.entries = response.data.entries;
                this.pagination = {
                  page: response.data.page,
                  total_pages: response.data.total_pages,
                  has_next: response.data.has_next,
                  has_prev: response.data.has_prev,
                  next_num: response.data.next_num,
                  prev_num: response.data.prev_num,
                };
                this.updatePages();
            })
            .catch(error => console.error("Error fetching Data:", error))
        },
        changePage(page) {
          if (page && page !== this.pagination.page) {
            this.fetchData(page);
          }
        },
        updatePages() {
          const pages = [];
          for (let i = 1; i <= this.pagination.total_pages; i++) {
            pages.push(i);
          }
          this.pages = pages;
        },

        async triggerExport() {
          this.status = 'Processing';
          try {
            const response = await axios.post('/export_csv');
            const data = response.data;
            this.pollTask(data.task_id);
          } catch (error) {
            console.error('Error triggering export:', error);
            this.status = 'Failed';
          }
        },
        
        async pollTask(taskId) {
          const interval = setInterval(async () => {
            try {
              const response = await axios.get(`/get_csv/${taskId}`);
              const data = response.data;
                  if (data.status === 'Success') {
                    this.status = 'Success';
                    this.downloadUrl = data.file_url; 
                    clearInterval(interval);
                    alert('CSV Export is complete. You can now download the file.');
                  } else if (data.status === 'Failed') {
                    this.status = 'Failed';
                    clearInterval(interval);
                    alert('Failed to generate the CSV. Please try again.');
                  }
                } catch (error) {
                  console.error('Error polling task:', error);
                  this.status = 'Failed';
                  clearInterval(interval);
                }
          }, 5000); // Poll every 5 seconds
        },

        goBack() { this.$router.push('/admin_home'); },
    },
    mounted() { this.fetchData(); },
};
</script>

<style scoped>
.go-back-button {
    position: absolute;
    top: 10px;
    right: 10px;
  }
</style>