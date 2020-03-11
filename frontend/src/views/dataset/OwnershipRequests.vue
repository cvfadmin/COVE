<template>
	<div class="ownership-requests container">
		<PageHeader></PageHeader>
		<section id="create-new">
			<h3>Create a New Ownership Request:</h3>
            <p><i>Please Note:</i> We will transfer ownership of datasets to users that can verify that they are associated with this dataset (e.g. dataset author, maintainer, etc.). <strong>After filling out this form expect an email from the COVE administrators (cove@thecvf.com)</strong> who may ask for additional verification information. Thank you for contributing to COVE! </p>
			<form v-on:submit.prevent="handleSubmit">
                <div class="input-group">
                    <div class="input-head">
                        <p>Please describe your association with this dataset:</p>
                        <p class="error">{{errors.content}}</p>
                    </div>
                    <textarea v-model="formData.content" placeholder="This message will be sent to the adminstrators." required></textarea>

                </div>
                <div class="input-group">
                    <button type="submit">Submit</button>
                </div>
            </form>
		</section>
	</div>
</template>

<script>
import PageHeader from '@/components/PageHeader'
import DatasetService from '@/services/DatasetService'
import router from '@/router'

export default {
	name: 'datasetEditRequests',
	components: {
		PageHeader,
	},

	data () {
		return {
            dataset: {},
            formData: {},
            errors: {
                content: '',
                preferredEmail: ''
            }
		}
	},

	methods: {

		async handleSubmit () {
			this.formData.author = this.$store.state.userId

			this.createOwnershipRequest(this.formData).then((response) => {
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
						
					alert("Your ownership request has been submitted.")
					router.push({name: "home"})
					
				} else {
					// Some weird error
					alert("Oops something went wrong :/ - Please email cove@thecvf.com if error persists.")
					console.log(response)
				}
			})
        },

        async createOwnershipRequest (data) {
			return await DatasetService.createOwnershipRequest(this.$route.params.id, data)
		}
        
	},

}
</script>


<style scoped lang="scss">

h3 {
    font-family: 'Vollkorn', serif;
    font-weight: 500;
}

.null-message {
	text-align: center;
}

#create-new {
    p {
        font-size: 12px;
    }
}

form {
	display: flex;
	flex-direction: column;
	margin-top: 25px;
}

</style>

