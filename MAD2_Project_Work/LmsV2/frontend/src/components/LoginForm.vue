<template>
    <br><br><br><br><br><br><h2 v-if="error_message" class="err_msg">{{ error_message }}</h2><br><br>

    <div v-if="!isFormVisible.AdminForm" class="login-form">
        <h2>Student Login</h2><br>
        <input type="email" v-model="loginData.email" placeholder="Enter User Mail Id" required />
        <input type="password" v-model="loginData.password" pattern=".{8,}" placeholder="Enter Password" required />
        <button @click.prevent="getCredentials" class="btn btn-primary">Login</button>
        <br><hr>
        <router-link to="/registerForm">
            <button class="btn btn-success">SignUp</button>
        </router-link>    
    </div>

    <button class="open-button btn btn-danger" @click="toggleForm('AdminForm')">Librarian Login</button>

    <div v-if="isFormVisible.AdminForm" class="login-form" >
        <h2>Librarian Login</h2><br>
        <input type="email" v-model="loginData.adm_email" placeholder="Enter Email" required />
        <input type="password" v-model="loginData.adm_password" placeholder="Enter Password" required />
        
        <button @click="getAdminCredentials" class="btn btn-primary" >Login</button> <br><hr>
        <button @click="toggleForm('AdminForm')" class="btn btn-danger" >Close</button>
    </div>
</template>


<script>
import axios from '../axiosConfig';

export default {
    name: 'LoginForm',
    data() {
        return {
            loginData: {
                email: null,
                password: null,
                adm_email: null,
                adm_password: null,
            },
            error_message:null,
            isFormVisible: { AdminForm: false, },
        }
    },
    methods: {
        toggleForm(formKey) {
            this.isFormVisible[formKey] = !this.isFormVisible[formKey];
        },
        async getCredentials() { // for normal user login
            try {
                const response = await axios.post('/login', {
                    email: this.loginData.email,
                    password: this.loginData.password,
            });
            const token = response.data.access_token;
            const user_id = response.data.id;
            localStorage.setItem('token', token);
            localStorage.setItem('user_id', user_id);
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            this.$router.push('/dashboard');
            } catch (error) {
                this.error_message = error.response.data.message;
                this.loginData.email=null;
                this.loginData.password=null;
            }
        },
        async getAdminCredentials() { // for librarian login
            try {
                const response = await axios.post('/adm_login', {
                    email: this.loginData.adm_email,
                    password: this.loginData.adm_password, });
            const token = response.data.access_token;
            localStorage.setItem('adm_token', token);
            axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            this.$router.push('/admin_home');
            } catch (error) {
                this.error_message = error.response.data.message;
                this.loginData.adm_email=null;
                this.loginData.adm_password=null;
        }
    },
    },
    mounted()
    {
        let logged = localStorage.getItem('token');
        if ( logged)
        {
            this.$router.push('/dashboard');
        }
    }
}
</script>

<style scoped>
.login-form {
    max-width: 400px;
    margin: 0 auto;
    padding: 2em;
    border: 1px solid #ccc;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #fff;
    justify-content: center;
    text-align: center;
    
}

.login-form input[type="email"],
.login-form input[type="password"] {
    width: calc(100% - 20px);
    padding: 10px;
    margin-bottom: 1em;
    border: 1px solid #ccc;
    border-radius: 5px;
    font-size: 1em;
}

.login-form .forgot-password {
    display: block;
    margin-bottom: 1em;
    color: #007bff;
    text-decoration: underline;
    font-size: 0.9em;
}

/*  Begin: Admin Login-Form Style Settings  */
.open-button {
	position: fixed;
	top: 10px;
	right: 10px;
    }

/* The popup form - hidden by default 
.form-popup {
  display: none;
  position: fixed;
  top: 60px;
  right: 45px;
}*/

</style>