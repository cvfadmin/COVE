<template>
	<div class="create-dataset container">
		<h1>Create your dataset entry</h1>

		<form v-on:submit.prevent="handleSubmit">
			<div class="input-group">
				
				<div class="input-head">
					<p>Contact name*:</p>
					<p class="error">{{errors.contact_name}}</p>
				</div>
				<input type="text" v-model="formData.contact_name" required>
				
				<div class="input-head">
					<p>Contact email*:</p>
					<p class="error">{{errors.contact_email}}</p>
				</div>
				<input type="email" v-model="formData.contact_email" required>
				
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
					<p>Thumbnail/Image link:</p>
					<p class="error">{{errors.thumbnail}}</p>
				</div>
				<input type="url" v-model="formData.thumbnail">
				
				<div class="input-head">
					<p>Citation of paper dataset was published in*:</p>
					<p class="error">{{errors.citation}}</p>
				</div>
				<input type="text" v-model="formData.citation" required>
				
				<div class="tags">
					<div class="tasks">
						<p>Tasks:</p>
						<div id="select-tags">
							<ModelMultiSelect :models="tasks" :category="'tasks'" :createNew="true"></ModelMultiSelect>
						</div>
					</div>

					<div class="topics">
						<p>Topics:</p>
						<div id="select-tags">
							<ModelMultiSelect :models="topics" :category="'topics'" :createNew="true"></ModelMultiSelect>
						</div>
					</div>

					<div class="data-types">
						<p>Data Types:</p>
						<div id="select-tags">
							<ModelMultiSelect :models="dataTypes" :category="'data_types'" :createNew="true"></ModelMultiSelect>
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
	name: 'createDataset',
	components: {
		ModelMultiSelect
	},

	data: function () {
		return {
			formData: {},
			tags: [],
			errors: {
				contact_name: '',
				contact_email: '',
				name: '',
				url: '',
				description: '',
				year_created: '',
				size: '',
				num_cat: '',
				thumbnail: '',
				citation: ''
			}
		}
	},

	computed: {
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
		}
	},

	methods: {

		async getTags() {
			const response = await DatasetService.getTags()
			this.tags = response.data.results
		},

		async handleSubmit() {
			let selectedTags = this.$store.state.selectedTags
			let oldTags = selectedTags.filter((item) => item.new == undefined)
			
			let newTags = selectedTags.filter((item) => item.new != undefined)
			newTags = newTags.map((item) => {
				return {"name": item.name, "category": item.category}
			})
			
			console.log('Data being passed:')
			console.log(newTags)
			this.createTags(newTags).then((response) => {
				this.formData.tags = oldTags.concat(response.data.new)
				this.formData.key = this.$route.params.key // Add key
				
				this.createDataset(this.formData).then((response) => {
					console.log(response)
					if (response.data.errors != undefined && response.status == 200) {
						// Show validation errors
						let errors = response.data.errors
						Object.keys(errors).forEach((key, idx) => {
							console.log('Missing tag key: ' + key)
							this.errors[key] = errors[key].join(" - ")
						})

					} else if (response.status == 200) {
						// Created successfully
						let self = this;
						Object.keys(this.formData).forEach(function(key,index) {
						    self.formData[key] = '';
						});
						
						alert("Thank you for your contribution! You can expect an email soon if your dataset is approved. You may close this page now.");
						router.push({ name: 'home' })
					
					} else {
						// Some weird error
						alert("Oops something went wrong :/ - Please email cove@thecvf.com if error persists.")
						console.log(response)
					}
				})
			}) 
		},

		async createTags(list) {
			return await DatasetService.createManyTags(list)
		},

		async createDataset(data) {
			return await DatasetService.createDataset(data)
		},
	},

	beforeMount(){
		this.getTags()
		this.$store.dispatch('clearSelectedTags')
	},
}
</script>

<!-- Add "scoped" attribute to limit SCSS to this component only -->
<style scoped lang="scss">
	
	h1 {
		border-bottom: 1px #000 solid;
	}

	form {

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
