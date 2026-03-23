<template>
    <br>
    <div class="container-fluid">
  <nav aria-label="...">
    <div class="d-flex justify-content-between align-items-center">
      <b style="background-color: white; padding: 5px;">Recently Added Books</b>

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

      <!-- SEARCH BAR -->
      <div class="justify-content-end">
        <form class="d-flex err_msg" @submit.prevent="submitSearch">
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" id="book_name" v-model="searchKey" value="book_name">
            <label for="book_name">Book</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" id="sect" v-model="searchKey" value="sect">
            <label for="sect">Section</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="radio" id="authors" v-model="searchKey" value="authors">
            <label for="authors">Author</label>
          </div>
          <input class="form-control me-2" type="search" v-model="searchQuery" placeholder="Search" aria-label="Search" required>
          <button class="btn btn-success" type="submit">Search</button>
        </form>
      </div>
    </div>
  </nav>
</div>
    
    <br />
    <div class="row">

    <div class="d-flex flex-row col-10"><!-- Flash Cards -->
      <div class="container text-center">
        <div class="row">
          <div v-for="book in books" :key="book.book_id" class="col mb-4">
            <div class="card">
              <div class="card-body">
                <router-link :to="`/ShowBook/${book.book_id}`">
                  <img
                    :src="`/book_files/${book.book_id}.jpg`"
                    height="320"
                    class="card-img-top"
                    alt="BOOK FILE NOT FOUND"
                  />
                  <div class="change">
                    <br />
                    <p><b>Section:</b> {{ book.sect }}</p>
                    <p><b>Book ID:</b> {{ book.book_id }}</p>
                    <p><b>Author(s):</b> {{ book.authors }}</p>
                    <p><b>Avg. Rating:</b> {{ book.avg_rating }}</p>
                    <p><b>Pages:</b> {{ book.pages }}</p>
                    <p><b>Added on:</b> {{ book.added_on }}</p>
                  </div>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  <!-- SIDE BAR -->
  <div class="d-flex flex-column flex-shrink-0 p-3 bg-light" style="max-width: 250px; height: 325px;">
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
            <a href="#" class="nav-link active" aria-current="page">
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#speedometer2"></use></svg>
              GoTo Library
            </a>
          </li>
          <li>
            <router-link :to="`/SectionsOptions`" class="nav-link link-dark">
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#speedometer2"></use></svg>
              Sections Options
            </router-link>
          </li>
          <li>
            <router-link :to="`/PendingReturns`" class="nav-link link-dark">
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#table"></use></svg>
              Pending Returns
            </router-link>
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
import axios from "../axiosConfig";

export default {
  name: "GotoLibrary",
  data() {
    return {
      books: [],
      pagination: {
        page: 1,
        total_pages: 1,
        has_next: false,
        has_prev: false,
        next_num: null,
        prev_num: null,
      },
      pages: [],
      searchKey: 'all',
      searchQuery: null,
    };
  },
  methods: {
    fetchBooks(page = 1) {
      axios.get(`/logged_in/?page=${page}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem("adm_token")}` },
        })
        .then((response) => {
          this.books = response.data.books;
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
        .catch((error) => {
          console.error("Error fetching books:", error);
        });
    },

    changePage(page) {
      if (page && page !== this.pagination.page) {
        this.fetchBooks(page);
      }
    },

    updatePages() {
      const pages = [];
      for (let i = 1; i <= this.pagination.total_pages; i++)
      {  pages.push(i);  }
      this.pages = pages;
    },

    async submitSearch() {
      await axios.get(`/search/${this.searchKey}/${this.searchQuery}`)
      .then((response) => { this.books = response.data.books; })
      .catch((error) => console.log("Error searching book:", error))
      },

    logout() {
      localStorage.removeItem("adm_token");
      delete axios.defaults.headers.common["Authorization"];
      this.$router.push("/");
    },

    async statisticsPage() {
      try {
        await axios.get('/statistics');
        this.$router.push({
          name: 'StatisticsHome'
        })
      } catch (error) {
        console.error('Error Pushing to Statistics:', error);
      }
    },
  },

  created() {
    this.fetchBooks();
  },
  
  mounted() {
    let adm_logged = localStorage.getItem("adm_token");
    if (!adm_logged) { this.$router.push("/"); }
  },
};
</script>

<style scoped>
.card {
  width: 18rem;
  height: 350px;
}
.card-body .change {
  margin-top: 1rem;
}
.change {
  display: none;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 95%;
  background-color: rgba(255, 255, 255, 0.9);
  border: 1px solid #ccc;
  color: black;
}
.card:hover .change {
  display: block;
}
</style>
