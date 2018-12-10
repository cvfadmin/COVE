<template>
	<div class="footer">
		<div class="cvf-logo">
			<img src="@/assets/cvf-logo.png" alt="CVF Logo">
		</div>
		<div class="content">
			<p>For feedback and inquiries, please contact us at <a href="mailto:cove@thecvf.com">cove@thecvf.com</a>.</p>
			<p>This effort is sponsored by an <a href="https://nsf.gov/awardsearch/showAward?AWD_ID=1463102" target="_blank" rel="noopener noreferrer">award</a> from the National Science Foundation (NSF).</p>
			<p>Site maintained by Boston University, University of Michigan and Notre Dame. Updated 2018.</p>
		</div>
		<div class="nsf-logo">
			<img src="@/assets/nsf-logo.png" alt="NSF Logo">
		</div>
	</div>
</template>

<script>

export default {
	name: 'Footer',
}

</script>

<style scoped lang="scss">

	.footer {
		margin: 20px 0 0 0;
		padding: 20px 0;
		background: #eee;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #525252;
		font-size: 11px;

		.content {
			margin: 0 20px;

			p {
				text-align: center;
				margin: 2px 0;

				a {
					color: #000;
					text-decoration: none;
				}
			}

		}

		.cvf-logo, .nsf-logo {
			img {
				width: 40px;
			}
		}

	}
</style>
