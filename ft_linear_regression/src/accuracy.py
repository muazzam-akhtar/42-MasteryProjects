from utils import getPath
from utils import fetchData
from utils import getThetas
from estimatePrice import estimatePrice

def	getAccuracy(thetas: tuple, mileages: list, prices: list) -> float:
	"""
	Checks the accuracy of the model with the formula:
	Absolute Losses = (Sum of Squares of Residuals) / (Total Sum of Squares)
	Accuracy = 1 - Absolute Losses
	
	Arg: thetas: tuple, mileages: list, prices: list

	Returns the tuple of t0, t1, new learning rate
	"""
	price_average = sum(prices) / len(prices)
	ssr = sum(map(lambda mileage, price: pow(price - estimatePrice(thetas,
		mileage, mileages, prices), 2), mileages, prices))
	sst = sum(map(lambda price: pow(price - price_average, 2), prices))
	return (1 - (ssr / sst))

def	main():
	thetas = getThetas(getPath('thetas.csv'))
	mileages, prices = fetchData(getPath('data.csv'))
	accuracy = getAccuracy(thetas, mileages, prices) * 100
	print("Accuracy is {:.5}%".format(accuracy))

if __name__ == '__main__':
	main()