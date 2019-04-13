<template>
	<div class="open-edit-requests">
		<PageHeader></PageHeader>
		<div class="container">
			<div class="admin-wrapper">
				<SideMenu></SideMenu>

				<Promised :promise="unresolvedEditRequestsPromise">
					<!-- Use the "pending" slot to display a loading message -->
					<template v-slot:pending>
						<p>Loading...</p>
					</template>
					<!-- The default scoped slot will be used as the result -->
					<template v-slot="data">
						<div class="display">
							<p class="null-message" v-if="data.data.results.length == 0"> No unresolved edit requests.</p>
							<ul class="edit-request-list">
								<li v-for="request in data.data.results" :key="request.id">
									<EditRequest :request="request"></EditRequest>
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
import EditRequest from '@/components/admin/EditRequest.vue'
import SideMenu from '@/components/admin/SideMenu.vue'
import AdminService from '@/services/AdminService'
import { Promised } from 'vue-promised'

export default {
	name: 'adminOpenEditRequests',
	components: {
		PageHeader,
		EditRequest,
		SideMenu,
		Promised
	},

	data () {
		return {
			unresolvedEditRequestsPromise: null,
		}
	},

	created () {
		this.unresolvedEditRequestsPromise = AdminService.getUnresolvedEditRequests()
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

	ul li:first-child div {
		margin-top: 0;
	}
}

</style>
