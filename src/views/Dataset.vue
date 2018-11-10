<template>
  <div class="dataset container">
		<PageHeader></PageHeader>
		<p>{{dataset}}</p>
  </div>
</template>

<script>

import PageHeader from '@/components/PageHeader.vue'
import DatasetService from '@/services/DatasetService'

export default {
	name: 'dataset',
	components: {
		PageHeader,
	},

	data () {
		return {
			dataset: {},
		}
	},

	methods: {
		async getDataset () {
			const response = await DatasetService.getDatasetById(this.$route.params.id)
			this.dataset = response.data.result
		}
	},

	beforeMount(){
		this.getDataset()
	},
}
</script>

<!-- Add "scoped" attribute to limit SCSS to this component only -->
<style scoped lang="scss">
</style>
