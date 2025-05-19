import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/auth/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register-organization',
    name: 'RegisterOrganization',
    component: () => import('../views/auth/RegisterOrganization.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('../views/dashboard/AdminDashboard.vue'),
    meta: { requiresAuth: true, role: 'T_ADMIN' }
  },
  {
    path: '/e-admin',
    name: 'EAdminDashboard',
    component: () => import('../views/dashboard/EAdminDashboard.vue'),
    meta: { requiresAuth: true, role: 'E_ADMIN' }
  },
  {
    path: '/senior-e-admin',
    name: 'SeniorEAdminDashboard',
    component: () => import('../views/dashboard/SeniorEAdminDashboard.vue'),
    meta: { requiresAuth: true, role: 'SENIOR_E_ADMIN' }
  },
  {
    path: '/o-convener',
    name: 'OrgDashboard',
    component: () => import('../views/dashboard/OrgDashboard.vue'),
    meta: { requiresAuth: true, role: 'O_CONVENER' }
  },
  {
    path: '/user',
    name: 'UserDashboard',
    component: () => import('../views/dashboard/UserDashboard.vue'),
    meta: { requiresAuth: true, role: 'DATA_USER' }
  },
  {
    path: '/users',
    name: 'Users',
    component: () => import('../views/management/UserManagement.vue')
  },
  {
    path: '/logs',
    name: 'Logs',
    component: () => import('../views/management/LogManagement.vue')
  },
  {
    path: '/policies',
    name: 'Policies',
    component: () => import('../views/management/PolicyManagement.vue')
  },
  {
    path: '/policy-management',
    name: 'PolicyManagement',
    component: () => import('../views/management/PolicyManagement.vue')
  },
  {
    path: '/user-management',
    name: 'UserManagement',
    component: () => import('../views/management/UserManagement.vue')
  },
  {
    path: '/organization-management',
    name: 'OrganizationManagement',
    component: () => import('../views/management/OrganizationManagement.vue')
  },
  {
    path: '/log-management',
    name: 'LogManagement',
    component: () => import('../views/management/LogManagement.vue')
  },
  {
    path: '/bank-account',
    name: 'BankAccount',
    component: () => import('../views/workspace/BankAccount.vue')
  },
  {
    path: '/members',
    name: 'Members',
    component: () => import('../views/workspace/Members.vue')
  },
  {
    path: '/activity-log',
    name: 'ActivityLog',
    component: () => import('../views/workspace/ActivityLog.vue')
  },
  {
    path: '/services-management',
    name: 'ServicesManagement',
    component: () => import('../views/workspace/ServicesManagement.vue')
  },
  {
    path: '/workspace-courses',
    name: 'WorkspaceCourses',
    component: () => import('../views/workspace/Courses.vue')
  },
  {
    path: '/dashboard',
    component: () => import('../views/dashboard/Dashboard.vue'),
    children: [
      { path: 'profile', component: () => import('../views/dashboard/UserProfileCard.vue') },
      // ... 其他子路由
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const role = localStorage.getItem('role')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    if (role === 'T_ADMIN') {
      router.push('/admin')
    } else if (role === 'E_ADMIN') {
      router.push('/e-admin')
    } else if (role === 'SENIOR_E_ADMIN') {
      router.push('/senior-e-admin')
    } else if (role === 'O_CONVENER') {
      router.push('/o-convener')
    } else {
      router.push('/user')
    }
  } else if (to.path === '/') {
    if (token) {
      if (role === 'T_ADMIN') next('/admin')
      else if (role === 'E_ADMIN') next('/e-admin')
      else if (role === 'SENIOR_E_ADMIN') next('/senior-e-admin')
      else if (role === 'O_CONVENER') next('/o-convener')
      else if (role === 'DATA_USER') next('/user')
    }
  }
  next()
})

export default router
