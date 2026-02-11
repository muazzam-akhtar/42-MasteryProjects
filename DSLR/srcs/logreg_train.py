from DSLR.config import Config
from DSLR.errors import errorHandler
from DSLR.model import trainOVR, predictOVR
from DSLR.modelSGD import trainOVRSGD
from DSLR.modelMBGD import trainOVRMBGD
from DSLR.utils import fetchData
from DSLR.preprocessing import cleanDF, labelsAndClasses
import numpy as np


def trainType(X, y, totalClasses, typeGD: str) -> tuple:
    """
    """
    match typeGD.lower():
        case 'batch':
            allTheta, X = trainOVR(X, y, totalClasses)

            return allTheta, X
        case 'sgd':
            allTheta, X = trainOVRSGD(X, y, totalClasses)

            return allTheta, X
        case 'mbgd':
            allTheta, X = trainOVRMBGD(X, y, totalClasses)

            return allTheta, X
        case _:
            raise ValueError('must input one of Batch, SGD, MBGD')


def train(typeGD: str) -> int:
    """
    train():

    Description:
        Loads the training data, cleans it, encodes house labels, trains\b
        classifiers, and prints accuracy. Returns 0 on success or 1 on error.
    Parameters:
        None
    Raises:
        None
    Returns:
        int:    0 on success, errorHandler returns 1 on any caught exceptions.
    """
    try:
        df = fetchData(Config.dataTrain)
        dfClean = cleanDF(df, 'train')

        X = dfClean[Config.colFeatures].to_numpy(dtype=float)

        houses = np.array(dfClean["Hogwarts House"].values)
        totalClasses, y = labelsAndClasses(houses)

        allTheta, X = trainType(X, y, totalClasses, typeGD)

        predictions, _ = predictOVR(X, allTheta)

        Config.setColour("[INFO]", 2, " Calculating Training Accuracy...")
        Config.setColour("[INFO]", 2, " Houses are labeled 0 - 3 Represeting:")
        Config.setColour("[INFO]", 2,
                         " Gryffindor: 0,"
                         " Hufflepuff: 1,"
                         " Ravenclaw : 2,"
                         " Slytherin : 3")

        accuracy = np.mean(predictions == y)
        Config.setColour("[INFO]", 2, f" Test Accuracy: {accuracy * 100:.4f}%")
        Config.setColour("[INFO]", 2, f" Predictions: {predictions}")
        Config.setColour("[INFO]", 2, f" True Labels: {y}")

    except Config.exceptions as e:
        return errorHandler(e)

    return 0


def main():
    """
    main()

    Description:
        Training model program Entrypoint.
    """
    try:
        typeGD = input('Input: Batch or SGD or MBGD\n')

        return train(typeGD)

    except Config.exceptions as e:
        return errorHandler(e)


if __name__ == "__main__":
    main()
