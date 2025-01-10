def	normalizeElem(elem: float, _max: float, _min: float) -> float:
	"""
	Finding the normalized elem which is in the range of (0, 1)

	Args: elem: float, _max: float, _min: float

	Returns the float value
	"""
	return ((elem - _min) / (_max - _min))

def	denormalizeElem(elem: float, _max: float, _min: float) -> float:
	"""
	Finding the elem which is in the range of (_min, _max)

	Args: elem: float, _max: float, _min: float

	Returns the float value
	"""
	return ((elem * (_max - _min)) + _min)

def	normalizeData(data: list) -> list:
	"""
	Calculating the normalized elements of the given list

	Args: data: list

	Returns the list of normalized elements
	"""
	_result = []
	for i in data:
		_result.append(normalizeElem(i, max(data), min(data)))
	return (_result)

def	findLosses(t0: float, t1: float, mileages: list, prices: list) -> float:
	"""
	Calculating the losses with given line equation and the observed data values

	Args: t0: float, t1: float, mileages: list, prices: list

	Returns the float value
	"""
	loss = 0.0
	for mileage, price in zip(mileages, prices):
		loss += (price - ((t1 * mileage) + t0)) ** 2
	return loss / len(mileages)