import Home from './views/Home.vue'
import routerGuards from '@/utils/router-guards';

export default [
    {
        path: '/',
        name: 'home',
        component: Home
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('./views/auth/Login.vue')
    },
    {
        path: '/register',
        name: 'register',
        component: () => import('./views/auth/Register.vue')
    },
    {
        path: '/logout',
        name: 'logout',
        component: () => import('./views/auth/Logout.vue')
    },
    {
        path: '/users/me',
        name: 'usersPage',
        component: () => import('./views/UsersPage.vue'),
        beforeEnter: (to, from, next) => { routerGuards.isLoggedInGuard(to, from, next) }
    },
    {
        path: '/datasets/create',
        name: 'createDataset',
        component: () => import('./views/dataset/CreateDataset.vue'),
        beforeEnter: (to, from, next) => { routerGuards.isLoggedInGuard(to, from, next) }
    },
    {
        path: '/datasets/:id',
        name: 'dataset',
        component: () => import('./views/Dataset.vue')
    },
    {
        path: '/datasets/:id/edit',
        name: 'editDataset',
        component: () => import('./views/dataset/EditDataset.vue'),
    },
    {
        path: '/datasets/:id/edit/requests',
        name: 'datasetEditRequests',
        component: () => import('./views/dataset/EditRequests.vue'),
    },
    {
        path: '/datasets/:id/requests/ownership',
        name: 'datasetOwnershipRequests',
        component: () => import('./views/dataset/OwnershipRequests.vue'),
        beforeEnter: (to, from, next) => { routerGuards.isLoggedInGuard(to, from, next) }
    },
    {
        path: '/admin/confirm-datasets',
        name: 'adminConfirmDatasets',
        component: () => import('./views/admin/ConfirmDatasets.vue'),
        beforeEnter: (to, from, next) => { routerGuards.isAdminGuard(to, from, next) }
    },
    {
        path: '/admin/open-edit-requests',
        name: 'adminOpenEditRequests',
        component: () => import('./views/admin/OpenEditRequests.vue'),
        beforeEnter: (to, from, next) => { routerGuards.isAdminGuard(to, from, next) }
    },
    {
        path: '/admin/open-ownership-requests',
        name: 'adminOpenOwnershipRequests',
        component: () => import('./views/admin/OpenOwnershipRequests.vue'),
        beforeEnter: (to, from, next) => { routerGuards.isAdminGuard(to, from, next) }
    },
    {
        path: '/admin/users-display',
        name: 'adminUsersDisplay',
        component: () => import('./views/admin/UsersDisplay.vue'),
        beforeEnter: (to, from, next) => { routerGuards.isAdminGuard(to, from, next) }
    },

]