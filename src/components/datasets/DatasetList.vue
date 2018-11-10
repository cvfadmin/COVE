<template>
	<ul class="dataset-list">
		<li v-for="dataset in datasets" :key="dataset.id">
			<DatasetPreview :dataset="{dataset}"></DatasetPreview>
		</li>
	</ul>
</template>

<script>

import DatasetService from '@/services/DatasetService'
import DatasetPreview from '@/components/datasets/DatasetPreview'

export default {
	name: 'DatasetList',
	components: {
		DatasetPreview,
	},

	data () {
		return {
			datasets: [],
		}
	},

	methods: {
		async getDatasets () {
			const response = await DatasetService.getDatasets()
			this.datasets = response.data.results
		}
	},

	beforeMount(){
		this.getDatasets()
	},
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
	
	.dataset-list {
		list-style: none;
		padding: 0;
		margin: 20px 0 0 0;
	}

</style>
