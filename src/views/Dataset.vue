<template>
	<div class="container">
		<PageHeader></PageHeader>
		<Promised :promise="datasetPromise">
	    <template v-slot:pending>
	      <p style="text-align: center;">Loading...</p>
	    </template>

	    <template v-slot="data">
	    	<DatasetDecisionBar v-if="data.data.result.is_approved == false && isAdmin" :datasetId="data.data.result.id"></DatasetDecisionBar>
	      <div class="dataset">
					<MainCard :dataset="data.data.result"></MainCard>
					<SideCard :dataset="data.data.result"></SideCard>
				</div>
	    </template>

	    <template v-slot:rejected="error">
	      <p>Error: {{ error.message }}</p>
	    </template>
	  </Promised>
	</div>
</template>

<script>
import PageHeader from '@/components/PageHeader.vue'
import DatasetService from '@/services/DatasetService'
import DatasetDecisionBar from '@/components/admin/DatasetDecisionBar.vue'
import MainCard from '@/components/datasets/mainpage/MainCard.vue'
import SideCard from '@/components/datasets/mainpage/SideCard.vue'
import { Promised } from 'vue-promised'

export default {
	name: 'dataset',
	components: {
		PageHeader,
		DatasetDecisionBar,
		Promised,
		MainCard,
		SideCard,
	},

	data () {
		return {
			datasetPromise: null
		}
	},

	computed: {
		isAdmin () {
			return this.$store.state.isAdmin
		},
	},

	methods: {
		async getDataset () {
			return await DatasetService.getDatasetById(this.$route.params.id)
		},
	},

	created () {
		this.datasetPromise = this.getDataset()
	},
}
</script>


<style scoped lang="scss">

a {
	color: #444;
	font-size: 14px;
}

strong {
	font-family: 'Open Sans', sans-serif;
	font-weight: 700;
	font-size: 14px;
	color: #656565;
}

.dataset {
	display: flex;
	justify-content: space-between;
	align-items: self-end;
	color: #888888;
}

.card-wrapper {
	padding-top: 20px;
	box-shadow: 0 1px 2px 0 rgba(0,0,0,0.1);
}

</style>
