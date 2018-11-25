import Api from '@/services/Api'
import UrlUtil from '@/utils/UrlUtil'

export default {
		getDatasets () {
			return Api().get('/datasets/')
		},

		searchDatasets (query, tasks, topics, dataTypes) {
			let url = UrlUtil.buildUrl('/datasets/', {
				search: query,
				tasks: tasks,
				topics: topics,
				data_types: dataTypes
			})
			return Api().get(url)
		},

		getDatasetById (dataset_id) {
			return Api().get('/datasets/' + dataset_id)
		},

		createDataset (data) {
			return Api().post('/datasets/', data)
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

		logoutUser () {
			return Api().post('/users/logout')
		},

		createAddDSRequest(data) {
			return Api().post('/requests/add-dataset', data)
		},

		createDeleteDSRequest(data) {
			return Api().post('/requests/delete-dataset', data)
		},

		createEditDSRequest(data) {
			return Api().post('/requests/edit-dataset', data)
		},

		// Admin stuff
		
		getAddDSRequests () {
			return Api().get('/requests/add-dataset')
		},
		
		getDeleteDSRequests () {
			return Api().get('/requests/delete-dataset')
		},
		
		getEditDSRequests () {
			return Api().get('/requests/edit-dataset')
		},

		getNotApprovedDatasets () {
			// Only admins can accesss this route
			return Api().get('/datasets?approved=false')
		},

		adminDatasetResponse (id, approval_obj) {
			return Api().put('/admin/datasets/' + id, approval_obj)
		},

		adminAddDSRequestResponse (id, approval_obj) {
			return Api().put('/admin/requests/add-dataset/' + id, approval_obj)
		},

		adminEditDSRequestResponse (id, approval_obj) {
			return Api().put('/admin/requests/edit-dataset/' + id, approval_obj)
		},

		adminDeleteDSRequestResponse (id, approval_obj) {
			return Api().put('/admin/requests/delete-dataset/' + id, approval_obj)
		},

		isCreateDSKeyValid (key) {
			return Api().get('/admin/create-dataset-key/' + key)
		},

}