<template>
	<div class="delete-dataset-request card-wrapper">
		<div class="info">
			<div>
				<p><strong>Contact Name: </strong> {{request.first_name}} {{request.last_name}}</p>
				<p><strong>Contact Email: </strong> {{request.email}}</p>
			</div>
			<div class="link">
				<router-link tag="a" :to="{path: '/datasets/' + request.dataset}" target="_blank" rel="noopener noreferrer">Link to Dataset</router-link>
			</div>
		</div>
		<p class="reason"><strong>Reason: </strong> {{request.reason}}</p>
		<div class="decision">
			<button v-on:click="adminDecision(true)">Approve</button>
			<button v-on:click="adminDecision(false)">Deny</button>
		</div>
	</div>
</template>

<script>
import DatasetService from '@/services/DatasetService'

export default {
	name: 'DeleteDatasetRequest',

	props: {
		request: Object,
	},

	methods: {
		async adminDecision (bool) {
			await DatasetService.adminDeleteDSRequestResponse(this.request.id, {"is_approved": bool}).then((response) => {
				if (response.status == 200) {
					if (bool) {
						alert('Request has been approved')
					} else {
						alert('Request has been denied')
					}
				} else {
						alert('Something went wrong :/')
						console.log(response)
					}
			})
		}
	}
}

</script>

<style scoped lang="scss">

.delete-dataset-request {
	margin: 0;
	padding-top: 20px;

	strong, a {
		color: #525252;
	}

	a {
		font-size: 12px;
	}

	p {
		margin: 0;
		font-size: 12px;
		color: #444;
	}

	.info {
		display: flex;
		justify-content: space-between;
	}

	.intro {
		margin: 10px 0;
	}
}

</style>
	

