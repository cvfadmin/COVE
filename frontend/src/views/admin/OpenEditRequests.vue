<template>
	<div class="open-edit-requests">
		<PageHeader></PageHeader>
		<div class="container">
			<div class="admin-wrapper">
				<SideMenu></SideMenu>
				<div class="display">
					<p class="null-message" v-if="unresolvedEditRequests.length == 0"> No unresolved edit requests.</p>
					<ul class="edit-request-list">
						<li v-for="request in unresolvedEditRequests" :key="request.id">
							<EditRequest :request="request"></EditRequest>
						</li>
					</ul>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import PageHeader from '@/components/PageHeader.vue'
import EditRequest from '@/components/admin/EditRequest.vue'
import SideMenu from '@/components/admin/SideMenu.vue'
import AdminService from '@/services/AdminService'

export default {
	name: 'adminOpenEditRequests',
	components: {
		PageHeader,
		EditRequest,
		SideMenu
	},

	data () {
		return {
			unresolvedEditRequests: [],
		}
	},

	computed: {
		unresolvedEditRequestsLength () {
			return this.unresolvedEditRequests.length
		},
	},

	methods: {
		async getUnresolvedEditRequests() {
			const response = await AdminService.getUnresolvedEditRequests()
			this.unresolvedEditRequests = response.data.results
		},
	},

	beforeMount () {
		this.getUnresolvedEditRequests()
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
