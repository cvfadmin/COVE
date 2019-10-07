<template>
	<div>
		<ul class="dataset-list">
			<li v-for="dataset in datasets" :key="dataset.id">
				<DatasetPreview :dataset="dataset" :notification="getNotificationObject(dataset)"></DatasetPreview>
			</li>
		</ul>
		<p id="bottom-message">{{bottomMessage}}</p>
	</div>
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
			lastDatasetRequestCompleted: true,
			limit: 25, // Number of datasets to request at once
			offset: 0,
			bottomMessage: "",
		}
	},

	methods: {

		// Whenever user has reached the bottom of the page, display the next
		// set of datasets.
		scroll () {
			window.onscroll = () => {
				let bottomOfWindow = Math.max(window.pageYOffset, document.documentElement.scrollTop, document.body.scrollTop) + window.innerHeight === document.documentElement.offsetHeight

				if (bottomOfWindow) {
					let params = {
						query: this.$route.query.query, 
						tasks: this.$route.query.tasks, 
						topics: this.$route.query.topics, 
						data_types: this.$route.query.data_types,
					}

					this.getDatasets(params)
				}
			}
		},

		// Get datasets to display, then set params for the next page.
		async getDatasets (params) {
			this.bottomMessage = "Loading..."

			// Finish last dataset request before starting a new one
			if (this.lastDatasetRequestCompleted) {
				this.lastDatasetRequestCompleted = false
				params.offset = this.offset
				params.limit = this.limit

				await DatasetService.searchDatasets(params).then((response) => {
					if (response.data.results.length == 0) {
						this.bottomMessage = "No more datasets to load."
					} else {
						this.datasets = this.datasets.concat(response.data.results)
						this.bottomMessage = ""
						// update offset to next new page
						this.offset = this.offset + this.limit
					}

					this.lastDatasetRequestCompleted = true
				}).catch((err) => {
					console.log(err)
					this.bottomMessage = "Something went wrong :/"
				})
			}
		},

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

	created (){

		let params = {
			query: this.$route.query.query, 
			tasks: this.$route.query.tasks, 
			topics: this.$route.query.topics, 
			data_types: this.$route.query.data_types,
		}
			
		// Clean params object
		for (const key of Object.keys(params)) {
			if (params[key] == undefined) {
				delete params[key]
			} 
		}

		this.getDatasets(params)
	},



	mounted () {
  		this.scroll()
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

	#bottom-message {
		text-align: center;
	}

</style>
