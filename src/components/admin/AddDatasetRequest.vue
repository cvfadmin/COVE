<template>
	<div class="add-dataset-request card-wrapper">
		<div class="info">
			<div>
				<p><strong>Dataset Name:</strong> {{request.dataset_name}}</p>
				<p><strong>Contact Name:</strong> {{request.first_name}} {{request.last_name}}</p>
				<p><strong>Contact Email:</strong> {{request.email}}</p>
			</div>
			<div class="link">
				<a :href="request.url" target="_blank" rel="noopener noreferrer">Link to Dataset</a>
			</div>
		</div>
		<p class="intro">{{request.intro}}</p>
		<div class="decision">
			<button v-on:click="adminDecision(true)">Approve</button>
			<button v-on:click="adminDecision(false)">Deny</button>
		</div>
	</div>
</template>

<script>
import DatasetService from '@/services/DatasetService'

export default {
	name: 'AddDatasetRequest',

	props: {
		request: Object,
	},

	methods: {
		async adminDecision (bool) {
			await DatasetService.adminAddDSRequestResponse(this.request.id, {"is_approved": bool}).then((response) => {
				
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

				this.$emit('addDSRequestCompleted')
			})
		}
	}
}

</script>

<style scoped lang="scss">
	
.add-dataset-request {
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
