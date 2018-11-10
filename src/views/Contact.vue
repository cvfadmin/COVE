<template>
  <div class="contact container">
		<PageHeader></PageHeader>
    <h1>This is a contact page</h1>
  </div>
</template>

<script>
// @ is an alias to /src
import PageHeader from '@/components/PageHeader.vue'

export default {
	name: 'contact',
	components: {
		PageHeader,
	}
}
</script>

<!-- Add "scoped" attribute to limit SCSS to this component only -->
<style scoped lang="scss">
</style>
