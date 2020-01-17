<template>
	<section id="pagination">
		<button v-on:click="previous" v-bind:class="{ hidden: hidePrevious }">< Previous Page</button>
		<button v-on:click="next" v-bind:class="{ hidden: hideNext }">Next Page ></button>
  </section>
</template>

<script>
export default {
	name: 'Pagination',

	data () {
		return {
			hideNext: false,
			hidePrevious: false,
		}
	},

	methods: {

		next () {
			this.$emit('next')
		},

		previous () {
			this.$emit('previous')
		}
	}
}

</script>

<!-- Add "scoped" attribute to limit SCSS to this component only -->
<style scoped lang="scss">

#pagination {
	display: flex;
	justify-content: space-between;

	button {
		width: 150px;
		margin: 0;
    border: none;
    padding: 10px 15px;
    border-radius: 3px;
    background: #525252;
    color: #fff;
    font-weight: 600;
    cursor: pointer;
	}

	.hidden {
		visibility: hidden;
	}
}
	
</style>
