import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import * as Cookies from 'js-cookie'
import DatasetService from '@/services/DatasetService'
import removeFromList from "@/components/utils.js"

Vue.use(Vuex)

export default new Vuex.Store({
	state: {
		datasets: [],
		tags: [],
		selectedTags: [],
		//User info
		accessToken: '',
		isAdmin: false,
		datasetsOwned: [],
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

		addSelectedTag (state, tag) {
			state.selectedTags.push(tag)
		},

		removeSelectedTag (state, tag) {
			Vue.set(state, 'selectedTags', removeFromList(tag, state.selectedTags))
		},

		setSelectedTags (state, list) {
			Vue.set(state, 'selectedTags', list)
		},

		setAccessToken (state, token) {
			Vue.set(state, 'accessToken', token)
		},

		setIsAdmin (state, isAdmin) {
			Vue.set(state, 'isAdmin', isAdmin)
		},

		setDatasetsOwned (state, list) {
			Vue.set(state, 'datasetsOwned', list)
		}
	},

	actions: {
		
		login ({commit, state}, [access_token, is_admin, datasets_owned]) {
			commit('setAccessToken', access_token)
			commit('setIsAdmin', is_admin)
			commit('setDatasetsOwned', datasets_owned)
		},
		
		logout ({commit, state}) {
			commit('setAccessToken', '')
			commit('setIsAdmin', false)
			commit('setDatasetsOwned', [])
		},

		clearSelectedTags ({commit, state}) {
			commit('setSelectedTags', [])
		},

		setSelectedTagsFromDS ({commit, state}, dataset) {
			let datasetTags = state.tags.filter((item) => {return dataset.tags.indexOf(item.id) != -1})
			commit('setSelectedTags', datasetTags)
		},

		async searchDatasets ({commit, state}, args) {
			await DatasetService.searchDatasets(args.query, args.tasks, args.topics, args.data_types).then((response) => {
				commit('setDatasets', response.data.results);
			}).catch((err) => {
				alert("Something went wrong :/")
			})
		},

	},

	plugins:[
		createPersistedState({
			storage: {
				getItem: key => Cookies.get(key),
				// Please see https://github.com/js-cookie/js-cookie#json, on how to handle JSON.
				setItem: (key, value) =>
					Cookies.set(key, value, { expires: 1, secure: false }), // Expiration should match JWT expiration
				removeItem: key => Cookies.remove(key),
			},
		}),
	],
})
