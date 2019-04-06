import Api from '@/services/Api'
import UrlUtil from '@/utils/UrlUtil'

export default {
		getDatasets () {
			return Api().get('/datasets/')
		},

		searchDatasets (params) {
			let url = UrlUtil.buildUrl('/datasets/', {
				search: params.query,
				tasks: params.tasks,
				topics: params.topics,
				data_types: params.dataTypes,
				limit: params.limit,
				offset: params.offset,
			})
			return Api().get(url)
		},

		getDatasetById (dataset_id) {
			return Api().get('/datasets/' + dataset_id)
		},

		createDataset (data) {
			return Api().post('/datasets/', data)
		},

		updateDataset (dataset_id, data) {
			return Api().put('/datasets/' + dataset_id, data)
		},

		getTags () {
			return Api().get('/tags/')
		},

		createManyTags (data) {
			// Expects list of objects
			return Api().post('/tags/?many=true', data)
		},

		loginUser (data) {
			return Api().post('/users/login', data)
		},

		registerUser (data) {
			return Api().post('/users/register', data)
		},

		logoutUser () {
			return Api().post('/users/logout')
		},

		getCurrentUserInfo () {
			return Api().get('/users/me')
		},

		// Admin stuff

		createEditRequest (dataset_id, data) {
			return Api().post('/admin/datasets/' + dataset_id + '/edit-requests', data)
		},

		getEditRequests (dataset_id) {
			return Api().get('/admin/datasets/' + dataset_id + '/edit-requests')
		},

}