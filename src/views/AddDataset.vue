<template>
	<div class="add-dataset container">
		<PageHeader></PageHeader>
		<form v-on:submit.prevent="handleSubmit">
			<div class="input-group">
				
				<div class="input-head">
					<p>First Name*:</p>
					<p class="error">{{errors.first_name}}</p>
				</div>
				<input type="text" v-model="formData.first_name" required>
				
				<div class="input-head">
					<p>Last Name*:</p>
					<p class="error">{{errors.last_name}}</p>
				</div>
				<input type="text" v-model="formData.last_name" required>
				
				<div class="input-head">
					<p>Email Address*:</p>
					<p class="error">{{errors.email}}</p>
				</div>
				<input type="email" v-model="formData.email" required>
				
				<div class="input-head">
					<p>Dataset Name*:</p>
					<p class="error">{{errors.dataset_name}}</p>
				</div>
				<input type="text" v-model="formData.dataset_name" required>
				
				<div class="input-head">
					<p>Year Created*:</p>
					<p class="error">{{errors.year}}</p>
				</div>
				<input type="text" v-model="formData.year" required>
				
				<div class="input-head">
					<p>Introduce yourself*:</p>
					<p class="error">{{errors.intro}}</p>
				</div>
				<textarea v-model="formData.intro" required></textarea>
				
				<div class="input-head">
					<p>Link to Dataset*:</p>
					<p class="error">{{errors.url}}</p>
				</div>
				<input type="url" v-model="formData.url" required>

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
	name: 'addDataset',
	components: {
		PageHeader,
	},

	data: function () {
		return {
			formData: {},
			errors: {
				first_name: '',
				last_name: '',
				email: '',
				dataset_name: '',
				year: '',
				intro: '',
				url: '',
			}
		}
	},

	methods: {
		async handleSubmit () {
			this.createAddDSRequest(this.formData).then((response) => {
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
						
					alert("Thank you for your contribution! You can expect an email soon if your request to add a dataset is approved.")
					router.push({ name: 'home' })
					
				} else {
					// Some weird error
					alert("Oops something went wrong :/ - Please email cove@thecvf.com if error persists.")
					console.log(response)
				}
			})
		},

		async createAddDSRequest (data) {
			return await DatasetService.createAddDSRequest(data)
		}
	},
}
</script>

<!-- Add "scoped" attribute to limit SCSS to this component only -->
<style scoped lang="scss">

form {
	margin-top: 25px;
}

</style>
