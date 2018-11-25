<template>
	<div class="add-dataset container">
		<PageHeader></PageHeader>
		<h2>Delete Request for {{dataset.name}}</h2>
		<form v-on:submit.prevent="handleSubmit">
			<div class="input-group">
				
				<div class="input-head">
					<p>First Name*:</p>
					<p class="error">{{errors.first_name}}</p>
				</div>
				<input type="text" v-model="formData.first_name" >
				
				<div class="input-head">
					<p>Last Name*:</p>
					<p class="error">{{errors.last_name}}</p>
				</div>
				<input type="text" v-model="formData.last_name" >
				
				<div class="input-head">
					<p>Email Address*:</p>
					<p class="error">{{errors.email}}</p>
				</div>
				<input type="email" v-model="formData.email" >
				
				<div class="input-head">
					<p>Reason dataset should be removed*:</p>
					<p class="error">{{errors.reason}}</p>
				</div>
				<textarea v-model="formData.reason"></textarea>
			</div>
			<div class="input-group">
				<button type="submit">Submit</button>
			</div>
		</form>
	</div>
</template>

<script>
import PageHeader from '@/components/PageHeader.vue'
import DatasetService from '@/services/DatasetService'
import router from '@/router'

export default {
	name: 'deleteDataset',
	components: {
		PageHeader,
	},

	props: {
		datasetName: String,
	},

	data: function () {
		return {
			dataset: {},
			formData: {},
			errors: {
				first_name: '',
				last_name: '',
				email: '',
				reason: ''
			}
		}
	},

	methods: {
		async handleSubmit () {
			// Assign to dataset
			this.formData.dataset = this.$route.params.id

			this.createEditDSRequest(this.formData).then((response) => {
				if (response.data.errors != undefined && response.status == 200) {
					// Show validation errors
					let errors = response.data.errors
					Object.keys(errors).forEach((key, idx) => {
						this.errors[key] = errors[key].join(" - ")
					})

				} else if (response.status == 200) {
					// Created successfully
					let self = this;
					Object.keys(this.formData).forEach(function(key,index) {
					    self.formData[key] = '';
					});
						
					alert("Thank you for your contribution! You can expect an email soon if your request to edit this dataset is approved.")
					router.push({ name: 'home' })
					
				} else {
					// Some weird error
					alert("Oops something went wrong :/ - Please email cove@thecvf.com if error persists.")
					console.log(response)
				}
			})
		},

		async createEditDSRequest (data) {
			return await DatasetService.createDeleteDSRequest(data)
		},

		async getDataset () {
			// TODO: Check for dataset in store before sending another request
			const response = await DatasetService.getDatasetById(this.$route.params.id)
			this.dataset = response.data.result
		},
	},

	beforeMount(){
		this.getDataset()
	},
}
</script>

<!-- Add "scoped" attribute to limit SCSS to this component only -->
<style scoped lang="scss">

h2 {
	font-family: 'Vollkorn', serif;
	font-weight: 400;
	font-size: 32px;
}

form {
	margin-top: 25px;
}

</style>
