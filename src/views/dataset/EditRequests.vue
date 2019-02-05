<template>
	<div class="edit-requests container">
		<PageHeader></PageHeader>
		<p class="null-message" v-if="unresolvedEditRequests.length == 0"> No open edit requests.</p>
		<section v-if="unresolvedEditRequests.length > 0">
			<h3>Open Edit Requests:</h3>
			<ul class="edit-request-list">
				<li v-for="request in unresolvedEditRequests" :key="request.id">
					<EditRequest :request="request"></EditRequest>
				</li>
			</ul>
		</section>
		<section v-if="isAdmin" id="create-new">
			<h3>Create a New Edit Request:</h3>
			<EditRequestForm></EditRequestForm>
		</section>
	</div>
</template>

<script>
import PageHeader from '@/components/PageHeader'
import DatasetService from '@/services/DatasetService'
import EditRequest from '@/components/admin/EditRequest.vue'
import EditRequestForm from '@/components/admin/EditRequestForm.vue'
import moment from 'moment'

export default {
	name: 'datasetEditRequests',
	components: {
		PageHeader,
		EditRequest,
		EditRequestForm
	},

	data () {
		return {
			dataset: {},
			requests: [],
		}
	},

	computed: {
		unresolvedEditRequests () {
			return this.requests.filter((item) => {
				return !item.is_resolved
			})
		},

		isAdmin () {
			return this.$store.state.isAdmin
		}
	},

	methods: {

		async getRequests () {
			const response = await DatasetService.getEditRequests(this.$route.params.id)
			this.requests = response.data.results
		},

		// TODO: Check for dataset in store before sending another request
		async getDataset () {
			return await DatasetService.getDatasetById(this.$route.params.id)
		},

		moment: function () {
			return moment();
		},
	},

	filters: {
		moment: function (date) {
			return moment(date).fromNow();
		}
	},

	created () {
		this.getDataset().then((response) => {
			this.dataset = response.data.result

			// TODO: better way to handle these permissions?
			if (!this.$store.state.isAdmin) {
				if (this.$store.state.userId != this.dataset.owner) {
					this.$router.push('/')
				}
			}
		})
		
		this.getRequests()
	}

}
</script>


<style scoped lang="scss">

h3 {
	font-family: 'Vollkorn', serif;
  font-weight: 500;
}

.null-message {
	text-align: center;
}

.request, .message {
	padding: 10px;
	
	p {
		margin: 0;
		font-size: 12px;
	}

	.bottom {
		margin-top: 5px;

		p {
			font-size: 11px;
			font-weight: 600;
		}
	}

	.top {
		margin-bottom: 5px;

		p {
			font-size: 11px;
			font-weight: 600;
		}
	}
}

form {
	display: flex;
	flex-direction: column;
	margin-top: 25px;
}

</style>

