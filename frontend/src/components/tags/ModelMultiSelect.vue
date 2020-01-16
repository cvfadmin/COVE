<template>
	<div class="model-multi-select">
		
		<input type="text" 
			v-model="cleanedQuery"
			v-on:keydown.enter.prevent="selectTagOrNew()"
			v-on:keydown.tab="hideDropdown"
			v-on:focus="showDropdown()"
			v-on-clickaway="hideDropdown"
			v-test="{ id : 'text'}"
		>
		
		<ul id="filtered-list" v-bind:class="{ hidden: isHidden }" v-test="{ id: 'filtered-list'}">
			<li v-for="model in filteredTags" :key=model.id>
				<div v-on:click.self="selectModel(model, $event)">{{model.name}}</div>
			</li>
		</ul>

		<ul id="selected-list" v-test="{ id : 'selected-list'}">
			<li v-for="model in selectedTags" :key=model.id>
				<div class="selected" v-on:click.self="unselectModel(model, $event)">{{model.name}}</div>
			</li>
		</ul>
	</div>
</template>

<script>
import { mixin as clickaway } from 'vue-clickaway';
import Test from '@/directives/test.js'

export default {
	name: 'ModelMultiSelect',
	directives: { Test },
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

			// Is called whenever the user types in the "tags" box.
			set: function (newQuery) {
				this.query = newQuery.toLowerCase().replace(/[^a-z\s]/g,'')
				this.showDropdown() // Show dropdown menu whenever user types
			}
		},

		// Current tags plus newly added tags minus removed tags
		// Updated when newlySelectedTags is updated
		selectedTags () {
			return this.currentTags.concat(this.newlySelectedTags).filter((item) => !this.removedTags.includes(item))
		},

		// Current tags that have not been selected.
		// Updated when selectTags is updated.
		notSelectedTags () {
			return this.models.filter((item) => !this.selectedTags.includes(item))
		},

		// Array of tags that have the "query" in their name.
		// Updated when notSelectedTags is updated.
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

		// Removes a tag.
		// If the tag wasn't newly created one, add it to the removedTags list
		// If tag was a newly created one, simply remove it from the newlySelectedTags list
		unselectModel(model) {
			if (this.currentTags.includes(model)) {
				this.removedTags.push(model)
			} else {
				this.newlySelectedTags = this.newlySelectedTags.filter((item) => item != model) 
			}
			
			this.$emit('changedTags', this.selectedTags, this.category)
		},

		// Called when a user enters a word into the "tag" boxes
		// If none of the existing tags are equal to the word, create a new tag.
		// If there is a tag that is equal, select the first one returned.
		selectTagOrNew () {
			// Do nothing if no word is entered
			if (this.query == "") return
			
			// Only select a model if it is equal to a query - so new tags can be substrings of old tags
			if (this.createNew) {
				
				if (this.filteredTags[0].name == this.query) {
					// Select first value in unselected list
					this.selectModel(this.filteredTags[0])
				
				} else {
					// No tags match - create new
					this.selectModel({
						"name": this.query,
						"category": this.category,
					})
				}

			} else {
				// Select most similar
				this.selectModel(this.filteredTags[0])
			}

			this.resetComponent()
		},

		clearSelectedTags() {
			this.resetComponent()
			this.newlySelectedTags = []
			this.$emit('changedTags', this.selectedTags, this.category)
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
			cursor: pointer;

			div {
				padding: 5px 10px;
			}
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
		
		/* Adds Scrolling */
		max-height: 210px;
		overflow-y: auto;
	}
}
	
</style>