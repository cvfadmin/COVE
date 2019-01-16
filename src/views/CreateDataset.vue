<template>
	<div class="create-dataset container">
		<PageHeader></PageHeader>
		<div class="form-container">
			<DatasetForm 
				:dataset="undefined" 
				:formData="formData" 
				:errors="errors" 
				@submitEvent="handleSubmit()">
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
			formData: {},
			errors: {}
		}
	},

	methods: {
		async handleSubmit() {
			let selectedTags = this.$store.state.selectedTags
			let oldTags = selectedTags.filter((item) => item.new == undefined)
			
			let newTags = selectedTags.filter((item) => item.new != undefined)
			newTags = newTags.map((item) => {
				return {"name": item.name, "category": item.category}
			})
			
			this.createTags(newTags).then((response) => {
				this.formData.tags = oldTags.concat(response.data.new)
				
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
	}
}
</script>


<style scoped lang="scss">

.form-container {
	width: 800px;
	margin: 0 auto;
}

</style>
