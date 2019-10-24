<template>
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
				<p>{{dataset.old_citation}}</p>
				<p>{{dataset.cite_title}} {{dataset.cite_authors}} {{dataset.cite_venue}} {{dataset.cite_year}}</p>
			</div>
		</div>
		<div v-if="isCurrentUserOwner || isAdmin" class="bottom">
			<router-link tag="a" :to="{path: '/datasets/' + dataset.id +'/edit'}">Edit Dataset Profile</router-link>
			<div class="edit-messages">
				<router-link tag="a" :to="{path: '/datasets/' + dataset.id +'/edit/requests'}">Open Edit Requests</router-link>
				<span>{{numberOpenEditRequests}}</span>
			</div>
		</div>
	</div>
</template>

<script>

export default {
	name: 'mainCard',
	props: {
		dataset: Object
	},

	computed: {
		isCurrentUserOwner () {
			return this.$store.state.userId == this.dataset.owner
		},

		isAdmin () {
			return this.$store.state.isAdmin
		},

		numberOpenEditRequests () {
			return this.dataset.edit_requests.filter((item) => { return !item.is_resolved }).length
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

</style>
