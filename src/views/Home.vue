<template>
	<div class="home container">
		<PageHeader></PageHeader>
		<IntroText></IntroText>
		
		<form id="filters" v-on:submit.prevent="search()">
			<div class="filter-bars">
				<div class="input-group">
					<p>Search Terms:</p>
					<input v-model="searchInput" type="search" placeholder="ex. trees, cars, birds">
				</div>
			</div>

			<div id="tags">
				<div class="input-group">
					<p>Tasks:</p>
					<ModelMultiSelect :models="tasks" :category="'tasks'" :createNew="false"></ModelMultiSelect>
				</div>
				
				<div class="input-group">
					<p>Topics:</p>
					<ModelMultiSelect :models="topics" :category="'topics'" :createNew="false"></ModelMultiSelect>
				</div>
				
				<div class="input-group">
					<p>Data Types:</p>
					<ModelMultiSelect :models="dataTypes" :category="'data_types'" :createNew="false"></ModelMultiSelect>
				</div>

				<div class="input-group submit-button">
					<button type="submit" class="card-wrapper">Search</button>
				</div>
			</div>
		</form>

		<section id="datasets">
			<DatasetList></DatasetList>
		</section>

	</div>
</template>

<script>
// @ is an alias to /src
import PageHeader from '@/components/PageHeader.vue'
import IntroText from '@/components/home/IntroText.vue'
import DatasetList from '@/components/datasets/DatasetList.vue'
import ModelMultiSelect from '@/components/tags/ModelMultiSelect'
import DatasetService from '@/services/DatasetService'
import router from '@/router'

export default {
	name: 'home',
	components: {
		PageHeader,
		IntroText, 
		DatasetList,
		ModelMultiSelect,
	},

	data () {
		return {
			searchInput: '',
		}
	},

	computed: {
		tags () {
			return this.$store.state.tags
		},

		tasks () {
			return this.tags.filter((item) => {
				return item.category == 'tasks'
			})
		},

		topics () {
			return this.tags.filter((item) => {
				return item.category == 'topics'
			})
		},

		dataTypes () {
			return this.tags.filter((item) => {
				return item.category == 'data_types'
			})
		},

		selectedTags () {
			return this.$store.state.selectedTags
		},

		selectedTasks () {
			return this.selectedTags.filter((item) => {
				return item.category == 'tasks'
			}).map((item) => {
				return item.name
			})
		},

		selectedTopics () {
			return this.selectedTags.filter((item) => {
				return item.category == 'topics'
			}).map((item) => {
				return item.name
			})
		},

		selectedDataTypes () {
			return this.selectedTags.filter((item) => {
				return item.category == 'data_types'
			}).map((item) => {
				return item.name
			})
		}
	},


	methods: {
		search() {

			let params = {
				query: this.searchInput, 
				tasks: this.selectedTasks, 
				topics: this.selectedTopics, 
				data_types: this.selectedDataTypes
			}
			
			this.$store.dispatch('searchDatasets', params)
			
			// Clean params object
			for (const key of Object.keys(params)) {
				if (params[key].length == 0) {
					delete params[key]
				}
			}

			router.push({ path: '/', query: params})
		},
	},

	beforeMount(){
		this.$store.commit('loadTags')
		this.$store.dispatch('clearSelectedTags')
	},
}
</script>

<!-- Add "scoped" attribute to limit SCSS to this component only -->
<style scoped lang="scss">

#filters {

	.filter-bars {
		display: flex;
		justify-content: space-between;

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