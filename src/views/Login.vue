<template>
	<div class="login container">
		<PageHeader></PageHeader>
		<div class="form-container">
			<h2>Login:</h2>
			<form v-on:submit.prevent="handleSubmit">
				<p class="error">{{error}}</p>
				<p class="error">{{routeError}}</p>
				<div class="input-group">
					<input v-model="username" type="text" placeholder="username" required>
					<input v-model="password" type="password" placeholder="password" required>
				</div>
				<div class="input-group">
					<button type="submit">Submit</button>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
import PageHeader from '@/components/PageHeader.vue'
import DatasetService from '@/services/DatasetService'
import router from '@/router'

export default {
	name: 'login',
	components: {
		PageHeader,
	},

	data () {
		return {
			username: '',
			password: '',
			error: ''
		}
	},

	computed: {
		routeError() {
			return this.$route.params.error
		}
	},

	methods: {
		handleSubmit () {
			this.loginUser().then((response) => {
				if (response.data.error != undefined && response.status == 200) {
					this.error = response.data.error

				} else if (response.status == 200) {
					this.$store.dispatch('login', [response.data.access_token, response.data.permissions.is_admin, response.data.user_id])
					router.push({ name: 'home' })
									
				} else {
					// Some weird error
					alert("Oops something went wrong :/ - Please email cove@thecvf.com if error persists.")
					console.log(response)
				}
			});
		},

		async loginUser() {
			return await DatasetService.loginUser({
				username: this.username, 
				password: this.password
			})
		},
	}
}
</script>

<!-- Add "scoped" attribute to limit SCSS to this component only -->
<style scoped lang="scss">

.form-container {
	max-width: 500px;
	margin: 0 auto;
}

.error {
	font-style: italic;
	font-weight: 400;
	color: #de6868;
	font-size: 12px;
}

h2 {
	margin-top: 40px;
}

form {

	button {
		background: none;
		border: 1px #000 solid;
		padding: 10px 0;
		margin: 20px 0 50px 0;
	}

	button:hover {
		background: #000;
		color: #fff;
	}
}

</style>
