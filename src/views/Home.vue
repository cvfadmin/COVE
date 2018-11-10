<template>
	<div class="home container">
		<PageHeader></PageHeader>
		<IntroText></IntroText>
		<section id="filters">
			<div class="filter-bars">
				<SearchInput></SearchInput>
			</div>
		</section>
		<section id="datasets">
			<DatasetList></DatasetList>
		</section>
	</div>
</template>

<script>
// @ is an alias to /src
import PageHeader from '@/components/PageHeader.vue'
import IntroText from '@/components/home/IntroText.vue'
import SearchInput from '@/components/SearchInput.vue'
import DatasetList from '@/components/datasets/DatasetList.vue'

export default {
	name: 'home',
	components: {
		PageHeader,
		IntroText, 
		SearchInput,
		DatasetList
	}
}
</script>

<!-- Add "scoped" attribute to limit SCSS to this component only -->
<style scoped lang="scss">

#filters {

	.filter-bars {
		display: flex;
		justify-content: space-between;

		.input-group:first-child {
			flex: 1;
		}

		.input-group { 
			/* Assumes a p elem and an input elem */
			display: flex;
			flex-direction: column;
		}

	}

}

</style>