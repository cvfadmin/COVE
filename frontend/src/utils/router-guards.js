import store from '@/store'

export default {
	
	isAdminGuard (to, from, next) {
    if (store.state.isAdmin) {
			next()
		} else {
			next({
				name: 'login',
				params: { error: 'You are not authorized to access this route.' },
			})
		}
	},

	isLoggedInGuard (to, from, next) {
		if (store.state.accessToken == '') {
			next({
				name: 'login',
				params: { error: 'You must be logged in to access this route.' },
			})
		} else {
			next()
		}
	},

}