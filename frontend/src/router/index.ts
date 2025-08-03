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
        {
      path: '/signup',
      component: () => import('@/pages/auth/Register.vue'),
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
  meta: { requiresAuth: true, role: 'superadmin', breadcrumb: 'Super Admin' },
  children: [
    { path: 'dashboard', name: 'SuperAdminDashboard', component: () => import('@/pages/superAdmin/Dashboard.vue'), meta: { breadcrumb: 'Dashboard' } },

    { path: 'users', name: 'SuperAdminUsers', component: () => import('@/pages/superAdmin/AllAdmins.vue'), meta: { breadcrumb: 'Users' } },
    { path: 'admins', name: 'AllAdmins', component: () => import('@/pages/superAdmin/AllAdmins.vue'), meta: { breadcrumb: 'Admins' } },
    { path: 'applicants', name: 'AllApplicants', component: () => import('@/pages/superAdmin/Applicants.vue'), meta: { breadcrumb: 'Applicants' } },

    // { path: 'courses', name: 'Courses', component: () => import('@/pages/superAdmin/courses/Index.vue'), meta: { breadcrumb: 'Courses' } },
    // { path: 'departments', name: 'Departments', component: () => import('@/pages/superAdmin/departments/Index.vue'), meta: { breadcrumb: 'Departments' } },

    // { path: 'academic-years', name: 'AcademicYears', component: () => import('@/pages/superAdmin/academicYears/Index.vue'), meta: { breadcrumb: 'Academic Years' } },
    // { path: 'terms', name: 'Terms', component: () => import('@/pages/superAdmin/terms/Index.vue'), meta: { breadcrumb: 'School Terms' } },

    // { path: 'logs', name: 'AuditLogs', component: () => import('@/pages/superAdmin/logs/Index.vue'), meta: { breadcrumb: 'Audit Logs' } },
    // { path: 'activity', name: 'ActivityReports', component: () => import('@/pages/superAdmin/activity/Index.vue'), meta: { breadcrumb: 'Activity Reports' } },

    // { path: 'settings', name: 'Settings', component: () => import('@/pages/superAdmin/settings/Index.vue'), meta: { breadcrumb: 'Site Configuration' } },
    // { path: 'backup', name: 'DatabaseBackup', component: () => import('@/pages/superAdmin/backup/Index.vue'), meta: { breadcrumb: 'Database Backup' } },

    { path: 'profile', name: 'SuperAdminProfile', component: () => import('@/pages/superAdmin/Profile.vue'), meta: { breadcrumb: 'Profile' } },
  ],
}

    // Unauthorized route
    // {
    //   path: '/error/Error401',
    //   name: 'Error401',
    //   component: () => import('@/pages/error/Error.vue'),
    // },
  ],
})

router.beforeEach(async (to, _, next) => {
  const auth = useAuthStore()

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
