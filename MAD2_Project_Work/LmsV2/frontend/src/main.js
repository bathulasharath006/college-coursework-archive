import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

import { createApp } from 'vue';
import App from './App.vue';
import router from './router';


import BackButton from './components/BackButton.vue';

const app = createApp(App);

app.component('BackButton', BackButton);

app.use(router);
app.mount('#app');
