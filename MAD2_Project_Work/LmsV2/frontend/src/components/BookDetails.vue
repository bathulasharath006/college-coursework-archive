<template>
    <div>
      <br>
      <br><BackButton />
      <div class="container" v-if="book">
        <div class="row">
          <div class="col-md-7 ">
            <template v-if="backpack.includes(book_id)">
              <div class="pdf-container">
                <iframe class="pdf" :src="`/book_files/${book_id}.pdf`" alt="PDF FILE NOT FOUND"></iframe>
              </div>
            </template>
            <template v-else>
              <div class="img-container">
                <img :src="`/book_files/${book_id}.jpg`" alt="BOOK IMAGE NOT FOUND" >
              </div>
            </template>
          </div>
          <div class="col-md-5">
            <div class="card">
              <div class="card-body">
                <h3 class="card-title">Highlights</h3>
                <p><b>Section:</b> {{ book.sect }}</p>
                <p><b>Book ID:</b> {{ book.book_id }}</p>
                <p><b>Book Name:</b></p> <h4>{{ book.book_name }}</h4>
                <p><b>Author(s):</b> {{ book.authors }}</p>
                <p><b>Synopsis:</b><br><br>{{ book.synopsis }}</p>
                <p><b>Avg. Rating:</b> {{ book.avg_rating }}</p>
                <p><b>Pages:</b> {{ book.pages }}</p>
                <p><b>Added on:</b> {{ book.added_on }}</p>

                <div v-if="!isFormVisible.RatingForm" >
                <template v-if="!backpack.includes(book.book_id) && !requests.includes(book.book_id) && limit < 5">
                  <a @click.prevent="requestBook" class="btn btn-primary">Request Access</a>
                </template>
                <template v-else-if="requests.includes(book.book_id)">
                  <a class="btn btn-warning">Pending Request</a>
                </template>
                <template v-else-if="backpack.includes(book.book_id)">
                  <button class="btn btn-success">Request Accepted</button> Book is accessible now
                  <span class="button-space"></span>
                  <button @click="toggleForm('RatingForm')" class="btn btn-danger">Return</button>
                </template>
                <template v-else-if="limit >= 5">
                  <button class="btn btn-danger">You Reached Limit</button><span class="button-space"></span>You can't request more books.
                </template>
              </div>

                <div v-if="isFormVisible.RatingForm" >
                  <form @submit.prevent="submitRating">
                    <h4>Please Rate this Book:</h4>
                    <div class="d-flex rating-group">
                      <label><input type="radio" value="1" v-model="rating"> 1 </label>
                      <label><input type="radio" value="2" v-model="rating"> 2 </label>
                      <label><input type="radio" value="3" v-model="rating"> 3 </label>
                      <label><input type="radio" value="4" v-model="rating"> 4 </label>
                      <label><input type="radio" value="5" v-model="rating"> 5 </label>
                    </div>
                    <br>
                    <div class="d-flex">
                    <button type="submit" class="btn btn-success">Submit</button>
                    <span class="button-space"></span>
                    <button class="btn btn-danger" @click="toggleForm('RatingForm')">Close</button><br>
                  </div>
                  </form>
                </div>

              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '../axiosConfig';
  
  export default {
    name: 'BookDetails',
    data() {
      return {
        isFormVisible: { RatingForm: false, },
        userId: null,
        book_id: null,
        book: null,
        backpack: [],
        requests: [],
        limit: 0,
        showRatingForm: false,
        rating: 3,
      };
    },
    methods: {
        toggleForm(formKey) {
        this.isFormVisible[formKey] = !this.isFormVisible[formKey];
      },
      async fetchBookDetails() {
        await axios.get(`/book_details/${this.userId}/${this.book_id}`)
          .then(response => {
            const data = response.data;
            this.book = data.book;
            this.backpack = data.backpack;
            this.requests = data.requests;
            this.limit = data.limit;
          })
          .catch(error => {
            console.error("Error fetching book details:", error);
          });
      },
      requestBook() {
        axios.get(`/requesting/${this.userId}/${this.book_id}`)
        .then(response => {
            const data = response.data;
            this.book = data.book;
            this.backpack = data.backpack;
            this.requests = data.requests;
            this.limit = data.limit;
          })
          .catch(error => {
            console.error("Error requesting book:", error);
          });
        },
        async submitRating() {
          await axios.get(`/return/${this.userId}/${this.book_id}/${this.rating}`)
          this.toggleForm('RatingForm');
          this.fetchBookDetails();
        }
      },
      mounted() {
      this.book_id = this.$route.params.book_id;
      this.userId = localStorage.getItem('user_id');
      this.fetchBookDetails();
    }

    };
  </script>
  
<style scoped>
  .button-space {
    margin-right: 20px;
  }
  
  .pdf-container {
  width: 100%;
  height: 0;
  padding-bottom: 113.33%; /* 850px / 750px = 1.1333 */
  position: relative;
  }

.pdf-container iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 0;
}

.img-container {
  width: 100%;
  height: 0;
  padding-bottom: 113%; /* 850px / 750px = 1.1333 */
  position: relative;
}

.img-container img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

  .d-flex {
  display: flex;
  justify-content: space-between;
  }

  .rating-group {
  font-size: 22px;
  }

  </style>