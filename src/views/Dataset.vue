<template>
	<div class="container">
		<PageHeader></PageHeader>
		<DatasetDecisionBar v-if="dataset.is_approved == false && isAdmin" :datasetId="dataset.id"></DatasetDecisionBar>		
		<div class="dataset">
			<div class="main card-wrapper">
				<div class="top">
					<div class="main-head">
						<div class="title">
							<h2>{{dataset.name}}</h2>
						</div>
						<div class="link">
							<a :href="dataset.url" target="_blank" rel="noopener noreferrer">Link to Dataset</a>
						</div>
					</div>
					<p class="description">{{dataset.description}}</p>
					<div class="citation">
						<strong>Citation:</strong>
						<p>{{dataset.citation}}</p>
					</div>
				</div>
				<div v-if="isCurrentUserOwner" class="bottom">
					<router-link tag="a" :to="{path: '/datasets/' + dataset.id +'/edit'}">Edit as Owner</router-link>
					<div class="edit-messages">
						<router-link tag="a" :to="{path: '/datasets/' + dataset.id +'/edit/requests'}">Open Edit Requests</router-link>
						<span>{{numberOpenEditRequests}}</span>
					</div>
				</div>

			</div>
			<div class="details">
				<div class="card-wrapper">
					<div class="photo">
						<img v-if="dataset.thumbnail == null" src="https://picsum.photos/300/200/?random">
						<img v-else :src="dataset.thumbnail">
					</div>
					<h4>Details:</h4>
					<p><strong>Year Created:</strong> {{dataset.year_created}}</p>
					<p><strong>Size:</strong> {{dataset.size}}</p>
					<p><strong>Number of Categories:</strong> {{dataset.num_cat}}</p>
					<p><strong>COVE Profile Last Updated:</strong> {{dataset.date_created | moment}}</p>
					
					<div class="tag-list">
						<p><strong>Tasks:</strong></p>
						<div v-for="tag in tasks">
							<router-link tag="a" :to="{name: 'home', query: {tasks: tag.name}}">{{tag.name}}</router-link>
						</div>
					</div>

					<div class="tag-list">
						<p><strong>Topics:</strong></p>
						<div v-for="tag in topics">
							<router-link tag="a" :to="{name: 'home', query: {topics: tag.name}}">{{tag.name}}</router-link>
						</div>
					</div>

					<div class="tag-list">
						<p><strong>Data Types:</strong></p>
						<div v-for="tag in dataTypes">
							<router-link tag="a" :to="{name: 'home', query: {data_types: tag.name}}">{{tag.name}}</router-link>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import PageHeader from '@/components/PageHeader.vue'
import DatasetService from '@/services/DatasetService'
import DatasetDecisionBar from '@/components/admin/DatasetDecisionBar.vue'
import moment from 'moment'

export default {
	name: 'dataset',
	components: {
		PageHeader,
		DatasetDecisionBar,
	},

	data () {
		return {
			dataset: {},
		}
	},

	computed: {
		tags () {
			let tags = []
			try {
				for (let i = 0; i < this.$store.state.tags.length; i++) {
					if (this.dataset.tags.includes(this.$store.state.tags[i].id)) {
						tags.push(this.$store.state.tags[i])
					}
				}
			} catch(err) {
				return []
			}
			return tags
		},

		tasks () {
			return this.tags.filter((item) => {
				return item.category == 'tasks'
			})
		},

		topics () {
			return this.tags.filter((item) => {
				return item.category == 'topics'
			})
		},

		dataTypes () {
			return this.tags.filter((item) => {
				return item.category == 'data_types'
			})
		},

		isCurrentUserOwner () {
			return this.$store.state.userId == this.dataset.owner
		},

		isAdmin () {
			return this.$store.state.isAdmin
		},

		numberOpenEditRequests () {
			return this.dataset.edit_requests.filter((item) => { return !item.is_resolved }).length
		}
	},

	methods: {
		// TODO: Check for dataset in store before sending another request
		async getDataset () {
			return await DatasetService.getDatasetById(this.$route.params.id)
		},

		moment: function () {
			return moment();
		},
	},

	beforeMount(){
		this.getDataset().then((response) => {
			this.dataset = response.data.result

			// TODO: better way to handle these permissions?
			if (!this.dataset.is_approved) {
				if (!this.$store.state.isAdmin) {
					if (this.$store.state.userId != this.dataset.owner) {
						this.$router.push('/')
					}
				}
			}
		})
		
		this.$store.commit('loadTags')
	},

	filters: {
		moment: function (date) {
			return moment(date).format('MMM. Do, YYYY');
		}
	}
}
</script>


<style scoped lang="scss">

a {
	color: #444;
	font-size: 14px;
}

strong {
	font-family: 'Open Sans', sans-serif;
	font-weight: 700;
	font-size: 14px;
	color: #656565;
}

.dataset {
	display: flex;
	justify-content: space-between;
	align-items: self-end;
	color: #888888;

	.main {
		flex: 1;
		margin-right: 20px;
		padding: 20px 30px;
		display: flex;
		flex-direction: column;
		justify-content: space-between;

		.description {
			font-size: 14px;
			color: #444;
			line-height: 25px;
		}

		.main-head {
			display: flex;
			justify-content: space-between;

			.title {
				flex: 1;
			}

			.dates p {
				margin: 0;
			}

			.dates strong {
				font-size: 12px;
			}
		}

		.citation strong {
			font-family: 'Open Sans', sans-serif;
			font-weight: 700;
			font-size: 14px;
			color: #656565;
		}

		.bottom {
			display: flex;
			justify-content: space-between;

			span {
				font-family: 'Open Sans', sans-serif;
				padding: 1px 5px;
				border-radius: 3px;
				background: #eee;
				font-size: 12px;
				margin-left: 10px;
			}
		}

		h2 {
			font-family: 'Vollkorn', serif;
			text-transform: capitalize;
			font-weight: 500;
			color: #525252;
			margin: 0;
			font-size: 28px;
		}

		p {
			font-size: 12px;
		}
	}

	.details {
		
		.tag-list {
			display: flex;
			flex-wrap: wrap;
			align-items: center;

			div a {
				text-decoration: none;
				font-family: 'Open Sans', sans-serif;
				font-size: 12px;
		    font-weight: 700;
		    color: #ccc;
		    text-transform: lowercase;
		    margin-left: 5px;
			}

			div:first-child {
				margin-left: 0;
			}
		}

		strong {
			font-size: 12px;
		}

		p {
			margin: 0;
			font-size: 12px;
			margin: 3px 0;
		}

		h4 {
			font-family: 'Vollkorn', serif;
			font-weight: 500;
			color: #525252;
			margin: 10px 0;
			font-size: 18px
		}

		img {
			width: 300px;
		}
	}
}

.card-wrapper {
	padding-top: 20px;
	box-shadow: 0 1px 2px 0 rgba(0,0,0,0.1);
}

</style>
