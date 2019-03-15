import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import * as Cookies from 'js-cookie'
import DatasetService from '@/services/DatasetService'

Vue.use(Vuex)

export default new Vuex.Store({
	state: {
		datasets: [],
		tags: [],
		
		//User info
		accessToken: '',
		isAdmin: false,
		userId: -1,
	},

	mutations: {
		async loadDatasets (state) {
			const response = await DatasetService.getDatasets()
			Vue.set(state, 'datasets', response.data.results)
		},

		async loadTags (state) {
			const response = await DatasetService.getTags()
			Vue.set(state, 'tags', response.data.results)
		},

		setDatasets (state, list) {
			Vue.set(state, 'datasets', list)
		},

		setAccessToken (state, token) {
			Vue.set(state, 'accessToken', token)
		},

		setIsAdmin (state, isAdmin) {
			Vue.set(state, 'isAdmin', isAdmin)
		},

		setUserId (state, id) {
			Vue.set(state, 'userId', id)
		}
	},

	actions: {
		
		login ({commit, state}, [access_token, is_admin, user_id]) {
			commit('setAccessToken', access_token)
			commit('setIsAdmin', is_admin)
			commit('setUserId', user_id)
		},
		
		logout ({commit, state}) {
			commit('setAccessToken', '')
			commit('setIsAdmin', false)
			commit('setUserId', -1)
		},

		async searchDatasets ({commit, state}, args) {
			await DatasetService.searchDatasets(args.query, args.tasks, args.topics, args.data_types).then((response) => {
				commit('setDatasets', response.data.results);
			}).catch((err) => {
				alert("Something went wrong :/")
			})
		},

	},

	plugins: [
		createPersistedState()/*({
			storage: {
				getItem: key => Cookies.get(key),
				// Please see https://github.com/js-cookie/js-cookie#json, on how to handle JSON.
				setItem: (key, value) =>
					Cookies.set(key, value, { expires: 3, secure: true }),
				removeItem: key => Cookies.remove(key),
			},
		}),*/
	],
})
