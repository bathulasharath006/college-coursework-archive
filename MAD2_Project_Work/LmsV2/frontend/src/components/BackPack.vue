<template>
    <BackButton />
    <br><br><br>
    <div class="container text-center">
      <div class="row justify-content-between">
        <div class="col-md-5 register-form">
            <form >
                <div>
                    <label><h2 class="err_msg">Student Details</h2></label>
                </div><hr>
                <div>
                    <label>Email:</label>
                    <input v-model="email" style="color: black;" disabled />
                </div>
                <div>
                    <label>Full Name:</label>
                    <input v-model="full_name" style="color: black;" disabled />
                </div>
                <div>
                    <label>Mobile Number:</label>
                    <input v-model="number" style="color: black;" disabled />
                </div>
            </form>
        </div>
        <div class="col-md-7">
            <br><h3 class="err_msg">Borrowed Books</h3><br>
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Book ID</th>
                        <th scope="col">Issue Date</th>
                        <th scope="col">Return Date</th>
                        <th scope="col">Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="booksBorrowed.length === 0">
                        <td colspan="5">
                            <h3>---- No, Books in the Back Pack ----</h3>
                        </td>
                    </tr>
                    <tr v-for="(row, index) in booksBorrowed" :key="index">
                        <th scope="row">{{ index + 1 }}</th>
                        <td><router-link :to="`/book_details/${row.book_id}`">{{ row.book_id }}</router-link></td>
                        <td> {{ row.issue_date }}  </td>
                        <td> {{ row.return_date }}  </td>
                        <td><button @click="returnBook(row.book_id)" class="btn btn-danger">Return</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    </div>
    </template>
    
    <script>
    import axios from '../axiosConfig'
    
    export default {
        name: 'BackPack',
        data() {
            return {
                email: null,
                full_name: null,
                number: null,
                userId: null,
                booksBorrowed: [],
            }
        },
        methods: {
            async fetchDetails() {
                await axios.get(`/backpack/${this.userId}`, {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                }).then(response => {
                      this.email = response.data.email;
                      this.full_name = response.data.full_name;
                      this.number = response.data.number;
                      this.booksBorrowed = response.data.backpack;
                    })
                    .catch(error => { console.log("There was an error fetching the requests:", error); })
                },
                async returnBook(bk_id) {
                    await axios.get(`/return/${this.userId}/${bk_id}/3`)
                    this.fetchDetails();
                },
        },
        mounted() {
            this.userId = localStorage.getItem('user_id');
            this.fetchDetails();
        }
    };
    </script>
    
    <style scoped>
    .register-form {
        max-width: 350px;
        margin: 0 auto;
        padding: 1em;
        border: 1px solid #ccc;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-color: #fff;
        justify-content: center;
        text-align: center;
        
    }
    
    .register-form input {
        width: calc(100% - 20px);
        padding: 10px;
        margin-bottom: 1em;
        border: 1px solid #ccc;
        border-radius: 5px;
        font-size: 1em;
    }
    </style>