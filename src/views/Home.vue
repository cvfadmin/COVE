<template>
	<div class="home container">
		<PageHeader></PageHeader>
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
			<DatasetList></DatasetList>
		</section>

	</div>
</template>

<script>
import PageHeader from '@/components/PageHeader.vue'
import IntroText from '@/components/home/IntroText.vue'
import DatasetList from '@/components/datasets/DatasetList.vue'
import ModelMultiSelect from '@/components/tags/ModelMultiSelect'
import DatasetService from '@/services/DatasetService'
import {removeEmptyProps} from '@/utils/misc.js'
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
			searchTags: {
				tasks: [],
				topics: [],
				dataTypes: [],
			},
		}
	},

	computed: {
		tags () {
			return this.$store.state.tags
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
	},


	methods: {
		search() {
			if (this.searchInput.length < 3 && this.searchInput.length > 0) {
				alert('Search query must be at least three characters long.')
				return
			}

			let params = {
				query: this.searchInput, 
				tasks: this.searchTags.tasks.map((item) => item.name), 
				topics: this.searchTags.topics.map((item) => item.name), 
				data_types: this.searchTags.dataTypes.map((item) => item.name),
			}
			
			this.$store.dispatch('searchDatasets', params)
			params = removeEmptyProps(params)
			router.push({ path: '/', query: params})
		},

		updateTags (taglist, category) {
			this.searchTags[category] = taglist
		},
	},

	created(){
		this.$store.commit('loadTags')
	},
}
</script>

<!-- Add "scoped" attribute to limit SCSS to this component only -->
<style scoped lang="scss">

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