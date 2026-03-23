<template>
    <div class="container">
      <BackButton />
      <div class="row">
        <h2 v-if="error_message" class="err_msg">{{ error_message }}</h2>
      <!-- GET Details Form -->

      <div class="col-md-6">
      <form class="getDetails"  @submit.prevent="GetDetails">
        <div>
          <input type="email" v-model="searchEmail" placeholder="Student Email ID" required />
          <input type="submit" value="Get Details" />
        </div>
      </form><br><br>
      </div>

      <div class="col-md-6">
      <form class="Data" @submit.prevent="updateDetails">
        <div>
          <label><b><h2>Update {{ role }} Info</h2></b></label>
        </div>
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
          <input type="submit" value="Update Details" style="background-color: #008000;" @click="matchPassword">
        </div>
      </form>
      </div>
    </div>
    </div>
</template>
  
<script>
import axios from '../axiosConfig';
  
export default {
  name: 'UpdateDetails',
  data() {
      return {
          searchEmail: null,
          email: null,
          full_name: null,
          number: null,
          create_password: null,
          confirm_password: null,
          key: null,
          role: null,
          error_message:null,
      }
  },
  mounted() {
      this.role = this.$route.params.role;
      this.searchEmail = this.$route.params.email;
      this.GetDetails();
  },
  methods: {
      async GetDetails() {
          try { let response;
                if ( this.role === "Student")
                   { response = await axios.get(`/update_student_details/${this.searchEmail}`); }
                else 
                   { response = await axios.get(`/update_librarian_details/${this.searchEmail}`); }
                
                this.email = response.data.email;
                this.full_name = response.data.full_name;
                this.number = response.data.number;
                this.error_message = null;
          } catch(error) {
              this.error_message = error.response.data.message;
              this.email = null;
              this.full_name = null;
              this.number = null;
              this.create_password = null;
              this.confirm_password = null;
              this.key = null;
          }
      },
      async updateDetails() {
          try {
              let response;
              if (this.role === "Student") {
                response = await axios.put(`/update_student_details/${this.email}`, {
                  email: this.email,
                  full_name: this.full_name,
                  number: this.number,
                  create_password: this.create_password,
                  confirm_password: this.confirm_password,
                  key: this.key
                });
              } else if (this.role === "Admin") {
                response = await axios.put(`/update_librarian_details/${this.email}`, {
                  email: this.email,
                  full_name: this.full_name,
                  number: this.number,
                  create_password: this.create_password,
                  confirm_password: this.confirm_password,
                  key: this.key
                });
              }

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
.container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
}

form {
  width: 300px;
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
  background-color: #1E90FF;
  color: white;
  cursor: pointer;
}
</style>