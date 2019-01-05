<template>
	<div class="admin">
		<PageHeader></PageHeader>
		<div class="container">
			<div class="admin-wrapper">
				<div class="side-menu">
					<ul>
						<li v-on:click="display = 'datasets'" class="card-wrapper">Confirm Datasets <span>{{notApprovedDatasetsLength}}</span></li>
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
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import PageHeader from '@/components/PageHeader.vue'
import DatasetPreview from '@/components/datasets/DatasetPreview.vue'
import DatasetService from '@/services/DatasetService'

export default {
	name: 'admin',
	components: {
		PageHeader,
		DatasetPreview,	},

	data () {
		return {
			notApprovedDatasets: [],
			display: 'datasets',
		}
	},

	computed: {
		notApprovedDatasetsLength () {
			return this.notApprovedDatasets.length
		},
	},

	methods: {
		async getNotApprovedDatasets() {
			const response = await DatasetService.getNotApprovedDatasets()
			this.notApprovedDatasets = response.data.results
		},
	},

	beforeMount () {
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
