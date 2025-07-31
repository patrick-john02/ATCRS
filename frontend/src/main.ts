import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from '@/router/index'
import pinia from '@/stores/index'

const app = createApp(App)

app.use(pinia);
app.use(router);


app.mount('#app')