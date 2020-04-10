<template>
	<div class="users-display">
		<PageHeader></PageHeader>
		<div class="container">
			<div class="admin-wrapper">
				<SideMenu></SideMenu>

				<Promised :promise="usersListPromise">
					<!-- Use the "pending" slot to display a loading message -->
					<template v-slot:pending>
						<p>Loading...</p>
					</template>
					<!-- The default scoped slot will be used as the result -->
					<template v-slot="data">
						<div class="display">
							<p class="null-message" v-if="data.data.length == 0"> No users found.</p>
							<ul class="user-list">
                                <li id="user-header">
                                    <p>Name</p>
                                    <p>Username</p>
                                    <p>Email</p>
                                    <p>Datasets Owned</p>
                                </li>
								<li v-for="user in data.data.users" :key="user.id">
                                    <p>{{user.first_name}} {{user.last_name}}</p>
                                    <p>{{user.username}}</p>
                                    <p>{{user.email}}</p>
                                    <p>{{user.datasets.length}}</p>
								</li>
							</ul>
						</div>
					</template>
					<!-- The "rejected" scoped slot will be used if there is an error -->
					<template v-slot:rejected="error">
						<p>Error: {{ error.message }}</p>
					</template>
				</Promised>

			</div>
		</div>
	 </div>
</template>

<script>
import PageHeader from '@/components/PageHeader.vue'
import SideMenu from '@/components/admin/SideMenu.vue'
import AdminService from '@/services/AdminService'
import { Promised } from 'vue-promised'

export default {
	name: 'adminUsersDisplay',
	components: {
		PageHeader,
        SideMenu,
		Promised
	},

	data () {
		return {
			usersListPromise: null,
		}
	},

	created () {
		this.usersListPromise = AdminService.getUsersList()
	}
}
</script>

<!-- Add "scoped" attribute to limit SCSS to this component only -->
<style scoped lang="scss">

.admin-wrapper {
	font-family: 'Open Sans', sans-serif;
	display: flex;

	.display {
		flex: 1;
		margin: 20px 30px;
	}

	.null-message {
		text-align: center;
	}

    ul {
        background: #fff;
        border-radius: 3px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.1);
        padding: 10px 20px;
        
        li {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            grid-gap: 10px;
            border-top: 1px solid #eee;

            p {
                color: #595959;
                font-size: 14px;
                margin: 0;
                padding: 10px 0;
                word-break: break-all;
            }
        }

        li#user-header {
            border: none;
            font-weight: bold;
        }
    }
}

</style>
