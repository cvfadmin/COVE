<template>
	<div id="app">
		<router-view/>
		<Footer></Footer>
	</div>
</template>

<script>
import Footer from '@/components/Footer.vue'

export default {
	components: {
		Footer,
	}
}

</script>

<!-- Global App Styles -->
<style lang="scss">

#app {
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	min-height: 100vh;
}

body {
	padding: 0;
	margin: 0;
	background: #fbfbfb;
	-webkit-font-smoothing:antialiased;
}

h1 {
	font-family: 'Vollkorn', serif;
  font-weight: 500;
  font-size: 48px;
}

h2, h4, p, a, input, button {
	font-family: 'Open Sans', sans-serif;
}

.container {
	width: 1040px;
	margin: 0 auto;
}

.card-wrapper {
	background: #fff;
	border-radius: 3px;
	padding: 20px;
	padding-top: 0;
	margin-top: 20px;
	box-shadow: 0 1px 2px 0 rgba(0,0,0,0.1);
}

textarea {
	min-height: 75px;
}

form {
		
		button {
			background: none;
			border: 1px #525252 solid;
			padding: 10px 0;
			margin: 20px 0 50px 0;
		}

		button:hover {
			background: #525252;
			color: #fff;
		}
}

ul {
	list-style: none;
	margin: 0;
	padding: 0;
}

/* Inputs */

.input-group {
	/* Assumes a p elem and an input elem */
	display: flex;
	flex-direction: column;

	p  {
		font-size: 14px;
		font-weight: 800;
		margin: 0;
	}

	input, textarea {
		border: none;
		box-shadow: 0 1px 2px 0 rgba(0,0,0,0.1);
		border-radius: 3px;
		color: #000;
		margin: 10px 0;
		padding: 5px 10px;
	}

	.input-head {
		display: flex;
		align-items: center;

		.error {
			margin-left: 12px;
			font-style: italic;
			font-weight: 300;
			color: #de6868;
			font-size: 10px;
		}
	}
}


</style>
