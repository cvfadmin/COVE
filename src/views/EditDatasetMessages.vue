<template>
	<div class="edit-dataset-messages container">
		<PageHeader></PageHeader>
		<section>
			<div v-for="request in requests" :key="request.id" class="request card-wrapper">
				<div class="top">
					<p>New Admin Request</p>
				</div>
				<p>{{request.content}}</p>
				<div class="bottom">
					<p class="date-sent">{{request.date_created | moment}}</p>
				</div>
			
				<div v-for="message in request.messages" :key="message.id" class="message card-wrapper">
					<p>{{message.content}}</p>
					<div class="bottom">
						<p class="date-sent">{{message.date_created | moment}}</p>
					</div>
				</div>

				<form v-on:submit.prevent="handleSubmit(request.id)">
					<span>{{errors[request.id]}}</span>
					<textarea v-model="newMessageContent[request.id]"></textarea>
					<button type="submit">Submit Reply</button>
				</form>

			</div>
		</section>
	</div>
</template>

<script>
import PageHeader from '@/components/PageHeader'
import DatasetService from '@/services/DatasetService'
import moment from 'moment'

export default {
	name: 'editDatasetMessages',
	components: {
		PageHeader,
	},

	data () {
		return {
			dataset: {},
			requests: [],
			newMessageContent: {},
			errors: {}
		}
	},

	methods: {

		async handleSubmit (request_id) {
			let messageData = {
				"content": this.newMessageContent[request_id],
				"author": this.$store.state.userId
			}

			this.createMessage(request_id, messageData).then((response) => {
				if (response.data.errors != undefined && response.status == 200) {
					// Show validation errors
					this.errors[request_id] = response.data.errors
				} else if (response.status == 200) {
					// Created successfully
					this.newMessageContent[request_id] = ''
						
					alert("Your message has been sent.")
					this.$router.go()
					
				} else {
					// Some weird error
					alert("Oops something went wrong :/ - Please email cove@thecvf.com if error persists.")
					console.log(response)
				}
			})
		},

		async getRequests () {
			const response = await DatasetService.getEditRequests(this.$route.params.id)
			this.requests = response.data.results
		},

		async createMessage (request_id, data) {
			return await DatasetService.createEditRequestMessage(request_id, data)
		},
		
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

		moment: function () {
			return moment();
		},
	},

	filters: {
		moment: function (date) {
			return moment(date).fromNow();
		}
	},

	beforeMount () {
		this.getDataset()
		this.getRequests()

		// TODO: better way to handle these permissions?
		/*console.log(this.$store.state.userId != this.dataset.owner)
		if (!this.$store.state.isAdmin && this.$store.state.userId != this.dataset.owner) {
			this.$router.push({
				name: 'login',
				params: { error: 'You must be logged in as the owner to edit this dataset' },
			})
		}*/
	}

}
</script>


<style scoped lang="scss">

.request, .message {
	padding: 10px;
	
	p {
		margin: 0;
		font-size: 12px;
	}

	.bottom {
		margin-top: 5px;

		p {
			font-size: 11px;
			font-weight: 600;
		}
	}

	.top {
		margin-bottom: 5px;

		p {
			font-size: 11px;
			font-weight: 600;
		}
	}
}

form {
	display: flex;
	flex-direction: column;
	margin-top: 25px;
}

</style>

