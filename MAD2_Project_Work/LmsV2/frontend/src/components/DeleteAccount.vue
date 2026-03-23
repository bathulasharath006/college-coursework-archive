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
      <form class="Data" v-if="role" @submit.prevent="deleteDetails">
        <div>
          <label><b><h2>Delete {{ role }} Account</h2></b></label>
        </div>
        <div>
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="email" style="color: black;" disabled />
        </div>
  
        <div>
          <label for="full_name">Full Name:</label>
          <input type="text" id="full_name" v-model="full_name" style="color: black;" disabled />
        </div>
  
        <div>
          <label for="number">Mobile Number:</label>
          <input type="text" id="number" v-model="number" style="color: black;" disabled />
        </div>

        <div>
          <input type="submit" value="Delete Account" style="background-color: #008000;">
        </div>
      </form>
    </div>
    </div>
  </div>
</template>

<script>
import axios from '../axiosConfig';
  
export default {
  name: 'DeleteAccount',
  data() {
      return {
          searchEmail: null,
          email: null,
          full_name: null,
          number: null,
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
                   { response = await axios.get(`/delete_student_account/${this.searchEmail}`); }
                else 
                   { response = await axios.get(`/delete_librarian_details/${this.searchEmail}`); }
                
                   this.email = response.data.email;
                this.full_name = response.data.full_name;
                this.number = response.data.number;
                this.error_message = null;
          } catch(error) {
              this.error_message = error.response.data.message;
              this.email = null;
              this.full_name = null;
              this.number = null;
          }
      },
      async deleteDetails() {
        try {
              let response;
              if (this.role === "Student")
                 { response = await axios.delete(`/delete_student_account/${this.email}`); }
              else
              { response = await axios.delete(`/delete_librarian_details/${this.email}`); }

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