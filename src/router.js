import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import store from '@/store'

Vue.use(Router)

export default new Router({
	mode: 'history',
	base: process.env.BASE_URL,
	routes: [
		{
			path: '/',
			name: 'home',
			component: Home
		},
		{
			path: '/admin',
			name: 'admin',
			component: () => import('./views/Admin.vue'),
			beforeEnter: (to, from, next) => {
				if (!store.state.isAdmin) {
					next({
						path: '/login',
					})
				} else {
					next()
				}
			}
		},
		{
			path: '/login',
			name: 'login',
			component: () => import('./views/Login.vue')
		},
		{
			path: '/register',
			name: 'register',
			component: () => import('./views/Register.vue')
		},
		{
			path: '/logout',
			name: 'logout',
			component: () => import('./views/Logout.vue')
		},
		{
			path: '/users/me',
			name: 'usersPage',
			component: () => import('./views/UsersPage.vue'),
			beforeEnter: (to, from, next) => {
				if (store.state.accessToken == '') {
					next({
						name: 'login',
						params: { error: 'You must be logged in to access this route.' },
					})
				} else {
					next()
				}
			}
		},
		{
			path: '/datasets/create',
			name: 'createDataset',
			component: () => import('./views/CreateDataset.vue'),
			beforeEnter: (to, from, next) => {
				if (store.state.accessToken == '') {
					next({
						name: 'login',
						params: { error: 'You must be logged in to add a dataset' },
					})
				} else {
					next()
				}
			}
		},
		{
			path: '/datasets/:id',
			name: 'dataset',
			component: () => import('./views/Dataset.vue')
		},
		{
			path: '/datasets/:id/edit',
			name: 'editDataset',
			component: () => import('./views/EditDataset.vue'),
			beforeEnter: (to, from, next) => {
				if (store.state.datasetsOwned.indexOf(parseInt(to.params.id)) != -1 || store.state.isAdmin) {
					next()
				} else {
					next({
						name: 'login',
						params: { error: 'You must be logged in as the owner to edit this dataset' },
					})
				}
			}
		}
	]
})
