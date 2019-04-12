<template>
	<div class="edit-request card-wrapper" :id="request.id">
		<div class="top">
			<p>Edit request #{{request.id}} on dataset: <router-link tag="a" :to="{path: '/datasets/' + request.dataset}">{{request.dataset_name}}</router-link></p>
			<button v-if="isAdmin" v-on:click="resolveRequest(true)">Mark as Resolved</button>
		</div>

		<p>{{request.content}}</p>

		<div class="bottom">
			<div v-if="!displayMessages" v-on:click="displayMessages = true" :class="repliesButton">
				<p>view {{request.messages.length}} {{replyOrReplies}}</p>
			</div>

			<div v-if="displayMessages" v-on:click="displayMessages = false" :class="repliesButton">
				<p>hide {{request.messages.length}} {{replyOrReplies}}</p>
			</div>

			<div v-if="!displayReplyForm" v-on:click="displayReplyForm = true" class="reply-form-button">
				<p>Send another message</p>
			</div>

			<div v-if="displayReplyForm" v-on:click="displayReplyForm = false" class="reply-form-button">
				<p>hide reply form</p>
			</div>

			<p>created {{request.date_created | moment}}</p>
		</div>

		<div v-if="displayMessages" v-for="message in request.messages" :key="message.id">
			<EditRequestMessage :message="message" v-on:markedAsRead="messageMarkedAsRead"></EditRequestMessage>
		</div>

		<form v-if="displayReplyForm" v-on:submit.prevent="handleSubmit()">
			<span>{{errors}}</span>
			<textarea v-model="newMessageContent"></textarea>
			<button type="submit">Submit Reply</button>
		</form>
	</div>
</template>

<script>
import moment from 'moment'
import EditRequestMessage from '@/components/admin/EditRequestMessage.vue'
import AdminService from '@/services/AdminService'

export default {
	name: 'editRequest',

	components: {
		EditRequestMessage,
	},

	props: {
		request: Object,
	},

	data () {
		return {
			displayMessages: false,
			displayReplyForm: false,
			newMessageContent: '',
			errors: '',
		}
	},

	computed: {
		replyOrReplies() {
			if (this.request.messages.length == 1) {
				return 'reply'
			} else {
				return 'replies'
			}
		},

		isAdmin() {
			return this.$store.state.isAdmin
		},

		repliesButton() {
			let unreadMessages = []

			if (this.isAdmin) {
				unreadMessages = this.request.messages.filter((item) => {return !item.has_admin_read})
			} else {
				unreadMessages = this.request.messages.filter((item) => {return !item.has_owner_read})
			}

			if (unreadMessages.length != 0) {
				return "replies-button-unread"
			} else {
				return "replies-button"
			}
		}
	},

	methods: {

		handleSubmit () {
			let messageData = {
				"content": this.newMessageContent,
				"author": this.$store.state.userId
			}

			this.createMessage(this.request.id, messageData).then((response) => {
				if (response.data.errors != undefined && response.status == 200) {
					// Show validation errors
					this.errors = response.data.errors
				} else if (response.status == 200) {
					// Created successfully
					this.newMessageContent = ''
						
					alert("Your message has been sent.")
					this.$router.go()
					
				} else {
					// Some weird error
					alert("Oops something went wrong :/ - Please email cove@thecvf.com if error persists.")
					console.log(response)
				}
			})
		},

		async createMessage (request_id, data) {
			return await AdminService.createEditRequestMessage(request_id, data)
		},


		async resolveRequest () {
			await AdminService.updateEditRequest(this.request.id, {"is_resolved": true}).then((response) => {
				if (response.status == 200 && response.data.error == undefined) {
					alert("Request #" + this.request.id + ' has been marked as resolved.')
					this.$router.go()
				} else {
					// Some weird error
					alert("Oops something went wrong :/ - Please email cove@thecvf.com if error persists.")
					console.log(response)
				}
			})
		},

		messageMarkedAsRead(message_id) {
			let message = this.request.messages.find((item) => {return item.id == message_id})
			if (this.isAdmin) {
				message.has_admin_read = true
			} else {
				message.has_owner_read = false
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
}
</script>

<style scoped lang="scss">

.edit-request, {
	padding: 10px;
	
	p {
		margin: 0;
		font-size: 12px;
	}

	.bottom {
		display: flex;
		align-items: baseline;
		margin-top: 5px;

		p, .reply-form-button {
			margin-left: 5px;
			font-size: 11px;
			font-weight: 600;
		}
	}

	.top {
		display: flex;
		align-items: baseline;
		justify-content: space-between;
		margin-bottom: 5px;

		p {
			font-size: 11px;
			font-weight: 700;
		}

		a {
			color: #363636;
		}

		button {
			margin-left: 10px;
			background: #fff;
		}
	}
}

.replies-button, .reply-form-button, .replies-button-unread {
	cursor: pointer;
	background: #eee;
	padding: 2px 4px;
	border-radius: 2px;
}

.replies-button-unread {
	background: #f8d7da;
}



form {
	display: flex;
	flex-direction: column;
	margin-top: 25px;

	button {
		margin-bottom: 0;
	}
}

</style>