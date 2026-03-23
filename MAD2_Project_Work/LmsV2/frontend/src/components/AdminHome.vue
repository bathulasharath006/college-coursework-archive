<template>
  <h1 class="err_msg">Library Management System</h1><br>
  <ul class="nav nav-pills nav-fill">
    <div class="container-fluid text-center">
    <div class="row">
      <div class="col-sm custom-col" style="background-color:#FFB5C5">
        <h5>Student</h5>
        <div class="button-group">

    <li class="nav-item">
      <!-- STUDENT REGISTER BUTTON -->
      <button @click="toggleForm('studentRegisterForm')" type="button" class="btn btn-primary">Register</button>

      <!-- Register Student Form -->
      <div v-if="isFormVisible.studentRegisterForm" class="overlay" @click="toggleForm('studentRegisterForm')">
        <div class="form-container" @click.stop>
          <form @submit.prevent="registerStudent">
            <h3>+ Register Student</h3>
            <div>
              <label for="email">Email:</label>
              <input type="email" id="email" v-model="student.email" placeholder="e.g. abc@gmail.com" required />
            </div>
            <div>
              <label for="full_name">Full Name:</label>
              <input type="text" id="full_name" v-model="student.full_name" placeholder="e.g. Dennis Ritchie" required />
            </div>
            <div>
              <label for="number">Mobile Number:</label>
              <input type="text" id="number" v-model="student.number" pattern="\d{10}" placeholder="Please enter a 10-digit number." required />
            </div>
            <div>
              <label for="create_password">Create Password:</label>
              <input type="password" id="create_password" v-model="student.create_password" pattern=".{8,}" placeholder="Password must be at least 8 characters" required />
            </div>
            <div>
              <label for="confirm_password">Confirm Password:</label>
              <input type="password" id="confirm_password" v-model="student.confirm_password" pattern=".{8,}" placeholder="Re-enter Password" required />
            </div>
            <div>
              <label for="key">Secret Key:</label>
              <input type="text" id="key" v-model="student.key" pattern="\d{6}" placeholder="Key for Password Recovery e.g. 123456" required />
            </div>
            <div>
              <input type="submit" value="Create Account" style="background-color: #008000" @click="matchPassword"/>
            </div>
          </form>
        </div>
      </div>
  </li>
  
  <li class="nav-item">
  <!-- STUDENT UPDATE BUTTON -->
  <button @click="toggleForm('studentUpdateForm')" type="button" class="btn btn-primary">Update</button>

  <!-- Update Student Form -->
  <div v-if="isFormVisible.studentUpdateForm" class="overlay" @click="toggleForm('studentUpdateForm')">
    <div class="form-container" @click.stop>
      <form @submit.prevent="updateStudent">
        <h3>Update Student Info</h3><br>
        <div>
          <input type="email" v-model="student.email" placeholder="Student Email ID" required />
          <input type="submit" value="Get Details" />
        </div>
      </form>
    </div>
  </div>
</li>
  
<li class="nav-item">
	<!-- STUDENT DELETE BUTTON -->
  <button @click="toggleForm('studentDeleteForm')" type="button" class="btn btn-primary">Delete</button>

  <!-- Delete Student Form -->
  <div v-if="isFormVisible.studentDeleteForm" class="overlay" @click="toggleForm('studentDeleteForm')">
    <div class="form-container" @click.stop>
      <form @submit.prevent="deleteStudent">
        <h3>Delete Student Account</h3><br>
        <div>
          <input type="email" v-model="student.email" placeholder="Student Email ID" required />
          <input type="submit" value="Get Details" />
        </div>
      </form>
    </div>
  </div>
</li>
</div>
</div>
<div class="col-sm custom-col" style="background-color:#FFFACD">
  <h5>Librarian</h5>
  <div class="button-group">

<li class="nav-item">
	<!-- LIBRARIAN REGISTER BUTTON -->
  <button @click="toggleForm('adminRegisterForm')" type="button" class="btn btn-primary">Register</button>

<!-- Register Librarian Form -->
<div v-if="isFormVisible.adminRegisterForm" class="overlay" @click="toggleForm('adminRegisterForm')">
  <div class="form-container" @click.stop>
    <form @submit.prevent="registerAdmin">
      <h3>+ Register Librarian</h3>
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="admin.email" placeholder="e.g. abc@gmail.com" required />
      </div>
      <div>
        <label for="full_name">Full Name:</label>
        <input type="text" id="full_name" v-model="admin.full_name" placeholder="e.g. Dennis Ritchie" required />
      </div>
      <div>
        <label for="number">Mobile Number:</label>
        <input type="text" id="number" v-model="admin.number" pattern="\d{10}" placeholder="Please enter a 10-digit number." required />
      </div>
      <div>
        <label for="create_password">Create Password:</label>
        <input type="password" id="create_password" v-model="admin.create_password" pattern=".{8,}" placeholder="Password must be at least 8 characters" required />
      </div>
      <div>
        <label for="confirm_password">Confirm Password:</label>
        <input type="password" id="confirm_password" v-model="admin.confirm_password" pattern=".{8,}" placeholder="Re-enter Password" required />
      </div>
      <div>
        <label for="key">Secret Key:</label>
        <input type="text" id="key" v-model="admin.key" pattern="\d{6}" placeholder="Key for Password Recovery e.g. 123456" required />
      </div>
      <div>
        <input type="submit" value="Create Account" style="background-color: #008000" @click="matchAdminPassword" />
      </div>
    </form>
  </div>
</div>
</li>


<li class="nav-item">
  <!-- LIBRARIAN UPDATE BUTTON -->
  <button @click="toggleForm('adminUpdateForm')" type="button" class="btn btn-primary">Update</button>

  <!-- Update Librarian Form -->
  <div v-if="isFormVisible.adminUpdateForm" class="overlay" @click="toggleForm('adminUpdateForm')">
    <div class="form-container" @click.stop>
      <form @submit.prevent="updateAdmin">
        <h3>Update Librarian Info</h3><br>
        <div>
          <input type="email" v-model="admin.email" placeholder="Librarian Email ID" required />
          <input type="submit" value="Get Details" />
        </div>
      </form>
    </div>
  </div>
</li>


<li class="nav-item">
	<!-- LIBRARIAN DELETE BUTTON -->
  <button @click="toggleForm('adminDeleteForm')" type="button" class="btn btn-primary">Delete</button>

  <!-- Delete Librarian Form -->
  <div v-if="isFormVisible.adminDeleteForm" class="overlay" @click="toggleForm('adminDeleteForm')">
    <div class="form-container" @click.stop>
      <form @submit.prevent="deleteAdmin">
        <h3>Delete Librarian Account</h3><br>
        <div>
          <input type="email" v-model="admin.email" placeholder="Librarian Email ID" required />
          <input type="submit" value="Get Details" />
        </div>
      </form>
    </div>
  </div>
</li>
</div>  
</div>

<div class="col-sm custom-col" style="background-color:#FFA07A">
  <h5>Book</h5>
  <div class="button-group">

<li class="nav-item">
	<!-- ADD BOOK BUTTON -->
  <button @click="toggleForm('addBookForm')" type="button" class="btn btn-primary">Add</button>

	<!-- Add Book Form -->
  <div v-if="isFormVisible.addBookForm" class="overlay" @click="toggleForm('addBookForm')">
    <div class="form-container" @click.stop>
      <form @submit.prevent="addBook" method="POST" enctype="multipart/form-data" >
        <h3>+ Add a Book</h3>
        <div>
          <label for="sect">Section Name:</label>
          <select id="sect" v-model="book.sect" required @click="fetchSections">
            <option value="" disabled selected> Select Section </option>
            <option v-for="section in sections" :key="section.section_name" :value="section.section_name">
              {{ section.section_name }}
            </option>
          </select>
        </div>
        <div><br>
          <label for="book_id">Book ID:</label>
          <input type="text" id="book_id" v-model="book.book_id" placeholder="e.g. CS2001" required />
        </div>
        <div>
          <label for="book_name">Book Name:</label>
          <input type="text" id="book_name" v-model="book.book_name" required />
        </div>
        <div>
          <label for="authors">Author(s):</label>
          <input type="text" id="authors" v-model="book.authors" placeholder="e.g. Author1, Author2, ..." required />
        </div>
        <div>
          <label for="synopsis">Synopsis:</label>
          <input type="text" id="synopsis" v-model="book.synopsis" maxlength="1000" placeholder=" Maximum 1000 Characters ..." required />
        </div>
        <div>
          <label for="pages">Pages:</label>
          <input type="number" id="pages" v-model="book.pages" placeholder="No. of Pages in the Book" required />
        </div>
        <div>
          <label for="image">Select Cover Page:</label>
          <input type="file" id="image" @change="handleFileUpload($event, 'image')" accept="image/*" required >
        </div>
        <div>
          <label for="pdfFile">Select PDF File:</label>
          <input type="file" id="pdfFile" @change="handleFileUpload($event, 'pdfFile')" accept=".pdf" required>
        </div>
        <div>
          <input type="submit" value = "Upload">
        </div>
      </form>
    </div>
  </div>
</li>


<li class="nav-item">
	<!-- UPDATE BOOK BUTTON -->
  <button @click="toggleForm('updateBookForm')" type="button" class="btn btn-primary">Update</button>

  <!-- Update Book Form -->
  <div v-if="isFormVisible.updateBookForm" class="overlay" @click="toggleForm('updateBookForm')">
    <div class="form-container" @click.stop>
      <form @submit.prevent="updateBook">
        <h3>Update a Book</h3><br>
        <div>
          <input type="text" v-model="book.book_id" placeholder="Enter Book ID" required />
          <input type="submit" value="Get Details" />
        </div>
      </form>
    </div>
  </div>
</li>


<li class="nav-item">
	<!-- DELETE BOOK BUTTON -->
  <button @click="toggleForm('deleteBookForm')" type="button" class="btn btn-primary">Delete</button>

  <!-- Delete Book Form -->
  <div v-if="isFormVisible.deleteBookForm" class="overlay" @click="toggleForm('deleteBookForm')">
    <div class="form-container" @click.stop>
      <form @submit.prevent="deleteBook">
        <h3>Remove a Book</h3><br>
        <div>
          <input type="text" v-model="book.book_id" placeholder="Enter Book ID" required />
          <input type="submit" value="Get Details" />
        </div>
      </form>
    </div>
  </div>
</li>

</div>
    </div>
  </div>
  </div>
</ul>


    <br><h3 class="err_msg">Pending Book Requests</h3><br>
    <div class="d-flex flex-row" >
      <table class="table table-striped table-hover container" style="text-align: center; max-height: 150px; overflow: auto;" >
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Student ID</th>
            <th scope="col">Requested Book</th>
            <th scope="col">Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="requests.length === 0">
            <td colspan="4">
              <br><h2>---- 0 Pending Requests ----</h2>
            </td>
          </tr>
          <tr v-for="(request, index) in requests" :key="index">
            <th scope="row">{{ index + 1 }}</th>
            <td><router-link :to="`/StudentDetails/${request.email}`">{{ request.email }}</router-link></td>
            <td><router-link :to="`/ShowBook/${request.book_id}`">{{ request.book_id }}</router-link></td>
            <td>
              <button @click="issueBook(request.email, request.book_id)" class="btn btn-success">Issue</button> &nbsp; &nbsp;
              <button @click="rejectBook(request.email, request.book_id)" class="btn btn-danger">Reject</button>
            </td>
          </tr>
        </tbody>
      </table>


  <!-- SIDE BAR -->
      <div class="d-flex flex-column flex-shrink-0 p-3 bg-light" style="max-width: 250px; height: 325px;">
        <a href="#" class="d-flex align-items-center mb-3 mb-md-0 me-md-auto link-dark text-decoration-none">
          <svg class="bi me-2" width="40" height="32"><use xlink:href="#bootstrap"></use></svg>
          <span class="fs-4">Menu</span>
        </a>
        <hr>
        <ul class="nav nav-pills flex-column mb-auto">
          <li class="nav-item">
            <a href="#" class="nav-link active" aria-current="page">
              <svg class="bi me-2" width="16" height="16"><use xlink:href="#home"></use></svg>
              Home
            </a>
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
import axios from '../axiosConfig';

export default {
  name: 'AdminHome',
  data() {
    return {
      isFormVisible: {
        studentRegisterForm: false,
        studentUpdateForm: false,
        studentDeleteForm: false,
        adminRegisterForm: false,
        adminUpdateForm: false,
        adminDeleteForm: false,
        addBookForm: false,
        updateBookForm: false,
        deleteBookForm: false,
      },
      student: {
        email: null,
        full_name: null,
        number: null,
        create_password: null,
        confirm_password: null,
        key: null,
      },
      admin: {
        email: null,
        full_name: null,
        number: null,
        create_password: null,
        confirm_password: null,
        key: null,
      },
      book: {
        sect: '',
        book_id: null,
        book_name: null,
        authors: null,
        synopsis: null,
        pages: null,
        image: null,
        pdfFile: null,
      },
      requests: [],
      sections: [],
      sectionsFetched: false,
      error_message:null,
    }
  },
  methods: {

    async fetchRequests() {
      await axios.get('/admin_home', {
        headers: { Authorization: `Bearer ${localStorage.getItem('adm_token')}` }
      }).then(response => {  this.requests = response.data; })
      .catch(error => { console.log("There was an error fetching the requests:", error); })
    }, // End of fetchRequests

    async issueBook(mail, bk_id) {
      await axios.get(`/admin/accept_request/${mail}/${bk_id}`);
      this.fetchRequests();
    },
    async rejectBook(mail, bk_id) {
      await axios.get(`/admin/reject_request/${mail}/${bk_id}`)
      this.fetchRequests();
    },

    async registerStudent() {
        try {
            const response = await axios.post('/register', {
                email: this.student.email,
                full_name: this.student.full_name,
                number: this.student.number,
                create_password: this.student.create_password,
                confirm_password: this.student.confirm_password,
                key: this.student.key,
        });
        
        this.isFormVisible = false;
        this.$router.push({
            name: "SuccessPage",
            params: { succ_id: response.data.succ_id, }
        });
        } catch (error) {
            this.error_message = error.response.data.message
            alert(this.error_message);
        }
    }, // End of registerStudent

    updateStudent() {
      this.$router.push({
        name: 'UpdateDetails',
        params: { role: "Student", email: this.student.email }
      })
    }, // End of updateStudent

    deleteStudent() {
      this.$router.push({
        name: 'DeleteAccount',
        params: { role: "Student", email: this.student.email }
      })
    }, // End of deleteStudent

    async registerAdmin() {
          try {
              const response = await axios.post('/registerLibrarian', {
                  email: this.admin.email,
                  full_name: this.admin.full_name,
                  number: this.admin.number,
                  create_password: this.admin.create_password,
                  confirm_password: this.admin.confirm_password,
                  key: this.admin.key,
          });

          this.$router.push({
              name: "SuccessPage",
              params: { succ_id: response.data.succ_id, }
          });
      } catch (error) {
          this.error_message = error.response.data.message
          alert(this.error_message);
      }
  }, // End of registerLibrarian

  updateAdmin() {
    this.$router.push({
      name: 'UpdateDetails',
      params: { role: "Admin", email: this.admin.email}
    })
  }, // End of updateAdmin

  deleteAdmin() {
    this.$router.push({
        name: 'DeleteAccount',
        params: { role: "Admin", email: this.admin.email }
      })
  }, // End of deleteAdmin

  async addBook() {
      try {
        const formData = new FormData();
        formData.append('sect', this.book.sect);
        formData.append('book_id', this.book.book_id);
        formData.append('book_name', this.book.book_name);
        formData.append('authors', this.book.authors);
        formData.append('synopsis', this.book.synopsis);
        formData.append('pages', this.book.pages);
        formData.append('image', this.book.image);
        formData.append('pdfFile', this.book.pdfFile);

        const response = await axios.post('/admin_add_book',
        formData, { headers: { 'Content-Type': 'multipart/form-data' } } );

        if ( response.status === 201 )
        {  this.$router.push({
              name: 'SuccessPage',
              params: { succ_id: response.data.succ_id }
            });
        }
      } catch (error) {
        if ( error.response.data.error === 409 )
        {
          this.$router.push({
            name: 'AlreadyExist',
            params: { book_id: this.book.book_id }
          })
        }
        else if (error.response.data.error === 400)
        {
          this.error_message = error.response.data.message;
          alert(this.error_message);
        }
        else
        { console.log(error)}
      }
    }, // End of addBook

    async fetchSections() {
      if (!this.sectionsFetched) {
        try {
          const response = await axios.get('/getSectionDetails');
          
        this.sections = response.data.map(section => ({
          section_name: section.sect_name,
        }));
        this.sectionsFetched = true;
      } catch (error) {
        console.error('Error fetching sections:', error);
      }
    }
  },


  updateBook() {
      this.$router.push({
        name: 'UpdateBook',
        params: { book_id: this.book.book_id }
      })
    }, // End of updateBook

    deleteBook() {
      this.$router.push({
        name: 'DeleteBook',
        params: { book_id: this.book.book_id }
      })
    }, // End of deleteBook

  handleFileUpload(event, fileType) {
      const file = event.target.files[0];
      this.book[fileType] = file;
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

    logout() {
            localStorage.removeItem('adm_token');
            delete axios.defaults.headers.common['Authorization'];
            this.$router.push('/');
    },

    toggleForm(formKey) {
      this.isFormVisible[formKey] = !this.isFormVisible[formKey];
    },

  matchPassword() {
      if (this.student.create_password !== this.student.confirm_password) {
        alert("Passwords did not match");
        this.student.create_password = "";
        this.student.confirm_password = "";
      }
    },

  matchAdminPassword() {
      if (this.admin.create_password !== this.admin.confirm_password) {
        alert("Passwords did not match");
        this.admin.create_password = "";
        this.admin.confirm_password = "";
      }
    },
  },


  mounted() {
    let adm_logged = localStorage.getItem("adm_token");
    if (!adm_logged) {
      this.$router.push("/");
    }
    this.fetchRequests();
  },
};
</script>

<style scoped>
.nav-pills .nav-item {
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  margin: 0 5px;
}

.custom-col {
  border: 1px solid #e0e0e0;
  padding: 5px;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.button-group {
  display: flex;
  justify-content: space-between;
  gap: 3px;
  width: 100%;
  margin-top: 10px;
}

.button-group .btn {
  flex: 1;
  margin: 0 2px;
}

.form-container {
  background: white;
  padding: 20px;
  border-radius: 5px;
  animation: slide-down 0.5s ease-out;

  max-width: 500px;
  width: 300%;
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

input {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  box-sizing: border-box;
}

input[type="submit"] {
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