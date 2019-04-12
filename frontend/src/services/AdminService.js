import Api from '@/services/Api'

export default {
		getUnresolvedEditRequests () {
			return Api().get('/admin/edit-requests?is_resolved=false')
		},

		createEditRequestMessage (request_id, data) {
			return Api().post('/admin/edit-requests/' + request_id + '/messages', data)
		},

		updateEditRequestMessage (message_id, data) {
			return Api().put('/admin/edit-request-messages/' + message_id, data)
		},

		updateEditRequest (request_id, data) {
			return Api().put('/admin/edit-requests/' + request_id, data)
		},

		adminDatasetResponse (id, approval_obj) {
			return Api().put('/admin/datasets/' + id, approval_obj)
		},

		getNotApprovedDatasets () {
			return Api().get('/datasets/?approved=false')
		},
}