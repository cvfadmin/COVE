<template>
	<div class="edit-request-message card-wrapper">
		<div class="top">
			<p>From {{message.author_name}} {{message.date_created | moment}}</p>
		</div>
		<p>{{message.content}}</p>
		<div class="bottom">
			<p v-if="!hasBeenRead" v-on:click="markAsRead()" class="mark-as-read">mark as read</p>
		</div>
	</div>
</template>

<script>
import moment from 'moment'
import AdminService from '@/services/AdminService'

export default {
	name: 'EditRequestMessage',
	props: {
		message: Object,
	},

	data (){
		return {
			hasBeenRead: undefined,
		}
	},

	methods: {

		async markAsRead () {
			let updatedMessage = {}

			if (this.$store.state.isAdmin) {
				updatedMessage.has_admin_read = true
			} else {
				updatedMessage.has_owner_read = true
			}

			await AdminService.updateEditRequestMessage(this.message.id, updatedMessage).then((response) => {
				if (response.status == 200) {
					this.hasBeenRead = true
				} else {
					// Some weird error
					alert("Oops something went wrong :/ - Please email cove@thecvf.com if error persists.")
					console.log(response)
				}
			})
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
		if (this.$store.state.isAdmin) {
			this.hasBeenRead = this.message.has_admin_read
		} else {
			this.hasBeenRead = this.message.has_owner_read
		}
	}
}
</script>

<style scoped lang="scss">
.edit-request-message, {
	padding: 10px;
	
	p {
		margin: 0;
		font-size: 12px;
	}

	.bottom {
		margin-top: 5px;
		display: flex;

		p {
			font-size: 11px;
			font-weight: 600;
			margin-left: 5px;
		}

		p:first-child {
			margin-left: 0;
		}

		.mark-as-read {
			cursor: pointer;
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
</style>