<template>
	<div class="details">
		<div class="card-wrapper">
			<div class="photo">
				<img v-if="dataset.thumbnail == null" src="https://picsum.photos/300/200/?random">
				<img v-else :src="dataset.thumbnail">
			</div>
			<h4>Details:</h4>
			<p v-if="dataset.year_created != null"><strong>Year Created:</strong> {{dataset.year_created}}</p>
			<p v-if="dataset.size != null"><strong>Size:</strong> {{dataset.size}}</p>
			<p v-if="dataset.num_cat != null"><strong>Number of Categories:</strong> {{dataset.num_cat}}</p>
			<p><strong>COVE Profile Last Updated:</strong> {{dataset.last_updated | moment}}</p>
						
			<div class="tag-list" v-if="tasks.length > 0">
				<p><strong>Tasks:</strong></p>
				<div v-for="tag in tasks">
					<router-link tag="a" :to="{name: 'home', query: {tasks: tag.name}}">{{tag.name}}</router-link>
				</div>
			</div>

			<div class="tag-list"  v-if="topics.length > 0">
				<p><strong>Topics:</strong></p>
				<div v-for="tag in topics">
					<router-link tag="a" :to="{name: 'home', query: {topics: tag.name}}">{{tag.name}}</router-link>
				</div>
			</div>

			<div class="tag-list"  v-if="dataTypes.length > 0">
				<p><strong>Data Types:</strong></p>
				<div v-for="tag in dataTypes">
					<router-link tag="a" :to="{name: 'home', query: {data_types: tag.name}}">{{tag.name}}</router-link>
				</div>
			</div>

			<div id="ownership-request" v-if="dataset.is_owned_by_admin">
				<router-link tag="a" :to="{name: 'datasetOwnershipRequests', param: {id: dataset.id}}">Request Ownership</router-link>
			</div>

		</div>
	</div>
</template>

<script>
import moment from 'moment'

export default {
	name: 'SideCard',
	props: {
		dataset: Object
	},

	computed: {
		tasks () {
			if (!this.dataset) {return []}
			return this.dataset.tags.filter((item) => item.category == 'tasks')
		},

		topics () {
			if (!this.dataset) {return []}
			return this.dataset.tags.filter((item) => item.category == 'topics')
		},

		dataTypes () {
			if (!this.dataset) {return []}
			return this.dataset.tags.filter((item) => item.category == 'data_types')
		},
	},

	methods: {
		moment: function () {
			return moment();
		},
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

.card-wrapper {
	padding-top: 20px;
	box-shadow: 0 1px 2px 0 rgba(0,0,0,0.1);
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


	#ownership-request {
		margin-top: 10px;
		display: flex;
		justify-content: center;
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

</style>