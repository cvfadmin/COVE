<template>
	<div class="users-page container">
		<PageHeader></PageHeader>
		<section>
			<h2 v-if="usersDatasets.length != 0">Your Datasets:</h2>
			<p class="null-message" v-if="usersDatasets.length == 0">You currently own no datasets.</p>
			<ul class="dataset-list">
				<li v-for="dataset in usersDatasets" :key="dataset.id">
					<DatasetPreview :dataset="dataset"></DatasetPreview>
				</li>
			</ul>
		</section>
	</div>
</template>

<script>
import PageHeader from '@/components/PageHeader.vue'
import DatasetService from '@/services/DatasetService'
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
			await DatasetService.getCurrentUserInfo().then((response) => {
				let userInfo = response.data.result
				this.usersDatasets = userInfo.datasets
			})
		},
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
}

</style>
