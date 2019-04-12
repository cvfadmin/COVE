<template>
	<div class="dataset-form">
		<form v-on:submit.prevent="triggerSubmit">
			<div class="input-group">
				
				<div class="input-head">
					<p>Dataset name*:</p>
					<p class="error">{{errors.name}}</p>
				</div>
				<input type="text" v-model="formData.name" required>
					
				<div class="input-head">
					<p>Url to dataset*:</p>
					<p class="error">{{errors.url}}</p>
				</div>
				<input type="url" v-model="formData.url" required>
					
				<div class="input-head">
					<p>Description of dataset*:</p>
					<p class="error">{{errors.description}}</p>
				</div>
				<textarea v-model="formData.description" required></textarea>
					
				<div class="input-head">
					<p>Year created:</p>
					<p class="error">{{errors.year_created}}</p>
				</div>
				<input type="text" v-model="formData.year_created">
					
				<div class="input-head">
					<p>Size of dataset:</p>
					<p class="error">{{errors.size}}</p>
				</div>
				<input type="text" v-model="formData.size">
					
				<div class="input-head">
					<p>Number of categories:</p>
					<p class="error">{{errors.num_cat}}</p>
				</div>
				<input type="text" v-model="formData.num_cat">
					
				<div class="input-head">
					<p>Thumbnail image link:</p>
					<p class="error">{{errors.thumbnail}}</p>
				</div>
				<input type="url" v-model="formData.thumbnail">
					
				<div class="input-head">
					<p>Citation of paper dataset was published in*:</p>
					<p class="error">{{errors.citation}}</p>
				</div>
				<textarea v-model="formData.citation" required></textarea>
					
				<div class="tags">
					<div class="tasks">
						<p>Tasks:</p>
						<div id="select-tags">
							<ModelMultiSelect 
							:models="tasks" 
							:category="'tasks'" 
							:createNew="true" 
							:currentTags="selectedTasks"
							v-on:changedTags="updateTags">
							</ModelMultiSelect>
						</div>
					</div>

					<div class="topics">
						<p>Topics:</p>
						<div id="select-tags">
							<ModelMultiSelect 
							:models="topics" 
							:category="'topics'" 
							:createNew="true" 
							:currentTags="selectedTopics"
							v-on:changedTags="updateTags">
							</ModelMultiSelect>
						</div>
					</div>

					<div class="data-types">
						<p>Data Types:</p>
						<div id="select-tags">
							<ModelMultiSelect
							v-if="dataset.tags"
							:models="dataTypes" 
							:category="'data_types'" 
							:createNew="true" 
							:currentTags="selectedDataTypes"
							v-on:changedTags="updateTags">
							</ModelMultiSelect>
						</div>
					</div>
				</div>
			
			</div>
			<div class="input-group">
				<button type="submit">Submit</button>
			</div>
		</form>
	</div>
</template>

<script>
import ModelMultiSelect from '@/components/tags/ModelMultiSelect'
import DatasetService from '@/services/DatasetService'
import router from '@/router'


export default {
	name: 'datasetForm',
	components: {
		ModelMultiSelect,
	},

	props: {
		tags: Array,
		dataset: {
			type: Object,
			default: () => {return {tags: []}}
		},
		errors: Object,
		formData: Object,
	},

	data () {
		return {
			updatedTags: this.dataset.tags
		}
	},

	computed: {

		tasks () {
			return this.tags.filter((item) => item.category == 'tasks')
		},

		topics () {
			return this.tags.filter((item) => item.category == 'topics')
		},

		dataTypes () {
			return this.tags.filter((item) => item.category == 'data_types')
		},

		selectedTasks () {
			return this.filterTagsByThisDS(this.tasks)
		},

		selectedTopics () {
			return this.filterTagsByThisDS(this.topics)
		},

		selectedDataTypes () {
			return this.filterTagsByThisDS(this.dataTypes)
		}

	},

	methods: {

		triggerSubmit () {
			if (!this.validateData()) { return }
			this.$emit('submitEvent', this.updatedTags)
		},

		updateTags (taglist, category) {
			// Remove all tags of same category then add taglist
			this.updatedTags = this.updatedTags.filter((item) => item.category != category).concat(taglist)
		},

		validateData () {
			if (this.formData.thumbnail == '' || this.formData.thumbnail == undefined) {return true}
			let whitelist = ['jpg', 'gif', 'png', 'jpeg']
			let thumbnailExtension = this.formData.thumbnail.split('.').pop()
			
			if (whitelist.indexOf(thumbnailExtension) == -1) {
				this.errors.thumbnail = "Only urls with extensions of: jpg, jpeg, png, and gif are permitted. Leave blank if you have no such link for your dataset."
				return false
			}
			return true
		},

		filterTagsByThisDS(taglist) {
			let ret = []
			for(var i in taglist){
				Array.from(taglist[i].datasets).forEach((item) => {
					if (item == this.$route.params.id) {
						ret.push(taglist[i])
					} 
				})
			}
			return ret
		}
	},
}
</script>

<style scoped lang="scss">

	form {
		margin-top: 40px;

		#select-tags .dropdown {
			margin-top: 10px;
			width: calc(100% - 30px);
			font-family: 'Open Sans', sans-serif;
			font-size: 12px;
			color: #000;
			border-color: #000;
			border-radius: 0;
			padding-top: 8px;

			.label {
				background: none;
			}

			.menu {
				color: #000;
				border-color: #000;
				border-radius: 0;
				font-size: 12px;
			}
			
			.visible {
				border-color: #000;
			}
		}

		.tags {
			div {
				margin-bottom: 10px;
			}
		}
	}

</style>
