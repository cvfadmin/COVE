import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import DatasetService from '@/services/DatasetService'
import removeFromList from "@/components/utils.js"

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  	datasets: [],
  	tags: [],
		selectedTags: [],
		accessToken: '',
		isAdmin: false,
  },

  mutations: {
		async loadDatasets (state) {
			const response = await DatasetService.getDatasets()
			Vue.set(state, 'datasets', response.data.results);
		},

		async loadTags (state) {
			const response = await DatasetService.getTags()
			Vue.set(state, 'tags', response.data.results);
		},

		setDatasets (state, list) {
			Vue.set(state, 'datasets', list);
		},

		addSelectedTag (state, tag) {
			state.selectedTags.push(tag)
		},

		removeSelectedTag (state, tag) {
			Vue.set(state, 'selectedTags', removeFromList(tag, state.selectedTags))
		},

		setSelectedTags (state, list) {
			Vue.set(state, 'selectedTags', list);
		},

		setAccessToken (state, token) {
			Vue.set(state, 'accessToken', token);
		},

		setIsAdmin (state, isAdmin) {
			Vue.set(state, 'isAdmin', isAdmin)
		}
  },

  actions: {
		
		logout ({commit, state}) {
			commit('setAccessToken', '')
			commit('setIsAdmin', false)
		},

		clearSelectedTags ({commit, state}) {
			commit('setSelectedTags', [])
		},

		async searchDatasets ({commit, state}, args) {
			await DatasetService.searchDatasets(args.query, args.tasks, args.topics, args.data_types).then((response) => {
				commit('setDatasets', response.data.results);
			}).catch((err) => {
				alert("Something went wrong :/")
			})
		},

  },

  plugins:[createPersistedState()],
})
