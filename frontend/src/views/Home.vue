<template>
	<div class="home container">
		<PageHeader v-on:push-home="clearSearch"></PageHeader>
		<IntroText></IntroText>
		
		<form id="filters" v-on:submit.prevent="search()">
			<div class="filter-bars">
				<div class="input-group">
					<p>Search Terms:</p>
					<div class="button-and-input card-wrapper">
						<input v-model="searchInput" type="search" placeholder="ex. trees, cars, birds">
						<button type="submit">Search</button>
					</div>
				</div>
			</div>

			<div id="tags">
				<div class="input-group">
					<p>Tasks:</p>
					<ModelMultiSelect :models="tasks" :category="'tasks'" :createNew="false" v-on:changedTags="updateTags"></ModelMultiSelect>
				</div>
				
				<div class="input-group">
					<p>Topics:</p>
					<ModelMultiSelect :models="topics" :category="'topics'" :createNew="false" v-on:changedTags="updateTags"></ModelMultiSelect>
				</div>
				
				<div class="input-group">
					<p>Data Types:</p>
					<ModelMultiSelect :models="dataTypes" :category="'data_types'" :createNew="false" v-on:changedTags="updateTags"></ModelMultiSelect>
				</div>

			</div>
		</form>

		<section id="datasets">
			<p class="num-results" v-if="searchInput == '' && totalNumSearchTags == 0">
				There are {{ totalNumResults }} datasets in COVE (showing {{numPageResults}}):
			</p>
			<p class="num-results" v-else>
				There are {{ totalNumResults }} datasets that match your query (showing {{numPageResults}}):
			</p>

			<DatasetList :datasets="datasets"></DatasetList>
		</section>
		
		<Pagination ref="pagination" v-on:next="pushNextPage" v-on:previous="pushPreviousPage"></Pagination>

	</div>
</template>

<script>
import PageHeader from '@/components/PageHeader.vue'
import IntroText from '@/components/home/IntroText.vue'
import Pagination from '@/components/home/Pagination.vue'
import DatasetList from '@/components/datasets/DatasetList.vue'
import ModelMultiSelect from '@/components/tags/ModelMultiSelect'
import DatasetService from '@/services/DatasetService'
import miscFunctions from '@/utils/misc.js'
import router from '@/router'

export default {
	name: 'home',
	components: {
		PageHeader,
		IntroText,
		Pagination, 
		DatasetList,
		ModelMultiSelect,
	},

	data () {
		return {
			searchInput: '',
			datasets: [],
			limit: 25,  // Datasets per page - offset is computed from page query param
			totalNumResults: null,
			numPageResults: null,
		}
	},

	computed: {
		tags () {
			return this.$store.state.tags
		},

		totalNumSearchTags () {
			return this.$store.state.searchTags.tasks.length + this.$store.state.searchTags.topics.length + this.$store.state.searchTags.dataTypes.length
		},

		tasks () {
			return this.tags.filter((item) => item.category == 'tasks')
		},

		topics () {
			return this.tags.filter((item) => item.category == 'topics')
		},

		dataTypes () {
			return this.tags.filter((item) => item.category == 'data_types')
		},

		page () {
			return this.$route.query.page || 1
		},
	},


	methods: {
		search() {
			if (this.searchInput.length < 3 && this.searchInput.length > 0) {
				alert('Search query must be at least three characters long.')
				return
			}
			// Go to 1st page after searching
			this.pushToNewPage(1)
		},

		updateTags(taglist, category) {
			if (category == "data_types") {
				this.$store.commit('setDataTypesSearchTags', taglist);
			} else if (category == "topics") {
				this.$store.commit('setTopicsSearchTags', taglist);
			} else {
				this.$store.commit('setTasksSearchTags', taglist);
			}

			// Update search results!
			this.search()
		},

		pushToNewPage(page) {
			/* Preserve current params but new page */
			let params = miscFunctions.cleanParams({
				query: this.searchInput, 
				tasks: this.$store.state.searchTags.tasks.map((item) => item.name), 
				topics: this.$store.state.searchTags.topics.map((item) => item.name), 
				data_types: this.$store.state.searchTags.dataTypes.map((item) => item.name),
				page: page,
			})
			
			// Update route parameters so reload provides same results
			this.$router.push({ path: '/', query: params})
			
			// Load datasets
			this.getDatasets(params)
		},

		pushNextPage() {
			this.pushToNewPage(parseInt(this.page) + 1)
		},

		pushPreviousPage() {
			// TODO: Add logic of when there is no previous page
			this.pushToNewPage(parseInt(this.page) - 1)
		},

		clearSearch() {
			// Reset the search bar and tags
			this.searchInput = ''
			
			this.$store.commit('setDataTypesSearchTags', []);
			this.$store.commit('setTopicsSearchTags', []);
			this.$store.commit('setTasksSearchTags', []);

			this.search()
		},

		// Get datasets to display, then set params for the next page.
		async getDatasets (params) {
			params.offset = parseInt(this.limit) * (params.page - 1)
			params.limit = this.limit

			await DatasetService.searchDatasets(params).then((response) => {
				this.totalNumResults = response.data.num_total_results
				this.numPageResults = response.data.num_page_results
				this.datasets = response.data.results
				
				// Logic for which pagination buttons should be show
				if (this.page == 1) {
					this.$refs.pagination.hidePrevious = true
				} else {
					this.$refs.pagination.hidePrevious = false
				}
				
				if ((parseInt(params.offset) + parseInt(this.limit)) >= parseInt(this.totalNumResults)) {
					this.$refs.pagination.hideNext = true
				} else {
					this.$refs.pagination.hideNext = false
				}

			}).catch((err) => {
				console.log(err)
				alert("Something went wrong :/ - can't load more datasets.")
			})
		}
	},

	created () {
		this.$store.commit('loadTags')
	},

	mounted () {
		let params = {
			query: this.$route.query.query, 
			tasks: this.$route.query.tasks, 
			topics: this.$route.query.topics, 
			data_types: this.$route.query.data_types,
			page: this.page,
		}
		
		if (this.page == 1) {
			this.$refs.pagination.hidePrevious = true
		} else {
			this.$refs.pagination.hidePrevious = false
		}

		this.getDatasets(params)
	}
}
</script>

<!-- Add "scoped" attribute to limit SCSS to this component only -->
<style scoped lang="scss">

.num-results {
	font-size: 14px;
	font-weight: 700;
}

#filters {

	.filter-bars {
		display: flex;
		justify-content: space-between;

		.button-and-input {
			display:flex;
			margin: 10px 0;
			padding: 0;

			input {
				flex-grow:2;
				/* And hide the input's outline, so the form looks like the outline */
				border:none;
				box-shadow: none;
				outline: none;
				margin: 0;
			}

			button {
				margin: 0;
				border: none;
				padding: 10px 15px;
				border-top-right-radius: 3px;
				border-bottom-right-radius: 3px;
				background: #525252;
				color: #eee;
				font-weight: 600;
			}
		}

		.input-group:first-child {
			flex: 1;
		}

		.input-group { 
			/* Assumes a p elem and an input elem */
			display: flex;
			flex-direction: column;
		}
	}

	#tags {
		display: flex;
		
		.input-group {
			margin-left: 15px;
			max-width: 220px;
			display: flex;
			flex-wrap: wrap;
		}

		.input-group:first-child {
			margin-left: 0;
		}

		.submit-button {
			width: -webkit-fill-available;
			max-width: none;
			display: flex;
			justify-content: flex-end;

			button {
				border-radius: 2px;
				background: #525252;
				color: #fff;
				padding: 5px 10px;
				border: none;
				margin: 0;
				text-transform: uppercase;
				font-weight: 600;
			}
		}
	}

}

</style>
