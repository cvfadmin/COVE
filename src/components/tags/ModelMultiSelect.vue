<template>
	<div class="model-multi-select">
		
		<input type="text" 
			v-model="cleanedQuery"
			v-on:keydown.enter.prevent="selectTagOrNew()"
			v-on:focus="showDropdown()"
			v-on-clickaway="hideDropdown"
		>
		
		<ul id="filtered-list" v-bind:class="{ hidden: isHidden }">
			<li v-for="(model, index) in filteredTags" :class="{ 'active': index == 0 }">
				<div v-on:click.self="selectModel(model, $event)">{{model.name}}</div>
			</li>
		</ul>

		<ul id="selected-list">
			<li v-for="model in selectedTags">
				<div class="selected" v-on:click.self="unselectModel(model, $event)">{{model.name}}</div>
			</li>
		</ul>
	</div>
</template>

<script>
import { mixin as clickaway } from 'vue-clickaway';

export default {
	name: 'ModelMultiSelect',
	props: {
		models: Array,
		currentTags: {
      type: Array,
      default: () => {return []}
    },
		createNew: Boolean,
		category: String,
	},
	mixins: [ clickaway ],

	data () {
		return {
			query: '',
			removedTags: [],
			newlySelectedTags: [],
			isHidden: true,
		}
	},

	computed: {

		cleanedQuery: {
			get: function () { return this.query },
			set: function (newQuery) { this.query = newQuery.toLowerCase().replace(/[^a-z\s]/g,'') }
		},

		selectedTags () {
			// current tags plus any new tags minus removed tags
			return this.currentTags.concat(this.newlySelectedTags).filter((item) => !this.removedTags.includes(item))
		},

		notSelectedTags () {
			return this.models.filter((item) => !this.selectedTags.includes(item))
		},

		filteredTags () {
			if (this.query == '') { return this.notSelectedTags }
			return this.notSelectedTags.filter((item) => item.name.includes(this.query))
		}
	},

	methods: {

		resetComponent () {
			this.query = ''
			this.isHidden = true
		},
		
		// All changes are routed through selectModel and unselectModel
		selectModel(model) {
			this.newlySelectedTags.push(model)
			this.$emit('changedTags', this.selectedTags, this.category)
		},

		unselectModel(model) {
			this.removedTags.push(model)
			this.$emit('changedTags', this.selectedTags, this.category)
		},

		selectTagOrNew () {
			if (this.filteredTags.length == 0 && this.createNew) {
				// Create new
				this.selectModel({
					"name": this.query,
					"category": this.category,
					"new":true
				})
			} else if (this.filteredTags[0] != undefined) {
				// Select First value in unselected list
				this.selectModel(this.filteredTags[0])
			}

			this.resetComponent()
		},
		
		showDropdown () { this.isHidden = false },
		hideDropdown: function () { this.isHidden = true } // Must use 'function' for click-away mixin	
	},
}

</script>

<style scoped lang="scss">

$primary-width: 200px;

.hidden {
	display: none;
}

input {
	width: $primary-width;
	margin-bottom: 0;
}

ul {
	padding: 0;
	margin: 0;
	list-style: none;

	li {
		font-family: 'Open Sans', san-serif;
		font-size: 12px;
	}
}

.model-multi-select {

	#selected-list {
		display: flex;
		flex-wrap: wrap;

		.selected {
			display: inline-block;
			border: 1px solid #000;
			padding: 5px 10px;
			margin: 10px 10px 0 0;
		}
	}

	.selected:hover {
		background: #de6868;
	}

	#filtered-list {
		position: absolute;
		z-index: 100;
		background: #fff;

		li {
			border: 1px solid #000;
			border-bottom: none;
			width: $primary-width;
			padding: 5px 10px;
			cursor: pointer;
		}

		li:hover, .active {
			background: #eee;
		}

		li:first-child {
			border-top: none;
		}

		li:last-child {
			border-bottom: 1px solid #000;
		}
	}

	#filtered-list:hover {
		.active {
			background: auto;
		}
	}
}
	
</style>