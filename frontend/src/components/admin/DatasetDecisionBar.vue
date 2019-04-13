<template>
	<div class="dataset-decision-bar">
		<p>This dataset has not yet been approved.</p>
		<div class="decision">
			<router-link tag="button" :to="{path: '/datasets/' + datasetId +'/edit/requests'}">Manage Edit Requests</router-link>
			<button v-on:click="adminDecision(true)">Approve</button>
			<button v-on:click="adminDecision(false)">Deny</button>
		</div>
	</div>
</template>

<script>
import AdminService from '@/services/AdminService'

export default {
	name: 'datasetDecisionBar',
	
	props: {
		datasetId: Number,
	},

	methods: {
		async adminDecision (bool) {
			await AdminService.adminDatasetResponse(this.datasetId, {"is_approved": bool}).then((response) => {
				alert(response.data.message)
			})
		},
	},
}
</script>


<style scoped lang="scss">

.dataset-decision-bar {
	display: flex;
	justify-content: space-between;
	margin: 10px 0 0 0;
	background: #d27878;
	padding: 10px 20px;
	border-radius: 2px;
	
	p {
		color: #862828;
		margin: 0;
	}	
}

</style>
