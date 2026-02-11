from .preprocessing import normaliseData
from .utils import saveThetas
from .config import Config
from .math import sigmoid
import numpy as np


def trainOVRMBGD(X: np.ndarray, y: np.ndarray, totalClasses: int) -> tuple:
    """
    Train a one-vs-rest (OvR) multiclass logistic regression model using
    mini-batch gradient descent (MBGD).
    """
    Config.setColour("[TRAINING STARTED]", 1,
                     " Training Started (Mini-Batch Gradient Descent)")

    try:
        X, m, n = normaliseData(X)

    except Config.exceptions as e:
        raise e

    batchSize = Config.batchSize
    allTheta = np.zeros((totalClasses, n))

    for k in range(totalClasses):
        y_k = (y == k).astype(int)

        theta = np.zeros(n)

        for _ in range(Config.epoch):
            indices = np.arange(m)
            np.random.shuffle(indices)
            shuffledX = X[indices]
            shuffledY = y_k[indices]

            for start in range(0, m, batchSize):
                end = start + batchSize
                X_batch = shuffledX[start:end]
                yBatch = shuffledY[start:end]

                h = sigmoid(np.dot(X_batch, theta))
                h = np.clip(h, 1e-12, 1 - 1e-12)

                grad = (1 / len(X_batch)) * (np.dot(X_batch.T, (h - yBatch)))
                grad = np.clip(grad, -10, 10)

                theta -= Config.learningRate * grad

        allTheta[k] = theta

    Config.setColour("[TRAINING COMPLETE]", 1)

    try:
        saveThetas(allTheta, Config.storeThetas)

    except Config.exceptions as e:
        raise e

    return allTheta, X
