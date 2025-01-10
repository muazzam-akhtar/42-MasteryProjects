from utils import getThetas
from utils import getPath
from utils import fetchData
from math_utils import denormalizeElem
from math_utils import normalizeElem
import os

def	estimatePrice(thetas: tuple, mileage: float, mileages: list, prices: list) -> float:
	"""
	Estimates the price with the given mileage, lists of observed data based on the
	predicted model of theta values
	
	Arg: filePath: str

	Returns the tuple of two floats- (t0, t1)
	"""
	normalized_mileage = normalizeElem(mileage, max(mileages), min(mileages))
	predicted_price = (thetas[1] * normalized_mileage) + thetas[0]
	return(denormalizeElem(predicted_price, max(prices), min(prices)))

if __name__ == '__main__':
	mileage = input("Enter mileage: ")
	thetas = getThetas(getPath('thetas.csv'))
	if os.path.exists('thetas.csv') and (thetas[0] != 0 or thetas[1] != 0):
		mileages, prices = fetchData(getPath('data.csv'))
		print(estimatePrice(thetas, float(mileage), mileages, prices))
	else:
		print(0.0)
