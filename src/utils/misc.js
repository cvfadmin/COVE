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

export default {removeFromList, removeEmptyProps};