from .preprocessing import normaliseData
from .utils import saveThetas
from .config import Config
from .math import sigmoid
import numpy as np


def trainOVR(X: np.ndarray, y: np.ndarray, totalClasses: int) -> tuple:
    """
    trainOVR(X: np.ndarray, y: np.ndarray, totalClasses: int):

    Description:
        The heart of the training model using One vs. Rest\b
        (One vs. All) multi-classifier logistic regression\b
        with gradient descent implemented:

                              m
        ∂J(θ) / ∂θj  = 1 / m  ∑  (hθ (x^(i)) - y^(i)) xj^(i)
                             i=1

        J(θ) :      Cost (loss) function for one class\b
                    (binary logistic regression).
        θ    :      Model parameters.
        m    :      Number of samples.
        x^(i):      Feature vector for the i-th trainning.
        y^(i):      True label (0 or 1 for each class).
        hθ(x)^(i):  Predicted probability.
        Xj^(i):     The j-th feature of the i-th feature\b
                    vector.
        ∂J(θ)/∂θj:  How much to adjust the weight θj during\b
                    gradient descent.

        Calls saveThetas() to write output thetas from training\b
        into a file called store_thetas.csv for later use by\b
        prediction models.
    Parameters:
        X[np.ndarray]:      The Feature columns data.
        y[np.ndarray]:      The target columns.
        totalClasses[int]:  The total number of classes.
    Raises:
        e:          Forwards exception e raised by other functions.
        ValueError: Any Value errors caught during gradient descent iteration.
    Returns:
        allTheta[np.ndarray[tuple[]]]:  The output thetas from training.
        X[np.ndarray[tuple]]:           The normalised features Data.
    """
    Config.setColour("[TRAINING STARTED]", 1)

    try:
        X, m, n = normaliseData(X)

    except Config.exceptions as e:
        raise e

    allTheta = np.zeros((totalClasses, n))

    for k in range(totalClasses):
        y_k = (y == k).astype(int)

        theta = np.zeros(n)

        for _ in range(Config.epoch):
            try:
                h = sigmoid(np.dot(X, theta))
                h = np.clip(h, 1e-12, 1 - 1e-12)

                grad = (1 / m) * (np.dot(X.T, (h - y_k)))
                grad = np.clip(grad, -10, 10)

                theta -= Config.learningRate * grad

            except ValueError as e:
                raise e

        allTheta[k] = theta

    Config.setColour("[TRAINING COMPLETE]", 1)

    try:
        saveThetas(allTheta, Config.storeThetas)

    except Config.exceptions as e:
        raise e

    return allTheta, X


def predictOVR(X: np.ndarray, allTheta: np.ndarray):
    """
    predictOVR(X: np.ndarray, allTheta: np.ndarray)

    Description:
        The prediction model, calls on sigmoid passing in X and allTheta\b
        to run probabilities for each class, then selects the highest\b
        probability for each class.
    Parameters:
        X[np.ndarray]:          The features columns data.
        allTheta[np.ndarray]:   The thetas for each feature.
    Raises:
        e:      The caught exception from called functions.
    Returns:
        tuple(predictions[np.ndarray], probs[np.ndarray])
    """
    try:
        probs = sigmoid(np.dot(X, allTheta.T))
        predictions = np.argmax(probs, axis=1)

    except Config.exceptions as e:
        raise e

    return predictions, probs
