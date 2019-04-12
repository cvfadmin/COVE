function removeFromList (item, list) {
	let idx = list.indexOf(item);
	if (idx !== -1) list.splice(idx, 1);
	return list
}

function removeEmptyProps(obj) {
	for (const key of Object.keys(obj)) {
		if (obj[key].length == 0) {
			delete obj[key]
		}
	}
	return obj
}

function cleanParams(obj) {
	obj = removeEmptyProps(obj)
	delete obj['limit']
	delete obj['offset']

	return obj
}

export default {removeFromList, removeEmptyProps, cleanParams};