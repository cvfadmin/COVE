<template>
	<div class="admin">
		<PageHeader></PageHeader>
		<div class="container">
			<div class="admin-wrapper">
				<SideMenu></SideMenu>
				<div class="display">
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
</template>

<script>
import PageHeader from '@/components/PageHeader.vue'
import DatasetPreview from '@/components/datasets/DatasetPreview.vue'
import SideMenu from '@/components/admin/SideMenu.vue'
import AdminService from '@/services/AdminService'

export default {
	name: 'admin',
	components: {
		PageHeader,
		DatasetPreview,	
		SideMenu
	},

	data () {
		return {
			notApprovedDatasets: []
		}
	},

	computed: {
		notApprovedDatasetsLength () {
			return this.notApprovedDatasets.length
		},
	},

	methods: {
		async getNotApprovedDatasets() {
			const response = await AdminService.getNotApprovedDatasets()
			this.notApprovedDatasets = response.data.results
		}
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

	.null-message {
		text-align: center;
	}

	.dataset-list {
		display: flex;
		justify-content: space-between;
		flex-wrap: wrap;

		li {
			margin: 0 0 20px 0;
			align-items: flex-start;
			width: calc(50% - 20px);
    	box-sizing: border-box;
		}
	}
}

</style>
