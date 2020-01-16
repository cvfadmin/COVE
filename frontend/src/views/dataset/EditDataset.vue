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
	name: 'editDataset',
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
			this.formData.tags = updatedTags

			this.updateDataset(this.$route.params.id, this.formData).then((response) => {
				if (response.data.errors != undefined && response.status == 200) {
					// Show validation errors
					let errors = response.data.errors
					Object.keys(errors).forEach((key, idx) => {
						console.log('Missing tag key: ' + key)
						this.errors[key] = errors[key].join(" - ")
					})
					alert('Please check over your responses for errors!')

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
					alert("Oops something went wrong :/ -  If error persists email cove@thecvf.com.")
					console.log(response)
					// Show submit button again
					this.$refs.datasetForm.hideSubmitButton = false
				}
				
			}).catch((response, y) => {
				alert("Oops something went wrong :/ -  If error persists email cove@thecvf.com.")
				console.log(response)
				// Show submit button again
				this.$refs.datasetForm.hideSubmitButton = false
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
				cite_year: this.dataset.cite_year,
				cite_venue: this.dataset.cite_venue,
				cite_authors: this.dataset.cite_authors,
				cite_title: this.dataset.cite_title,
			}
		})

		this.getTags()
	}
}
</script>


<style scoped lang="scss">

</style>

