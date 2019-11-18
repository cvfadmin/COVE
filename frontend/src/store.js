import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import * as Cookies from 'js-cookie'
import DatasetService from '@/services/DatasetService'

Vue.use(Vuex)

export default new Vuex.Store({
	state: {
		tags: [],
		
		// For persistent behavior with tags
		searchTags: {
			tasks: [],
			topics: [],
			dataTypes: [],
		},

		//User info
		accessToken: '',
		isAdmin: false,
		userId: -1,
	},

	mutations: { // Always synchronous

		async loadTags (state) {
			const response = await DatasetService.getTags()
			Vue.set(state, 'tags', response.data.results)
		},

		setAccessToken (state, token) {
			Vue.set(state, 'accessToken', token)
		},

		setIsAdmin (state, isAdmin) {
			Vue.set(state, 'isAdmin', isAdmin)
		},

		setUserId (state, id) {
			Vue.set(state, 'userId', id)
		},

		setDataTypesSearchTags (state, updatedTags) {
			Vue.set(state['searchTags'], 'dataTypes', updatedTags)
		},

		setTasksSearchTags (state, updatedTags) {
			Vue.set(state['searchTags'], 'tasks', updatedTags)
		},

		setTopicsSearchTags (state, updatedTags) {
			Vue.set(state['searchTags'], 'topics', updatedTags)
		},

		clearSearchTags (state) {
			Vue.set(state, 'searchTags', { tasks: [], topics: [], dataTypes: [],})
		}
	},

	actions: { // Synchronous or Asynchronous
		
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

	},

	plugins: [
		createPersistedState()
	],
})
