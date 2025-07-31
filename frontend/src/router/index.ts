import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/pages/LandingPage.vue'),
    },
    {
      path: '/login',
      component: () => import('@/pages/auth/Login.vue'),
    },
    {
      path: '/forgot-password',
      component: () => import('@/pages/auth/ForgotPassword.vue'),
    },
    {
      path: '/admin/dashboard',
      component: () => import('@/pages/admin/Dashboard.vue'),
    },
    {
      path: '/student/dashboard',
      component: () => import('@/pages/student/Dashboard.vue'),
    },
    {
      path: '/superadmin/dashboard',
      component: () => import('@/pages/superAdmin/Dashboard.vue'),
    },
  ],
});

export default router;
