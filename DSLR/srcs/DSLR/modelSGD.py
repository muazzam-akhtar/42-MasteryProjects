from .preprocessing import normaliseData
from .utils import saveThetas
from .config import Config
from .math import sigmoid
import numpy as np


def trainOVRSGD(X: np.ndarray, y: np.ndarray, totalClasses: int) -> tuple:
    """
    trainOVRSGD(X: np.ndarray, y: np.ndarray, totalClasses: int):

    Description:
        Trains a one-vs-rest (OvR) multiclass logistic regression model using
        stochastic gradient descent (SGD). Each classifier is trained to\b
        distinguish one class from all others by updating its parameters\b
        after processing each individual training example.

        SGD updates parameters immediately after each training example:

            θ := θ - a * (hθ(x⁽ⁱ⁾) - y⁽ⁱ⁾) * x⁽ⁱ⁾

        where h_θ(x_i) = 1 / (1 + e^(-θᵀx_i))

    Parameters:
        X[np.ndarray]:      The feature matrix of shape (m, n), where m is\b
                            the number of samples and n is the number of\b
                            features. Each row represents one training example.
        y[np.ndarray]:      The vector of true class labels corresponding to\b
                            the samples in X. Labels should be encoded as\b
                            integers in the range [0, totalClasses - 1].
        totalClasses[int]:  The number of distinct output classes to train\b
                            in the one-vs-rest scheme.
    Raises:
        Config.exceptions:  If data normalization, gradient updates, or file\b
                            saving encounters an error.
        ValueError:         If the input dimensions are inconsistent or\b
                            invalid.
    Returns:
        tuple:              A tuple containing:\b
                            - allTheta[np.ndarray]: The trained weight matrix\b
                            for all classes, where each row corresponds to\b
                            one classifiers parameters.
                            - X[np.ndarray]: The normalized feature matrix\b
                            used during training.
    """
    Config.setColour("[TRAINING STARTED]", 1,
                     "Training Started (Stochastic Gradient Descent)")

    try:
        X, m, n = normaliseData(X)

    except Config.exceptions as e:
        raise e

    allTheta = np.zeros((totalClasses, n))

    for k in range(totalClasses):
        y_k = (y == k).astype(int)

        theta = np.zeros(n)

        for _ in range(Config.epoch):
            indices = np.arange(m)
            np.random.shuffle(indices)

            for i in indices:
                xi = X[i]
                yi = y_k[i]

                hi = sigmoid(np.dot(xi, theta))
                hi = np.clip(hi, 1e-10, 1 - 1e-10)

                grad = (hi - yi) * xi
                grad = np.clip(grad, -10, 10)

                theta -= Config.learningRate * grad

        allTheta[k] = theta

    Config.setColour("[TRAINING COMPLETE]", 1)

    try:
        saveThetas(allTheta, Config.storeThetas)

    except Config.exceptions as e:
        raise e

    return allTheta, X
