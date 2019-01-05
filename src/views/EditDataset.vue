<template>
	<div class="edit-dataset container">
		<PageHeader></PageHeader>
		<DatasetForm 
			:dataset="dataset" 
			:formData="formData" 
			:errors="errors" 
			@submitEvent="handleSubmit()">
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
			dataset: {},
			formData: {},
			errors: {},
		}
	},

	methods: {
		async getDataset () {
			// Check for dataset in store before sending another request
			let thisDSId = this.$route.params.id
			let storedDS = this.$store.state.datasets.find((item) => { return item.id == thisDSId })

			if (storedDS == undefined) {
				const response = await DatasetService.getDatasetById(thisDSId)
				this.dataset = response.data.result
			} else {
				this.dataset = storedDS
			}
		},

		async handleSubmit() {
			let selectedTags = this.$store.state.selectedTags
			let oldTags = selectedTags.filter((item) => item.new == undefined)
			
			let newTags = selectedTags.filter((item) => item.new != undefined)
			newTags = newTags.map((item) => {
				return {"name": item.name, "category": item.category}
			})
			
			this.createTags(newTags).then((response) => {
				this.formData.tags = oldTags.concat(response.data.new).map((item) => { return item.id })
				
				this.updateDataset(this.$route.params.id, this.formData).then((response) => {
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
						
						alert("Your dataset has been updated");
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

		async updateDataset(d_id, data) {
			return await DatasetService.updateDataset(d_id, data)
		},
	},

	beforeMount () {
		this.getDataset()
		this.$store.commit('loadTags')

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
	}
}
</script>


<style scoped lang="scss">

</style>

