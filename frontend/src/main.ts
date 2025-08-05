import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from '@/router/index'
// import pinia from '@/stores/index'

import pinia from '@/stores'
import { useSidebarStore } from '@/stores/sidebar'

const app = createApp(App)

app.use(pinia);
app.use(router);


app.mount('#app')

const sidebarStore = useSidebarStore()
sidebarStore.initialize()