<template>
	<div class="register container">
		<PageHeader></PageHeader>
		<div class="form-container">
			<h2>Register:</h2>
			<form v-on:submit.prevent="handleSubmit">
				<p class="error">{{error}}</p>
				<div class="input-group">
					<div class="input-row">
						<input v-model="first_name" type="text" placeholder="First Name" required>
						<input v-model="last_name" type="text" placeholder="Last Name" required>
					</div>
					<input v-model="username" type="text" placeholder="Username" required>
					<input v-model="email" type="email" placeholder="Email" required>
					<input v-model="password" type="password" placeholder="Password" required>
					<input v-model="confirmPassword" type="password" placeholder="Confirm Password" required>
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
	name: 'register',
	components: {
		PageHeader,
	},

	data () {
		return {
			first_name: '',
			last_name: '',
			username: '',
			password: '',
			confirmPassword: '',
			email: '',
			error: ''
		}
	},

	methods: {
		handleSubmit () {
			if (this.password != this.confirmPassword) {
				this.error = "Passwords don't match"
				return
			}

			this.registerUser().then((response) => {
				if (response.data.error != undefined && response.status == 200) {
					this.error = response.data.error
				} else if (response.status == 200) {
					// Save token to store
					this.$store.commit('setAccessToken', response.data.access_token)
					this.$store.commit('setIsAdmin', response.data.permissions.is_admin)
					router.push({ name: 'home' })
									
				} else {
					// Some weird error
					alert("Oops something went wrong :/ - Please email cove@thecvf.com if error persists.")
					console.log(response)
				}
			});
		},

		async registerUser() {
			return await DatasetService.registerUser({
				first_name: this.first_name,
				last_name: this.last_name,
				username: this.username,
				email: this.email, 
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

	.input-row {
		display: flex;
		align-items: center;

		input {
			flex: 1;
		}

		input:first-child {
			margin-right: 7px;
		}

		input:last-child {
			margin-left: 7px;
		}
	}

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
