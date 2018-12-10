<template>
	<div class="model-multi-select">
		
		<input type="text" 
			v-model="modelSearchString" 
			v-on:input="searchModelsList()"
			v-on:keydown.enter.prevent="selectModelOrNew()"
			v-on:focus="makeVisible()"
			v-on-clickaway="makeHidden"
		>
		
		<ul id="not-selected-list" v-bind:class="{ hidden: isHidden }">
			<li v-for="(model, index) in notSelectedModels" :class="{ 'active': index == 0 }">
				<div v-on:click.self="selectModel(model, $event)">{{model.name}}</div>
			</li>
		</ul>

		<ul id="selected-list">
			<li v-for="model in selectedModels">
				<div class="selected" v-on:click.self="unSelectModel(model, $event)">{{model.name}}</div>
			</li>
		</ul>
	</div>
</template>

<script>
import removeFromList from "@/components/utils.js"
import { mixin as clickaway } from 'vue-clickaway';

export default {
	name: 'ModelMultiSelect',
	props: {
		models: Array,
		createNew: Boolean,
		category: String
	},
  mixins: [ clickaway ],

	data () {
		return {
			selectedModels: [],
			filteredModels: [],
			modelSearchString: '',
			newModels: [], // Expects list of objs with name property
			isHidden: true,
		}
	},

	computed: {
		notSelectedModels () {
			// Everything that is not selected or filtered out by the search
			let notSelected = this.models.filter((item) => !this.selectedModels.includes(item))
			return notSelected.filter((item) => !this.filteredModels.includes(item))
		},

		toFilterModels () {
			return this.models.filter((item) => !this.selectedModels.includes(item))
		}
	},

	methods: {

		selectModel(model) {
			// notSelectedModels is computed - will adjust
			this.selectedModels.push(model)
			this.$store.commit('addSelectedTag', model)
		},

		unSelectModel(model) {
			// notSelectedModels is computed - will adjust
			this.selectedModels = removeFromList(model, this.selectedModels)
			this.$store.commit('removeSelectedTag', model)
		},
		
		searchModelsList() {
			this.modelSearchString = this.modelSearchString.toLowerCase()

			if (this.modelSearchString == '') { 
				this.filteredModels = []
			} else {
				this.filteredModels = this.toFilterModels.filter((item) => !item.name.includes(this.modelSearchString))
			}
		},

		selectModelOrNew () {
			this.modelSearchString = this.modelSearchString.toLowerCase()

			if (this.notSelectedModels.length == 0 && this.createNew) {
				// Create new
				this.selectModel({
					"name": this.modelSearchString,
					"category": this.category,
					"new":true
				})
				// Reset
				this.modelSearchString = ''
				this.filteredModels = []
			} else {
				// Select First value in unselected list
				if (this.notSelectedModels[0] != undefined) {
					this.selectModel(this.notSelectedModels[0])
					// Clear text
					this.modelSearchString = ''
				}
			}
		},
		
		makeVisible () {
			this.isHidden = false
		},

		makeHidden: function () {
			this.isHidden = true
		}		

	},

	beforeMount () {
		this.selectedModels = this.$store.state.selectedTags.filter((item) => {return item.category == this.category})
	}
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

	#not-selected-list {
    position: absolute;
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

	#not-selected-list:hover {
		.active {
			background: auto;
		}
	}
}
	
</style>