<template>
	<div class="dataset">
		<router-link :to="{path: '/datasets/' + dataset.id}" class="nav-link">
			<div class="photo">
				<img v-if="dataset.thumbnail == null" src="https://picsum.photos/300/200/?random">
				<img v-else :src="dataset.thumbnail">
			</div>
			<div class="info">
				<h4>{{dataset.name}}</h4>
				<p>{{dataset.description | truncate(125)}}</p>
			</div>
			<div class="tags">
				<div class="tag" v-for="tag in tags" :key="tag.id">
					{{tag.name}}
				</div>
			</div>
		</router-link>
	</div>
</template>

<script>

export default {
	name: 'DatasetPreview',
	props: {
		dataset: Object,
	},

	computed: {
		tags () {
			let tags = []
			for (let i = 0; i < this.$store.state.tags.length; i++) {
				if (this.dataset.tags.includes(this.$store.state.tags[i].id)) {
					tags.push(this.$store.state.tags[i])
				}
			}
			return tags
		}
	},

	filters: {
		truncate: function (text, stop, clamp) {
			if (!text) return ''
			return text.slice(0, stop) + (stop < text.length ? clamp || '...' : '')
		}
	}
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

$card-radius: 3px;

.dataset {
	display: flex;
	flex-direction: column;
	background: #fff;
	border-radius: $card-radius;
	box-shadow: 0 1px 2px 0 rgba(0,0,0,0.1);
	color: #888888;
	
	a {
		color: #888888;
		text-decoration: none;
	}
	
	.photo {

		img {
			width: 100%;
			height: 200px;
			border-top-left-radius: $card-radius;
			border-top-right-radius: $card-radius;
		}
	}
	

	.info {
		padding: 0 20px 0 20px;

		h4 {
			margin: 15px 0 5px 0;
			font-size: 16px;
			text-transform: capitalize;
			font-weight: 600;
			color: #525252;
    	font-family: 'Vollkorn', serif;
		}

		p {
			margin: 0;
			font-size: 12px;
		}
	}

	.tags {
		margin: 10px 20px;
		display: flex;

		.tag {
			font-size: 11px;
			font-weight: 700;
			color: #ccc;
			text-transform: lowercase;
			margin-left: 5px;
		}

		.tag:first-child {
			margin-left: 0;
		}
	}

}

</style>
