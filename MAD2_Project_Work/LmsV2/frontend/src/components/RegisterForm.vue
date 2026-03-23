<template>
    <br><br> <h3 v-if="error_message"  class="err_msg">{{ error_message }}</h3> <br><br>
    <BackButton />
    <div class="register-form">
        <form @submit.prevent="register">

            <h1>Registration Form</h1><br>
            <div>
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="details.email" placeholder="e.g. abc@gmail.com" required />
            </div>

            <div>
                <label for="full_name">Full Name:</label>
                <input type="text" id="full_name" v-model="details.full_name" placeholder="e.g. Dennis Ritchie" required />
            </div>

            <div>
                <label for="number">Mobile Number:</label>
                <input type="text" id="number" v-model="details.number" pattern="\d{10}" placeholder="Please enter a 10-digit number." required />
            </div>

            <div>
                <label for="create_password">Create Password:</label>
                <input type="password" id="create_password" v-model="details.create_password" pattern=".{8,}" placeholder="Password must be at least 8 characters" required />
            </div>

            <div>
                <label for="confirm_password">Confirm Password:</label>
                <input type="password" id="confirm_password" v-model="details.confirm_password" pattern=".{8,}" placeholder="Re-enter Password" required />
            </div>

            <div>
                <label for="key">Secret Key:</label>
                <input type="text" id="key" v-model="details.key" pattern="\d{6}" placeholder="Key for Password Recovery e.g. 123456" required />
            </div>

            <button type="submit" class="btn btn-success" @click="matchPassword">Create Account</button>
        </form>
    </div>
</template>

<script>
import axios from '../axiosConfig';

export default {
    name: 'RegisterForm',
    data() {
        return {
            details:{
                email: null,
                full_name: null,
                number: null,
                create_password: null,
                confirm_password: null,
                key: null,
            },
            error_message:null,
        }
    },
    methods: {
        async register() {
            try {
                const response = await axios.post('/register', {
                    email: this.details.email,
                    full_name: this.details.full_name,
                    number: this.details.number,
                    create_password: this.details.create_password,
                    confirm_password: this.details.confirm_password,
                    key: this.details.key,
            });

            this.$router.push({
                name: 'SuccessPage',
                params: { succ_id: response.data.succ_id, }
            });
        } catch (error) {
            this.error_message = error.response.data.message
        }
    },
    matchPassword() {
      if (this.details.create_password !== this.details.confirm_password) {
        alert("Passwords did not match");
        this.details.create_password = '';
        this.details.confirm_password = '';
      }
    }
    },
}
</script>

<style scoped>
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

.register-form input {
    width: calc(100% - 20px);
    padding: 10px;
    margin-bottom: 1em;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 1em;
}

</style>