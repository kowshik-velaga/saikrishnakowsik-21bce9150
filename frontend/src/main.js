import { createApp } from 'vue';
import { io } from 'socket.io-client';
import App from './App.vue';

const socket = io('http://localhost:5000'); // Change to your server URL

const app = createApp(App);

app.config.globalProperties.$socket = socket;

app.mount('#app');
