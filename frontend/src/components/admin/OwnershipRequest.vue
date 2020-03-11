<template>
	<div class="ownership-request card-wrapper" :id="request.id">
		<div class="top">
            <p><strong>Ownership request {{request.id}} on dataset: <router-link tag="a" :to="{path: '/datasets/' + request.dataset}">{{request.dataset_name}}</router-link></strong></p>
            <div>
                <button v-on:click="resolveRequest(true)">Transfer Ownership</button>
                <button v-on:click="resolveRequest(false)">Deny</button>
            </div>
		</div>
		<p class="content">{{request.content}}</p>
        <p><strong>Requested by:</strong> {{request.author_name}}</p>
        <p><strong>Response Email:</strong> {{request.author_email}}</p>
	</div>
</template>

<script>
import moment from 'moment'
import AdminService from '@/services/AdminService'

export default {
	name: 'ownershipRequest',

	props: {
		request: Object,
	},

	data () {
		return {
			errors: '',
		}
	},

	methods: {

		async resolveRequest (isApproved) {
            // Get confirmation of action
            if (isApproved) {
                var isConfirmed = confirm('Are you sure you want to approve the ownership transfer in request ' + this.request.id +'?')
            } else {
                var isConfirmed = confirm('Are you sure you want to deny and delete the ownership transfer in request ' + this.request.id +'?')
            }
            // Do nothing - was not confirmed
            if (!isConfirmed) { return }

			await AdminService.updateOwnershipRequest(this.request.id, {"is_approved": isApproved}).then((response) => {
				if (response.status == 200 && response.data.error == undefined) {
					alert("Request " + this.request.id + ' has been marked as resolved.')
					this.$router.go()
				} else {
					alert("Oops something went wrong :/ - Please email cove@thecvf.com if error persists.")
					console.log(response)
				}
			}).catch(() => {
                alert("Oops something went wrong :/ - Please email cove@thecvf.com if error persists.")
				console.log(response)
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
}
</script>

<style scoped lang="scss">

.ownership-request, {
	padding: 10px;

    .content {
        margin: 10px 0;
    }
	
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

</style>