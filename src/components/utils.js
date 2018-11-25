function removeFromList (item, list) {
	let idx = list.indexOf(item);
	if (idx !== -1) list.splice(idx, 1);
	return list
}

export default removeFromList;