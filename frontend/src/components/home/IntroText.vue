<template>
	<section id="introduction">
    <p><strong>COVE</strong> is an online repository for computer vision datasets sponsored by the Computer Vision Foundation. It is intended to aid the computer vision research community and serve as a centralized reference for all datasets in the field. If you are a researcher with a dataset not currently in COVE, please help make this site as comprehensive a resource as possible for the community and add it to the database!</p>
  </section>
</template>

<script>
export default {
	name: 'IntroText',
}
</script>

<!-- Add "scoped" attribute to limit SCSS to this component only -->
<style scoped lang="scss">

section {
	max-width: 1040px;
	margin: 0 auto;
}

p {
	line-height: 30px;
  font-size: 15px;
  margin: 20px 0;
}

</style>
