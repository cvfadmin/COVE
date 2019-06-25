<template>
	<header>
		<div class="header-wrapper">
			<div class="logo" v-on:click="pushHome">
				<h1>Cove</h1>
				<h2>Computer Vision Exchange</h2>
			</div>
			<nav id='nav'>
				<ul>
					<li><router-link tag="a" to="/">Home</router-link></li>
					<li><router-link tag="a" to="/datasets/create">Add a Dataset</router-link></li>
					<li><a href="https://github.com/cvfadmin/COVE/issues">Report an Issue</a></li>
					<li v-if="this.isLoggedIn"><router-link tag="a" to="/users/me">Your Page</router-link></li>
					<li v-if="!this.isLoggedIn"><router-link tag="a" to="/login">Login</router-link></li>
					<li v-if="!this.isLoggedIn"><router-link tag="a" to="/register">Register</router-link></li>
					<li v-if="this.isLoggedIn && this.isAdmin"><router-link tag="a" to="/admin/confirm-datasets">Admin Panel</router-link></li>
					<li v-if="this.isLoggedIn"><router-link tag="a" to="/logout">Logout</router-link></li>
				</ul>
			</nav>
		</div>
	</header>
</template>

<script>
import router from '@/router'

export default {
	name: 'PageHeader',
	
	computed: {
		isLoggedIn () {
			return this.$store.state.accessToken != ''
		},

		isAdmin () {
			return this.$store.state.isAdmin
		}
	},

	methods: {
		pushHome() {
			this.$router.push({ path: '/'})
		}
	}
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

header {
	
	.header-wrapper {
	display: flex;
	align-items: center;
	max-width: 1040px;
	margin: auto;

		h1 {
			margin: 0;
			height: 100px;
			font-size: 100px;
			font-weight: 500;
			font-family: 'Vollkorn', serif;
			text-transform: uppercase;
		}

		h2 {
			margin: 0;
			text-transform: uppercase;
			font-size: 17px;
			margin-top: 10px;
		}

		nav {
			flex: 1;
			text-align: right;
			
			ul {
				margin: 0;
				padding: 0;
				list-style: none;
				display: flex;
				justify-content: flex-end;

				li {
					margin: 15px;

					a {
						font-size: 14px;
						font-weight: 200;
						text-transform: uppercase;
						color: #000;
						text-decoration: none;
					}

					a.router-link-exact-active {
						text-decoration: underline;
					}
				}

				li:last-child {
					margin-right: 0;
				}
			}
		}

		.logo {
			display: flex;
			flex-direction: column;
			align-items: center;
			cursor: pointer;
		}
	}
}

</style>
