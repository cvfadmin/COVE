<template>
	<div class="users-page container">
		<PageHeader></PageHeader>
		<section>
			<h2 v-if="usersDatasets.length != 0">Your Datasets:</h2>
			<p class="null-message" v-if="usersDatasets.length == 0">You currently own no datasets.</p>
			<ul class="dataset-list">
				<li v-for="dataset in usersDatasets" :key="dataset.id">
					<DatasetPreview :dataset="dataset" :notification="getNotificationObject(dataset)"></DatasetPreview>
				</li>
			</ul>
		</section>
	</div>
</template>

<script>
import PageHeader from '@/components/PageHeader.vue'
import UserService from '@/services/UserService'
import DatasetPreview from '@/components/datasets/DatasetPreview.vue'

export default {
	name: 'usersPage',
	components: {
		PageHeader,
		DatasetPreview
	},

	data () {
		return {
			usersDatasets: []
		}
	},

	methods: {
		async getUserInfo () {
			await UserService.getCurrentUserInfo().then((response) => {
				let userInfo = response.data.result
				this.usersDatasets = userInfo.datasets
			})
		},

		countUnreadMessages(message_list) {
			let unresolved = message_list.filter((item) => { return !item.is_resolved })
			return unresolved.length
		},

		getNotificationObject (dataset) {
			let numUnread = this.countUnreadMessages(dataset.edit_requests)
			if (numUnread > 0) {
				return {
					'message': 'You have ' + numUnread + ' open edit requests for this dataset',
					'link': {'path': '/datasets/' + dataset.id +'/edit/requests'},
				}
			} else {
				return undefined
			}
		}
	},

	beforeMount() {
		this.getUserInfo()
	}
}
</script>

<style scoped lang="scss">

section {
	
	h2 {
		font-family: 'Vollkorn', serif;
    text-transform: capitalize;
    font-weight: 500;
    color: #333333;
    font-size: 28px;
	}

	.null-message {
		text-align: center;
	}

	ul {
		display: flex;
  	flex-flow: row wrap;
		justify-content: space-between;
		list-style: none;
		padding: 0;
		margin: 20px 0 0 0;

		&::after {
		  content: "";
			width: calc(33% - 20px);
		}

		li {
			margin: 0 0 20px 0;
			align-items: flex-start;
			width: calc(33% - 20px);
    	box-sizing: border-box;
		}
	}

	a.edit-messages {
		margin: 0 0 10px 0;
		padding: 5px 8px;
		font-family: 'Open Sans', san-serif;
		font-size: 11px;
		font-weight: 600;
		color: #000;
		display: block;
	}

	a.edit-messages:hover {
		color: #444;
	}
}

</style>
