<template>
	<div class="admin container">
		<PageHeader></PageHeader>
		<div class="admin-wrapper">
			<div class="side-menu">
				<ul>
					<li v-on:click="display = 'datasets'" class="card-wrapper">Confirm Datasets <span>{{notApprovedDatasetsLength}}</span></li>
					<li v-on:click="display = 'add-dataset-requests'" class="card-wrapper">Add Dataset Requests <span>{{addDSRequestsLength}}</span></li>
					<li v-on:click="display = 'edit-dataset-requests'" class="card-wrapper">Edit Dataset Requests <span>{{editDSRequestsLength}}</span></li>
					<li v-on:click="display = 'delete-dataset-requests'" class="card-wrapper">Delete Dataset Requests <span>{{deleteDSRequestsLength}}</span></li>
				</ul>
			</div>
			<div class="display">
				<div v-if="display == 'datasets'">
					<p class="null-message" v-if="notApprovedDatasets.length == 0"> No datasets to confirm.</p>
					<ul class="dataset-list">
						<li v-for="dataset in notApprovedDatasets" :key="dataset.id">
							<DatasetPreview :dataset="dataset"></DatasetPreview>
						</li>
					</ul>
				</div>

				<div v-if="display == 'add-dataset-requests'">
					<p class="null-message" v-if="addDSRequests.length == 0"> No add requests to confirm.</p>
					<div v-for="request in addDSRequests" :key="request.id">
						<AddDatasetRequest :request="request"></AddDatasetRequest>
					</div>
				</div>

				<div v-if="display == 'edit-dataset-requests'">
					<p class="null-message" v-if="editDSRequests.length == 0"> No edit requests to confirm.</p>
					<div v-for="request in editDSRequests" :key="request.id">
						<EditDatasetRequest :request="request"></EditDatasetRequest>
					</div>
				</div>

				<div v-if="display == 'delete-dataset-requests'">
					<p class="null-message" v-if="deleteDSRequests.length == 0"> No delete requests to confirm.</p>
					<div v-for="request in deleteDSRequests" :key="request.id">
						<DeleteDatasetRequest :request="request"></DeleteDatasetRequest>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import PageHeader from '@/components/PageHeader.vue'
import DatasetPreview from '@/components/datasets/DatasetPreview.vue'
import DatasetService from '@/services/DatasetService'
import AddDatasetRequest from '@/components/admin/AddDatasetRequest.vue'
import DeleteDatasetRequest from '@/components/admin/DeleteDatasetRequest.vue'
import EditDatasetRequest from '@/components/admin/EditDatasetRequest.vue'

export default {
	name: 'admin',
	components: {
		PageHeader,
		DatasetPreview,
		AddDatasetRequest,
		DeleteDatasetRequest,
		EditDatasetRequest,
	},

	data () {
		return {
			addDSRequests: [],
			editDSRequests: [],
			deleteDSRequests: [],
			notApprovedDatasets: [],
			display: 'datasets',
		}
	},

	computed: {
		notApprovedDatasetsLength () {
			return this.notApprovedDatasets.length
		},

		deleteDSRequestsLength () {
			return this.deleteDSRequests.length
		},

		addDSRequestsLength () {
			return this.addDSRequests.length
		},

		editDSRequestsLength () {
			return this.editDSRequests.length
		},
	},

	methods: {
		
		// Getters:
		async getAddDSRequests() {
			const response = await DatasetService.getAddDSRequests()
			this.addDSRequests = response.data.results
		},

		async getDeleteDSRequests() {
			const response = await DatasetService.getDeleteDSRequests()
			this.deleteDSRequests = response.data.results
		},

		async getEditDSRequests() {
			const response = await DatasetService.getEditDSRequests()
			this.editDSRequests = response.data.results
		},

		async getNotApprovedDatasets() {
			const response = await DatasetService.getNotApprovedDatasets()
			this.notApprovedDatasets = response.data.results
		},


		// Setters:
		async approveDataset(ds) {
			await DatasetService.approveDataset(ds).then((response) => {
				console.log(response)
			})
		}
	},

	beforeMount () {
		this.getAddDSRequests()
		this.getEditDSRequests()
		this.getDeleteDSRequests()
		this.getNotApprovedDatasets()
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

	.side-menu {
		
		ul {
			margin: 25px 0;

			li {
				cursor: pointer;
				font-weight: 600;
				padding: 10px 10px;
				display: flex;
				justify-content: space-between;
				align-items: center;
				font-size: 13px;
				color: #525252;

				span {
					padding: 5px;
					border-radius: 3px;
					background: #eee;
					font-size: 12px;
					margin-left: 15px;
				}
			}

			li:hover {
				background: #eee;
			}
		}
	}

	.null-message {
		text-align: center;
	}

	.dataset-list {
		display: flex;
		justify-content: space-between;

		li {
			margin: 0 0 20px 0;
			align-items: flex-start;
			width: calc(50% - 20px);
    	box-sizing: border-box;
		}
	}
}

</style>
