<template>
	<div class="container">
		<PageHeader></PageHeader>
		<div v-if="dataset.is_approved == false" class="not-approved">
			<p>This dataset has not yet been approved.</p>
			<div class="decision">
				<button v-on:click="adminDecision(true)">Approve</button>
				<button v-on:click="adminDecision(false)">Deny</button>
			</div>
		</div>
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
				<div class="bottom">
					<router-link tag="a" :to="{path: '/datasets/' + dataset.id +'/edit-request'}">Edit Request</router-link>
					<router-link tag="a" :to="{path: '/datasets/' + dataset.id +'/delete-request'}">Delete Request</router-link>
				</div>

			</div>
			<div class="details">
				<div class="card-wrapper">
					<div class="photo">
						<img v-if="dataset.thumbnail == null" src="https://picsum.photos/300/200/?random">
						<img v-else :src="dataset.thumbnail">
					</div>
					<h4>Details:</h4>

					<p><strong>Created:</strong> {{dataset.date_created | moment}}</p>
					<p><strong>Last Updated:</strong> {{dataset.date_created | moment}}</p>

					<p><strong>Size:</strong> {{dataset.size}}</p>
					<p><strong>Number of Categories:</strong> {{dataset.num_cat}}</p>
					
					<div class="tag-list">
						<p><strong>Tasks:</strong></p>
						<div v-for="tag in tasks">
							{{tag.name}}
						</div>
					</div>

					<div class="tag-list">
						<p><strong>Topics:</strong></p>
						<div v-for="tag in topics">
							{{tag.name}}
						</div>
					</div>

					<div class="tag-list">
						<p><strong>Data Types:</strong></p>
						<div v-for="tag in dataTypes">
							{{tag.name}}
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
import moment from 'moment'

export default {
	name: 'dataset',
	components: {
		PageHeader,
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
		}
	},

	methods: {
		async getDataset () {
			// TODO: Check for dataset in store before sending another request
			const response = await DatasetService.getDatasetById(this.$route.params.id)
			this.dataset = response.data.result
		},

		async adminDecision (bool) {
			await DatasetService.adminDatasetResponse(this.dataset.id, {"is_approved": bool}).then((response) => {
				alert(response.data.message)
				console.log(response)
			})
		},

		moment: function () {
			return moment();
		},
	},

	beforeMount(){
		this.getDataset()
		this.$store.commit('loadTags')
	},

	filters: {
		moment: function (date) {
			return moment(date).format('MMM. Do, YYYY');
		}
	}
}
</script>

<!-- Add "scoped" attribute to limit SCSS to this component only -->
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

			div {
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

.not-approved {
	display: flex;
	justify-content: space-between;
	margin: 20px 0;
	background: #d27878;
	padding: 10px 20px;
	border-radius: 2px;
	
	p {
		color: #862828;
		margin: 0;
	}	

	.decision {
		button {

		}
	}
}

</style>
