<template>
	<div class="create-dataset container">
		<PageHeader></PageHeader>
		<Promised :promise="tagsPromise">
			<!-- Use the "pending" slot to display a loading message -->
			<template v-slot:pending>
				<p>Loading...</p>
			</template>
			<!-- The default scoped slot will be used as the result -->
			<template v-slot="data">
				<div class="form-container">
					<DatasetForm 
						:tags="data.data.results"
						:formData="formData" 
						:errors="errors" 
						@submitEvent="handleSubmit">
					</DatasetForm>	
				</div>
			</template>
			<!-- The "rejected" scoped slot will be used if there is an error -->
			<template v-slot:rejected="error">
				<p>Error: {{ error.message }}</p>
			</template>
		</Promised>
	 </div>
</template>

<script>
import ModelMultiSelect from '@/components/tags/ModelMultiSelect'
import DatasetForm from '@/components/datasets/DatasetForm'
import DatasetService from '@/services/DatasetService'
import PageHeader from '@/components/PageHeader'
import router from '@/router'
import { Promised } from 'vue-promised'


export default {
	name: 'createDataset',
	components: {
		ModelMultiSelect,
		PageHeader,
		DatasetForm,
		Promised
	},

	data () {
		return {
			tagsPromise: null,
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
	},

	created () {
		this.tagsPromise = DatasetService.getTags()
	}
}
</script>


<style scoped lang="scss">

.form-container {
}

</style>
