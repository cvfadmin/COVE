import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'
import store from '@/store'
import DatasetService from '@/services/DatasetService'

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
			path: '/about',
			name: 'about',
			component: () => import('./views/About.vue')
		},
		{
			path: '/add-dataset',
			name: 'addDataset',
			component: () => import('./views/AddDataset.vue')
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
			path: '/logout',
			name: 'logout',
			component: () => import('./views/Logout.vue')
		},
		{
			path: '/datasets/create/:key',
			name: 'createDataset',
			component: () => import('./views/CreateDataset.vue'),
			beforeEnter: (to, from, next) => {
				DatasetService.isCreateDSKeyValid(to.params.key).then((response) => {
					if (response.data.is_active) {
						next()
					} else {
						next({
							path: '/',
						})
					}
				})
			}
		},
		{
			path: '/datasets/:id',
			name: 'dataset',
			component: () => import('./views/Dataset.vue')
		},
		{
			path: '/datasets/:id/edit-request',
			name: 'editDataset',
			component: () => import('./views/requests/EditDataset.vue')
		},
		{
			path: '/datasets/:id/delete-request',
			name: 'deleteDataset',
			component: () => import('./views/requests/DeleteDataset.vue')
		}
	]
})
