<template>
	<ul class="dataset-list">
		<li v-for="dataset in datasets" :key="dataset.id">
			<DatasetPreview :dataset="dataset" :notification="getNotificationObject(dataset)"></DatasetPreview>
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
	
	computed: {
		datasets () {
			return this.$store.state.datasets
		}
	},

	methods: {

		countOpenRequests(message_list) {
			let unresolved = message_list.filter((item) => { return !item.is_resolved })
			return unresolved.length
		},

		getNotificationObject (dataset) {
			if (this.$store.state.isAdmin && !dataset.is_approved) {
				return {
					'message': 'This dataset needs to be confirmed.',
					'link': {'path': '/datasets/' + dataset.id},
				}
			} else if (this.$store.state.userId == dataset.owner) {
				let numUnread = this.countOpenRequests(dataset.edit_requests)
				if (numUnread > 0) {
					return {
						'message': 'You have ' + numUnread + ' unread edit requests for this dataset',
						'link': {'path': '/datasets/' + dataset.id +'/edit/requests'},
					}
				}
			}
			return undefined
		}
	},

	beforeMount(){

		let params = {
			query: this.$route.query.query, 
			tasks: this.$route.query.tasks, 
			topics: this.$route.query.topics, 
			data_types: this.$route.query.data_types
		}
			
		// Clean params object
		for (const key of Object.keys(params)) {
			if (params[key] == undefined) {
				delete params[key]
			} 
		}

		this.$store.dispatch('searchDatasets', params)
	},
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
	
	ul.dataset-list {
		display: flex;
  	flex-flow: row wrap;
		justify-content: space-between;
		list-style: none;
		padding: 0;
		margin: 20px 0 0 0;

		&::after {
		  content: "";
			width: calc(33% - 20px);
		}

		li {
			margin: 0 0 20px 0;
			align-items: flex-start;
			width: calc(33% - 20px);
    	box-sizing: border-box;
		}
	}

</style>
