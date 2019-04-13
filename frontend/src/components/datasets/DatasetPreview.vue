<template>
	<div class="dataset">
		<router-link :to="{path: '/datasets/' + dataset.id}" class="nav-link">
			<div class="photo">
				<img v-if="dataset.thumbnail == null" src="https://picsum.photos/300/200/?random">
				<img v-else :src="dataset.thumbnail">
				<div v-if="notification" class="notification alert">
					<router-link :to="notification.link" class="alert"> {{notification.message}} </router-link>
				</div>
			</div>
			<div class="info">
				<h4>{{dataset.name}}</h4>
				<p>{{dataset.description | truncate(125)}}</p>
			</div>
		</router-link>
	</div>
</template>

<script>

export default {
	name: 'DatasetPreview',
	props: {
		dataset: Object,
		notification: Object
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
		position: relative;

		img {
			width: 100%;
			height: 200px;
			object-fit: cover;
			border-top-left-radius: $card-radius;
			border-top-right-radius: $card-radius;
		}

		.notification {
			position: absolute;
			top: 10px;
			left: 5px;
			margin-right: 5px;
			padding: 4px 5px;
			border-radius: 2px;
			display: flex;
			align-items: center;

			a {
				font-size: 11px;
				color: #721c24;
				text-decoration: underline;
			}
		}
	}
	

	.info {
		padding: 0 20px 20px 20px;

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

}

</style>
