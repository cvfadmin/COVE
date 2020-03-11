<template>
	<form v-on:submit.prevent="handleSubmit">
		<div class="input-group">		
			<div class="input-head">
				<p>Please describe what you would like the owner of this dataset to edit:</p>
				<p class="error">{{errors.content}}</p>
			</div>
			<textarea v-model="formData.content" placeholder="This message will be sent to the owner." required></textarea>

		</div>
		<div class="input-group">
			<button type="submit">Submit</button>
		</div>
	</form>
</template>

<script>
import PageHeader from '@/components/PageHeader.vue'
import DatasetService from '@/services/DatasetService'
import router from '@/router'

export default {
	name: 'editRequestForm',
	components: {
		PageHeader,
	},

	data: function () {
		return {
			formData: {},
			errors: {
				content: ''
			}
		}
	},

	methods: {
		async handleSubmit () {
			this.formData.author = this.$store.state.userId

			this.createRequest(this.formData).then((response) => {
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
						
					alert("Your message has been sent.")
					router.go()
					
				} else {
					// Some weird error
					alert("Oops something went wrong :/ - Please email cove@thecvf.com if error persists.")
					console.log(response)
				}
			})
		},

		async createRequest (data) {
			return await DatasetService.createEditRequest(this.$route.params.id, data)
		}
	},
}
</script>


<style scoped lang="scss">

form {
	margin-top: 0;
}

</style>
