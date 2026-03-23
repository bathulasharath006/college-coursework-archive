<template>
    <div>
      <BackButton />
  
      <form @submit.prevent="fetchBookDetails">
        <div style="display: inline-flex;">
          <input type="text" v-model="searchBook_id" placeholder="Enter Book ID" required />&emsp;
          <input type="submit" value="Get Details" />
        </div>
      </form>
  
      <h3 v-if="error_message" class="err_msg">{{ error_message }}</h3><br>
      <div class="container">
        <div class="row">
          <div class="col-md-7">
            <iframe class="iframe-container" :src="`/book_files/${book_id}.pdf`" frameborder="0" alt="PDF FILE NOT FOUND"></iframe>
          </div>
          <div class="col-md-5">
            <form class="register-form" @submit.prevent="deleteBook">
              <div>
                <label for="book_id">Book ID:</label>
                <input type="text" id="book_id" v-model="book_id" placeholder="Unique Book id" style="color: black;" disabled />
              </div>
              <div>
                <label for="added_on">Added On:</label>
                <input type="text" id="added_on" v-model="added_on" placeholder="Date in yyyy-mm-dd" style="color: black;" disabled />
              </div>
              <div>
                <label for="sect">Section Name:</label>
                <input type="text" id="sect" v-model="sect" placeholder="e.g. Department Name" style="color: black;" disabled />
              </div>
              <div>
                <label for="book_name">Book Name:</label>
                <input type="text" id="book_name" v-model="book_name" placeholder="The Linux Commmand Line" style="color: black;" disabled />
              </div>
              <div>
                <label for="authors">Author(s):</label>
                <input type="text" id="authors" v-model="authors" placeholder="e.g. Author1, Author2, ..." style="color: black;" disabled />
              </div>
              <div>
                <label for="synopsis">Synopsis:</label>
                <textarea style="width: 100%; color: black;" type="text" id="synopsis" v-model="synopsis" maxlength="1000" placeholder=" Maximum 1000 Characters ..." disabled/>
              </div>
              <div>
                <label for="pages">Pages:</label>
                <input type="number" id="pages" v-model="pages" placeholder="No. of Pages in the Book" style="color: black;" disabled />
              </div>
              <div>
                <input type="submit" value="Delete">
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
    
<script>
import axios from '../axiosConfig';
    
export default {
  name: 'DeleteBook',
  data() {
    return {
      book_id: null,
      added_on: null,
      sect: null,
      book_name: null,
      authors: null,
      synopsis: null,
      pages: null,
      searchBook_id: null,
      error_message:null,
    };
  },
  mounted() {
    this.searchBook_id = this.$route.params.book_id;
    this.fetchBookDetails();
  },
  methods: {
    async fetchBookDetails() {
      try {
        await axios.get(`/admin_delete_book/${this.searchBook_id}`)
        .then(response => {
          const data = response.data;
          this.book_id = data.book_id;
          this.added_on = data.added_on;
          this.sect = data.sect;
          this.book_name = data.book_name;
          this.authors = data.authors;
          this.synopsis = data.synopsis;
          this.pages = data.pages;
          this.error_message = null;
        });
      } catch(error) {
      this.error_message = error.response.data.message;
          this.book_id = null;
          this.added_on = null;
          this.sect = null;
          this.book_name = null;
          this.authors = null;
          this.synopsis = null;
          this.pages = null;
        }
    },
    async deleteBook() {
      try {
        const response = await axios.delete(`/admin_delete_book/${this.book_id}`);

            this.$router.push({
              name: 'SuccessPage',
              params: { succ_id: response.data.succ_id }
            });
        } catch(error) {
            this.error_message = error.response.data.message;
          }
    }
  }
};
</script>
    
<style scoped>
.iframe-container {
  position: relative;
  width: 100%;
  height: 110%;
}

.register-form {
    max-width: 450px;
    margin: 0 auto;
    padding: 1em;
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #fff;
    justify-content: center;
    text-align: center;
    
}

input {
    width: calc(100% - 20px);
    padding: 10px;
    margin-bottom: 1em;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 1em;
}
  
input[type="submit"] {
      background-color: #108b40;
      color: white;
      cursor: pointer;
}
</style>