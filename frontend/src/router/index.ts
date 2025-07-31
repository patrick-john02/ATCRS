import { createRouter, createWebHistory } from "vue-router";
import Login from "@/pages/auth/Login.vue";
import LandingPage from "@/pages/LandingPage.vue";


const router = createRouter({
    history: createWebHistory(),
    routes:[
        {path: '/', component: LandingPage},
        {path: '/login', component: Login}

    ]
})

export default router