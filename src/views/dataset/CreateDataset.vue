<template>
	<div class="create-dataset container">
		<PageHeader></PageHeader>
		<div class="form-container">
			<DatasetForm 
				v-if="tags"
				:tags="tags"
				:formData="formData" 
				:errors="errors" 
				@submitEvent="handleSubmit">
			</DatasetForm>	
		</div>
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
			tags: null,
			formData: {},
			errors: {}
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
				this.formData.tags = oldTags.concat(response.data.new).map((item) => item.id)
				
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

		async createTags (list) {
			return await DatasetService.createManyTags(list)
		},

		async createDataset(data) {
			return await DatasetService.createDataset(data)
		},

		async getTags() {
			await DatasetService.getTags().then((response) => {
				this.tags = response.data.results
			})
		},
	},

	created () {
		this.getTags()
	}
}
</script>


<style scoped lang="scss">

.form-container {
}

</style>
