from DSLR.config import Config
from DSLR.errors import errorHandler
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np


def checkAccuracy(pathTruth, pathPredict):
    """
    checkAccuracy(pathTruth: str, pathPredict: str):

    Description:
        Compares the predicted Hogwarts house classifications with the true\b
        labels to evaluate model accuracy. The function loads both CSV\b
        files, prints a comparison sample, calculates accuracy, displays\b
        error statistics, and lists the misclassified rows with their indices.
    Parameters:
        pathTruth[str]:     Path to the CSV file containing the true\b
                            Hogwarts House labels.
        pathPredict[str]:   Path to the CSV file containing the predicted\b
                            Hogwarts House labels.
    Raises:
        e:      If either of the provided CSV files cannot be opened or read.
    Returns:
        int:    Returns 0 after displaying the calculated accuracy and error\b
                information.
    """
    Config.setColour("[LOADING FILES]\n", 1,
                     f'\t{pathTruth}\n\t{pathPredict}\n')

    try:
        dfTruth = pd.read_csv(pathTruth)
        dfPredict = pd.read_csv(pathPredict)

    except Config.exceptions as e:
        return errorHandler(e)

    Config.setColour("[CALCULATING ACCURACY]\n", 1)

    fullDF = pd.concat([dfPredict.head(10), dfTruth.head(10)], axis=1)
    Config.setColour('[INFO]', 2, "     True Values:     Predicted Values:")
    print(f'{fullDF}\n')

    yTrue = np.array(dfTruth['Hogwarts House'].values)
    yPred = np.array(dfPredict['Hogwarts House'].values)

    accuracy = accuracy_score(y_true=yTrue, y_pred=yPred)
    Config.setColour("[INFO]", 2, f" Test Accuracy: {accuracy * 100:.2f}%")

    errorRows = dfPredict.loc[yTrue != yPred]
    Config.setColour("[INFO]", 2, f" Truth CSV Shape: {dfTruth.shape}")
    Config.setColour("[INFO]", 2, f" Error shape: {errorRows.shape}")

    prcntError = (errorRows.shape[0] * 100) / dfTruth.shape[0]
    Config.setColour("[INFO]", 2, f" Percentage Error: {prcntError}%\n")

    Config.setColour("[INFO]", 2, f" Inaccurate rows: ({errorRows.shape[0]})")
    Config.setColour("[INFO]", 2, " Index:   House:")
    for item in errorRows.values:
        print(f'\t{item[0]}\t{item[1]}')

    return 0


def main():
    """
    main()

    Description:
        Entrypoint to accuracy program.
    """
    try:
        path = input('Input: Path to true labels CSV file\n')

        return checkAccuracy(path, Config.predictions)

    except Config.exceptions as e:
        return errorHandler(e)


if __name__ == "__main__":
    main()
