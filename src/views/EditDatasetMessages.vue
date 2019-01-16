<template>
	<div class="edit-dataset-messages container">
		<PageHeader></PageHeader>
		<section>
			<ul class="edit-request-list">
				<li v-for="request in unresolvedEditRequests" :key="request.id">
					<EditRequest :request="request"></EditRequest>
				</li>
			</ul>
		</section>
	</div>
</template>

<script>
import PageHeader from '@/components/PageHeader'
import DatasetService from '@/services/DatasetService'
import EditRequest from '@/components/admin/EditRequest.vue'
import moment from 'moment'

export default {
	name: 'editDatasetMessages',
	components: {
		PageHeader,
		EditRequest,
	},

	data () {
		return {
			dataset: {},
			requests: []
		}
	},

	computed: {
		unresolvedEditRequests () {
			return this.requests.filter((item) => {
				return !item.is_resolved
			})
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

	beforeMount () {
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

