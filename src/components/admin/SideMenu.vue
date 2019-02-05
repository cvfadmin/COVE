<template>
	<div class="side-menu">
		<ul>
			<li><router-link tag="a" to="/admin/confirm-datasets">Confirm Datasets</router-link></li>
			<li><router-link tag="a" to="/admin/open-edit-requests">Open Edit Requests</router-link></li>
		</ul>
	</div>
</template>

<script>

export default {
	name: 'SideMenu',
}

</script>

<style scoped lang="scss">

.side-menu {
		
	ul {
		margin: 20px 0;

		li {
			margin: 10px 0;
			background: #fff;
			border-radius: 3px;
			box-shadow: 0 1px 2px 0 rgba(0,0,0,0.1);

			a {
				display: flex;
				justify-content: space-between;
				align-items: center;
				font-size: 13px;
				font-weight: 600;
				padding: 10px 10px;
				color: #525252;
				text-decoration: none;
				
				span {
					padding: 5px;
					border-radius: 3px;
					background: #eee;
					font-size: 12px;
					margin-left: 15px;
				}
			}
		}

		li:hover {
			background: #eee;
		}
	}
}

</style>