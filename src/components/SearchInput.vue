<template>
	<div class="input-group">
		<p>Search Terms:</p>
		<input type="search" placeholder="ex. trees, cars, birds">
	</div>
</template>


<script>

export default {
	name: 'SearchInput',
}

</script>


<style scoped lang="scss">

.input-group {
	input[type="search"] {
		border: 1px #000 solid;
		color: #000;
		font-family: 'Open Sans', sans-serif;
		margin: 10px 0;
		padding: 5px 10px;
	}

	p  {
		font-size: 14px;
		font-weight: 800;
		margin: 0;
	}
}
	
</style>