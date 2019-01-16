export default {
	buildUrl (route, params) {
		let url = route
		let isFirst = true

		for (const key of Object.keys(params)) {
			// Skip if value is no value to add
	    if (params[key] == undefined || params[key].length == 0) {
	    	continue
	    }

	    if (isFirst) {
	    	url += '?' + key + '=' + params[key]
	    	isFirst = false
	    } else {
				url += '&' + key + '=' + params[key]
	    }
		}

		return url
	}
}