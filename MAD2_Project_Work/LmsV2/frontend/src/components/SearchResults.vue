<template>
    <br>
    <div class="container-fluid">
  <nav aria-label="...">
    <div class="d-flex justify-content-between align-items-center">

      <!-- SEARCH BAR -->
      <div class="justify-content-end">
        <form @submit.prevent="submitSearch" class="d-flex err_msg" method="POST">
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
                <a href="#" @click.prevent="showBookDetails(book.book_id)">
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
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

  <!-- SIDE BAR -->
  <div class="d-flex flex-column flex-shrink-0 p-3 bg-light col-2" style="width: 250px; height: 250px;">
    <a href="#"  class="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-dark text-decoration-none">
  <svg class="bi me-2" width="40" height="32">
    <use xlink:href="#bootstrap"></use>
  </svg>
  <span class="fs-4">Home</span>
</a>
    <hr />
    <ul class="nav nav-pills flex-column mb-auto">
      <li class="nav-item">
        <a href="#" class="nav-link active" aria-current="page">
          <svg class="bi me-2" width="16" height="16">
            <use xlink:href="#home"></use>
          </svg>
          Library
        </a>
      </li>
      <li>
        <router-link :to="`/BackPack`" class="nav-link link-dark">
          <svg class="bi me-2" width="16" height="16">
            <use xlink:href="#speedometer2"></use>
          </svg>
          My BackPack
        </router-link>
      </li>
      <li>
        <a @click.prevent="logout" href="#" class="nav-link link-dark">
          <svg class="bi me-2" width="16" height="16">
            <use xlink:href="#grid"></use>
          </svg>
          Sign Out
        </a>
      </li>
    </ul>
    <hr />
  </div>
  
</div>
</template>

<script>
import axios from "../axiosConfig";

export default {
  name: "SearchResults",
  data() {
    return {
      books: [],
      searchKey: 'all',
      searchQuery: null,
    };
  },
  methods: {
    async fetchBooks( ) {
            await axios.post('/search', { searchKey: this.searchKey, searchQuery: this.searchQuery })
              .then((response) => { this.books = response.data.books; })
              .catch((error) => { console.error("Error fetching books:", error); });
    },
    showBookDetails(bookId) {
      this.$router.push({ name: "BookDetails", params: { book_id: bookId } });
    },
    async submitSearch() {
      await axios.post('/search', {
        searchKey: this.searchKey,
        searchQuery: this.searchQuery })
        .then(response => { this.books = response.data.books; })
        .catch(error => { console.error('Error:', error); });
        // this.books = response.data.books;
    },
    logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("user_id");
      delete axios.defaults.headers.common["Authorization"];
      this.$router.push("/");
    },
  },
  created() { this.fetchBooks(); },
  mounted() {
    this.searchKey = this.$route.params.searchKey;
    this.searchQuery = this.$route.params.searchQuery;
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
