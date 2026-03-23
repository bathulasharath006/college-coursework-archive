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
            <a v-else :class="['page-link', { 'current': true, 'active': !isFormVisible.studentUpdateForm }]">{{ page_num }}</a>
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
    <a href="#" @click.prevent="fetchBooks" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-dark text-decoration-none">
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
        <a @click="toggleForm('studentUpdateForm')" href="#" class="nav-link link-dark">
          <svg class="bi me-2" width="16" height="16">
            <use xlink:href="#speedometer2"></use>
          </svg>
          Update Profile
        </a>

      <!-- Student Update Form -->
      <div v-if="isFormVisible.studentUpdateForm" class="overlay" @click="toggleForm('studentUpdateForm')">
        <div class="form-container" @click.stop>
          <form @submit.prevent="updateStudent">
            <h3>Update Profile</h3>
            <div>
              <label for="email">Email:</label>
              <input type="email" id="email" v-model="email" style="color: black;" disabled />
            </div>
            <div>
              <label for="full_name">Full Name:</label>
              <input type="text" id="full_name" v-model="full_name" placeholder="e.g. Dennis Ritchie" required />
            </div>
            <div>
              <label for="number">Mobile Number:</label>
              <input type="text" id="number" v-model="number" pattern="\d{10}" placeholder="Please enter a 10-digit number." required />
            </div>
            <div>
              <label for="create_password">Create Password:</label>
              <input type="password" id="create_password" v-model="create_password" pattern=".{8,}" title="Password must be at least 8 characters" placeholder="Strong Password" required />
            </div>
            <div>
              <label for="confirm_password">Confirm Password:</label>
              <input type="password" id="confirm_password" v-model="confirm_password" pattern=".{8,}" title="Password must be at least 8 characters" placeholder="Re-enter Password" required />
            </div>
            <div>
              <label for="key">Secret Key:</label>
              <input type="text" id="key" v-model="key" pattern="\d{6}" title="Please enter a 6-digit number." placeholder="Key for Password Recovery e.g. 123456" required />
            </div>
            <div>
              <input type="submit" value="Update Details" style="background-color: #008000" @click="matchPassword"/>
            </div>
          </form>
        </div>
      </div>

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
  name: "DashboardPage",
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

      isFormVisible: { studentUpdateForm: false },
      email: null,
      full_name: null,
      number: null,
      create_password: null,
      confirm_password: null,
      key: null,
      userId:null,
    };
  },
  methods: {
    async fetchBooks(page = 1) {
      this.searchKey = 'all',
      this.searchQuery = null,
            await axios.get(`/logged_in/?page=${page}`, {
                  headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
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
    showBookDetails(bookId) {
      this.$router.push({ name: "BookDetails", params: { book_id: bookId } });
    },
    changePage(page) {
      if (page && page !== this.pagination.page) {
        this.fetchBooks(page);
      }
    },
    updatePages() {
      const pages = [];
      for (let i = 1; i <= this.pagination.total_pages; i++) {
        pages.push(i);
      }
      this.pages = pages;
    },
    async submitSearch() {
      await axios.get(`/search/${this.searchKey}/${this.searchQuery}`)
      .then((response) => { this.books = response.data.books; })
      .catch((error) => console.log("Error searching book:", error))
      },
      toggleForm(formKey) {
        this.isFormVisible[formKey] = !this.isFormVisible[formKey];
      },
    async updateStudent() {
        if (this.email) {
          try {
            await axios.put(`/update_student_details/${this.email}`, {
              email: this.email,
              full_name: this.full_name,
              number: this.number,
              create_password: this.create_password,
              confirm_password: this.confirm_password,
              key: this.key
            });
            this.toggleForm('studentUpdateForm');
            alert("Profile Updated Successfully");
            this.create_password = null,
            this.confirm_password = null,
            this.key = null
          } catch (error) { console.log("Error in updating: ", error);}        
        } else {
          await axios.get(`/backpack/${this.userId}`, {
            headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
            }).then(response => {
              this.email = response.data.email;
              this.full_name = response.data.full_name;
              this.number = response.data.number;
            })
        }
      },
      matchPassword() {
        if (this.create_password !== this.confirm_password) {
          alert("Passwords did not match");
          this.create_password = '';
          this.confirm_password = '';
        }
      },
      logout() {
      localStorage.removeItem("token");
      localStorage.removeItem("user_id");
      delete axios.defaults.headers.common["Authorization"];
      this.$router.push("/");
    },
  },
  mounted() {
    let logged = localStorage.getItem("token");
    this.userId = localStorage.getItem('user_id');
    if (!logged) {
      this.$router.push("/");
    }
    this.fetchBooks();
    this.updateStudent();
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
.form-container {
  background: white;
  padding: 20px;
  border-radius: 5px;
  animation: slide-down 0.5s ease-out;

  max-width: 400px;
  width: 100%;
  margin: 0 auto;
  padding: 1em;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  justify-content: center;
  text-align: center;
}

form {
  width: 100%;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

label {
  display: block;
  margin-bottom: 10px;
}

.form-container input {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  box-sizing: border-box;
}

.form-container input[type="submit"] {
  background-color: #1e90ff;
  color: white;
  cursor: pointer;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

@keyframes slide-down {
  from {
    transform: translateY(-100%);
  }
  to {
    transform: translateY(0);
  }
}

</style>
