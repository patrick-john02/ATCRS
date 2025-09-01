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
          meta: { breadcrumb: 'Admin Dashboard' },
          component: () => import('@/pages/admin/Dashboard.vue'),
        },
        {
          path: 'applicants',
          name: 'AdminAllApplicant',
          meta: { breadcrumb: 'Manage All Applicant' },
          component: () => import('@/pages/admin/AllApplicant.vue'),
        },
        {
          path: 'applicants/pending',
          name: 'AdminPendingApplicants',
          meta: { breadcrumb: 'Manage Pending Applicants' },
          component: () => import('@/pages/admin/PendingApplicants.vue'),
        },
        {
          path: 'applicants/verified',
          name: 'AdminVerifiedApplicants',
          meta: { breadcrumb: 'Manage Verified Applicants' },
          component: () => import('@/pages/admin/VerifiedApplicants.vue'),
        },
        {
          path: '/admin/exams',
          name: 'AdminManageExams',
          meta: { breadcrumb: 'Manage Exams' },
          component: () => import('@/pages/admin/ManageExams.vue'),
        },

        {
          path: '/admin/manage/exams/:id',
          name: 'AdminViewManageExams',
          meta: { breadcrumb: 'View Manage Exams' },
          component: () => import('@/pages/admin/ManageExamsView.vue'),
        },

        {
          path: '/admin/results',
          name: 'AdminViewResults',
          meta: { breadcrumb: 'View Results' },
          component: () => import('@/pages/admin/ViewResults.vue'),
        },
        {
          path: '/admin/results/passed',
          name: 'AdminPassedApplicants',
          meta: { breadcrumb: 'Passed Applicants' },
          component: () => import('@/pages/admin/PassedApplicants.vue'),
        },
        {
          path: '/admin/results/failed',
          name: 'AdminFailedApplicants',
          meta: { breadcrumb: 'Failed Applicants' },
          component: () => import('@/pages/admin/FailedApplicants.vue'),
        },
        {
          path: '/admin/courses',
          name: 'AdminCourses',
          meta: { breadcrumb: 'Manage Courses' },
          component: () => import('@/pages/admin/Courses.vue'),
        },
        {
          path: '/admin/courses/',
          name: 'AdminCourses',
          meta: { breadcrumb: 'Manage Courses' },
          component: () => import('@/pages/admin/Courses.vue'),
        },
        {
          path: '/admin/users/admins',
          name: 'AdminManageAdmin',
          meta: { breadcrumb: 'Manage Admins' },
          component: () => import('@/pages/admin/ManageAdmin.vue'),
        },
        {
          path: '/admin/users/students',
          name: 'AdminManageStudents',
          meta: { breadcrumb: 'Manage Students' },
          component: () => import('@/pages/admin/ManageStudents.vue'),
        },
        {
          path: '/admin/announcements/create',
          name: 'AdminManageAnnouncements',
          meta: { breadcrumb: 'Manage Announcements' },
          component: () => import('@/pages/admin/ManageLandingPage.vue'),
        },

        {
          path: '/admin/profile',
          name: 'AdminProfile',
          meta: { breadcrumb: 'Profile' },
          component: () => import('@/pages/admin/Profile.vue'),
        },
      ],
    },
//student
{
  path: '/student',
  component: () => import('@/components/layouts/StudentDashboardLayout.vue'),
  meta: { requiresAuth: true, role: 'applicant' },
  children: [
    // Dashboard
    {
      path: 'dashboard',
      name: 'StudentDashboard',
      meta: { breadcrumb: 'Student Dashboard' },
      component: () => import('@/pages/student/Dashboard.vue'),
    },

    // Admission
    {
      path: 'admission/apply',
      name: 'AdmissionApply',
      meta: { breadcrumb: 'Apply for Admission' },
      component: () => import('@/pages/student/Apply.vue'),
    },
    {
      path: 'admission/status',
      name: 'AdmissionStatus',
      meta: { breadcrumb: 'Admission Status' },
      component: () => import('@/pages/student/Status.vue'),
    },
    {
      path: 'admission/requirements',
      name: 'AdmissionRequirements',
      meta: { breadcrumb: 'Upload Requirements' },
      component: () => import('@/pages/student/Requirements.vue'),
    },

    // Online Examination
    {
      path: 'exam/instructions',
      name: 'ExamInstructions',
      meta: { breadcrumb: 'Exam Instructions' },
      component: () => import('@/pages/student/Instructions.vue'),
    },
    {
      path: 'exam/start',
      name: 'TakeExam',
      meta: { breadcrumb: 'Take Exam' },
      component: () => import('@/pages/student/Start.vue'),
    },
    {
      path: 'exam/history',
      name: 'ExamHistory',
      meta: { breadcrumb: 'Exam History' },
      component: () => import('@/pages/student/History.vue'),
    },

    // Results
    {
      path: 'results/scores',
      name: 'ViewScores',
      meta: { breadcrumb: 'View Scores' },
      component: () => import('@/pages/student/Scores.vue'),
    },
    {
      path: 'results/download',
      name: 'DownloadResult',
      meta: { breadcrumb: 'Download Result' },
      component: () => import('@/pages/student/Download.vue'),
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

    { path: 'courses-and-departments', name: 'Courses and Departments', component: () => import('@/pages/superAdmin/CoursesAndDept.vue'), meta: { breadcrumb: 'Departments' } },

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
