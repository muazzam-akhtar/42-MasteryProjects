from DSLR.utils import fetchData, loadThetas, savePredictions
from DSLR.preprocessing import normaliseData, cleanDF
from DSLR.config import Config
from DSLR.model import predictOVR
from DSLR.errors import errorHandler


def predict() -> int:
    """
    predict():

    Description:
        Generates Hogwarts house predictions for the test dataset using the\b
        trained one-vs-rest logistic regression model. The function loads\b
        the test data, applies preprocessing and normalization, performs\b
        prediction, and saves the results to a CSV file.
    Parameters:
        None
    Raises:
        e:      If there is an error during data loading, preprocessing, or\b
                prediction.
    Returns:
        int:    Returns 0 on successful prediction and file save operation,\b
                or the error handler's return code on failure.
    """
    try:
        df = fetchData(Config.dataTest)
        allTheta = loadThetas()

        X = cleanDF(df, 'predict')
        X = X[Config.colFeatures].to_numpy(dtype=float)
        X, _, _ = normaliseData(X, mode=1)

        predictions, _ = predictOVR(X, allTheta)
        Config.setColour("[PREDICTIONS COMPLETE]", 1)

        savePredictions(predictions)

    except Config.exceptions as e:
        return errorHandler(e)

    return 0


def main():
    """
    main(None):

    Description:
        Entry point to predict program.
    """
    return predict()


if __name__ == "__main__":
    main()
