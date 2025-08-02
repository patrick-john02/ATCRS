import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // Public routes
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

    // Admin dashboard
    {
      path: '/admin',
      component: () => import('@/components/layouts/AdminDashboardLayout.vue'),
      meta: { requiresAuth: true, role: 'admin' },
      children: [
        {
          path: 'dashboard',
          name: 'AdminDashboard',
          component: () => import('@/pages/admin/Dashboard.vue'),
        },
      ],
    },

    // Student dashboard
    {
      path: '/student',
      component: () => import('@/components/layouts/StudentDashboardLayout.vue'),
      meta: { requiresAuth: true, role: 'applicant' },
      children: [
        {
          path: 'dashboard',
          name: 'StudentDashboard',
          component: () => import('@/pages/student/Dashboard.vue'),
        },
      ],
    },

    // Super Admin dashboard
    {
      path: '/superadmin',
      component: () => import('@/components/layouts/SuperDashboardLayout.vue'),
      meta: { requiresAuth: true, role: 'superadmin' },
      children: [
        {
          path: 'dashboard',
          name: 'SuperAdminDashboard',
          component: () => import('@/pages/superAdmin/Dashboard.vue'),
        },
      ],
    },

    // Unauthorized route
    // {
    //   path: '/error/Error401',
    //   name: 'Error401',
    //   component: () => import('@/pages/error/Error401.vue'),
    // },
  ],
})

// ✅ Navigation Guard for Authentication & Role-Based Access
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()

  // Wait until the store is hydrated (if using SSR or persisted store)
  if (!auth.user && auth.accessToken) {
    try {
      await auth.fetchUser()
    } catch {
      auth.logout()
      return next('/login')
    }
  }

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const requiredRole = to.meta.role

  if (requiresAuth) {
    if (!auth.accessToken || !auth.user) {
      return next('/login')
    }

    if (requiredRole && auth.user.user_type !== requiredRole) {
      return next('/error/Error401')
    }
  }

  return next()
})

export default router
