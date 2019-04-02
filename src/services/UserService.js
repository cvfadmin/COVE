import Api from '@/services/Api'

export default {
	getCurrentUserInfo () {
		return Api().get('/users/me')
	},
}