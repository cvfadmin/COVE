<template>
	<div class="dataset">
		<router-link :to="{path: '/datasets/' + dataset.dataset.id}" class="nav-link">
			<img v-if="dataset.dataset.thumbnail == null" src="https://picsum.photos/250/150/?random">
			<img v-else src={dataset.dataset.thumbnail}>
			<div class="info">
				<h4>{{dataset.dataset.name}}</h4>
				<p>{{dataset.dataset.description}}</p>
			</div>
		</router-link>
	</div>
</template>

<script>

export default {
	name: 'DatasetPreview',
	props: {
		dataset: Object,
	}
}

</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">

.dataset {
	width: 250px;
	height: 300px;
	display: flex;
	flex-direction: column;
	border: 1px solid #000;
	
	a {
		color: #000;
		text-decoration: none;
	}

	img {
		width: 250px;
		height: 150px;
		border-bottom: 1px solid #000;
	}

	.info {
		padding: 0 15px;

		h4 {
			text-transform: capitalize;
			font-weight: 700;
			margin: 10px 0 10px 0;
			border-bottom: 1px solid #000;
		}

		p {
			margin: 0;
			font-size: 12px;
		}
	}

}

</style>
