<template>
    <br><br><br>
    <div class="d-flex flex-row">
        <div class="container text-center">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col"></th>
                        <th scope="col"></th>
                        <th scope="col"></th>
                        <th scope="col"><h3>Pending Returns</h3></th>
                        <th scope="col"></th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <thead>
                    <tr>
                    <th scope="col">#</th>
                    <th scope="col">Email ID</th>      
                    <th scope="col">Book ID</th>
                    <th scope="col">Issued Date</th>
                    <th scope="col">Return Date</th>
                    <th scope="col">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="entries.length === 0">
                        <td colspan="6">
                            <h3>---- 0 Books Borrowed ----</h3>
                        </td>
                    </tr>
                    <tr  v-for="(row, index) in entries" :key="index">
                        <th scope="row">{{ index + 1 }}</th>
                        <td><router-link :to="`/StudentDetails/${row.email}`">{{ row.email }}</router-link></td>
                        <td><router-link :to="`/ShowBook/${row.book_id}`">{{ row.book_id }}</router-link></td>
                        <td> {{ row.issue_date }}  </td>
                        <td> {{ row.return_date }}  </td>
                        <td><button @click="revokeAccess(row.email, row.book_id)" class="btn btn-danger">Revoke Access</button></td>
                    </tr>
                </tbody>
            </table>
        </div>


  <!-- SIDE BAR -->
  <div class="d-flex flex-column flex-shrink-0 p-3 bg-light" style="max-width: 250px; height: 335px;">
        <a href="#" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-dark text-decoration-none">
          <svg class="bi me-2" width="40" height="32"><use xlink:href="#bootstrap"></use></svg>
          <span class="fs-4">Menu</span>
        </a>
        <hr>
        <ul class="nav nav-pills flex-column mb-auto">
          <li class="nav-item">
            <router-link :to="`/admin_home`" class="nav-link link-dark">
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#home"></use></svg>
              Home
            </router-link>
          </li>
          <li>
            <router-link :to="`/GotoLibrary`" class="nav-link link-dark">
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#speedometer2"></use></svg>
              GoTo Library
            </router-link>
          </li>
          <li>
            <router-link :to="`/SectionsOptions`" class="nav-link link-dark">
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#speedometer2"></use></svg>
              Sections Options
            </router-link>
          </li>
          <li>
            <a href="#" class="nav-link active" aria-current="page">
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#speedometer2"></use></svg>
              Pending Returns
            </a>
          </li>
          <li>
            <a @click.prevent="statisticsPage" href="#" class="nav-link link-dark">
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#grid"></use></svg>
              Statistics
            </a>
          </li>
          <li>
            <a @click.prevent="logout" href="#" class="nav-link link-dark">
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#people-circle"></use></svg>
              Sign Out
            </a>
          </li>
        </ul>
        <hr>
      </div>

</div>
</template>

<script>
import axios from '../axiosConfig';

export default {
    name: 'PendingReturns',
    data() {
        return {
            entries: [],
        }
    },
    methods: {
        async fetchDetails() {
            await axios.get('/admin/pending_returns', {
                headers: { Authorization: `Bearer ${localStorage.getItem('adm_token')}` }
            }).then(response => {  this.entries = response.data;  })
            .catch(error => { console.log("There was an error fetching the requests:", error); })
        },

        async revokeAccess(mail, bk_id) {
            await axios.get(`/admin/revoke/${mail}/${bk_id}`)
            this.fetchDetails();
        },

        async statisticsPage() {
          try {
            await axios.get('/statistics');
            this.$router.push({
              name: 'StatisticsHome'
            })
          } catch (error) { console.error('Error Pushing to Statistics:', error); }
        },

        logout() {
            localStorage.removeItem('adm_token');
            delete axios.defaults.headers.common['Authorization'];
            this.$router.push('/');
        },
    },
    mounted() { this.fetchDetails(); },
}
</script>