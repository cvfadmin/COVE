<template>
	<div class="edit-dataset container">
		<PageHeader></PageHeader>
		<DatasetForm 
			v-if="dataset && tags" 
			:dataset="dataset"
			:tags="tags"
			:formData="formData" 
			:errors="errors" 
			@submitEvent="handleSubmit">
		</DatasetForm>
	</div>
</template>

<script>
import ModelMultiSelect from '@/components/tags/ModelMultiSelect'
import DatasetForm from '@/components/datasets/DatasetForm'
import DatasetService from '@/services/DatasetService'
import PageHeader from '@/components/PageHeader'
import router from '@/router'


export default {
	name: 'createDataset',
	components: {
		ModelMultiSelect,
		PageHeader,
		DatasetForm
	},

	data () {
		return {
			dataset: null,
			tags: null,
			formData: {},
			errors: {},
		}
	},

	methods: {

		async handleSubmit(updatedTags) {
			// Seperate previously created tags from new tags
			let oldTags = updatedTags.filter((item) => item.new == undefined)
			let newTags = updatedTags.filter((item) => item.new != undefined)
			newTags = newTags.map((item) => {
				return {"name": item.name, "category": item.category}
			})
			
			this.createTags(newTags).then((response) => {
				this.formData.tags = oldTags.concat(response.data.new).map((item) => { return item.id })
				
				this.updateDataset(this.$route.params.id, this.formData).then((response) => {
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
						
						alert("Your dataset has been updated");
						router.push({path: '/datasets/' + this.dataset.id})
					
					} else {
						// Some weird error
						alert("Oops something went wrong :/ - Please email cove@thecvf.com if error persists.")
						console.log(response)
					}
				})
			}) 
		},

		async getTags() {
			await DatasetService.getTags().then((response) => {
				this.tags = response.data.results
			})
		},

		async createTags (list) {
			return await DatasetService.createManyTags(list)
		},

		async updateDataset(d_id, data) {
			return await DatasetService.updateDataset(d_id, data)
		},
	},

	async created () {
		await DatasetService.getDatasetById(this.$route.params.id).then((response) => {
			this.dataset = response.data.result

			// TODO: better way to handle these permissions?
			if (!this.$store.state.isAdmin && this.$store.state.userId != this.dataset.owner) {
				this.$router.push({
					name: 'login',
					params: { error: 'You must be logged in as the owner to edit this dataset' },
				})
			}

			this.formData = {
				name: this.dataset.name,
				url: this.dataset.url,
				description: this.dataset.description,
				year_created: this.dataset.year_created,
				size: this.dataset.size,
				num_cat: this.dataset.num_cat,
				thumbnail: this.dataset.thumbnail,
				citation: this.dataset.citation,
			}
		})

		this.getTags()
	}
}
</script>


<style scoped lang="scss">

</style>

