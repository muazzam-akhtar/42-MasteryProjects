from .config import Config
import pandas as pd
import numpy as np
import csv as csv
import os


def getPath(filename: str):
    """
    Fetches the path of the file.

    Arg: filename: str

    Returns the path of the file in string
    """
    if os.path.basename(filename).startswith('.'):
        raise ValueError("Error: The file name should not start with '.'")

    if not filename.lower().endswith('.csv'):
        raise ValueError("Error: The file must have a .csv extension")

    if not os.access(filename, os.R_OK):
        raise PermissionError("Error: The file is not readable")

    if os.path.isdir(filename):
        raise IsADirectoryError("Error: The path provided is a directory")

    if os.path.getsize(filename) == 0:
        raise ValueError("Error: The file is empty")

    file = os.path.join(filename)

    return file


def fetchData(filePath: str) -> pd.DataFrame:
    """
    Reads and stores the data in the list

    Arg: filePath: str

    Returns the tuple of two lists-mileages, prices
    """
    try:
        df = pd.read_csv(getPath(filePath))

    except Config.exceptions as e:
        print(f"\033[91m{e}\033[0m")

        raise e

    return df


def saveThetas(params: np.ndarray, filename: str) -> None:
    """
    saveThetas(params: ndarray, filename: str):

    Description:
        Function to write values into new file from training for later use\b
        by prediction and accuracy programs. Creates new file if it doesn't\b
        exist.
    Parameters:
        params(ndarray):    Values to write into file.
        filename(str):      Name of file to write to or create.
    Raises:
        e:          Forwards any exception raised during the writing process.
    Returns:
        None
    """
    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)

            for item in params:
                writer.writerow(item)

        Config.setColour("[INFO]", 2, f" Saved allTheta to {filename}")

    except Config.exceptions as e:
        raise e


def loadThetas():
    """
    loadThetas():

    Description:
        Loads the saved theta (model weight) values from a CSV file used in\b
        training. These parameters are later used for making predictions in\b
        the logistic regression model.
    Parameters:
        None
    Raises:
        OSError:        If the theta file cannot be found or read.
        ValueError:     If the file contents are not properly formatted or\b
                        contain invalid values.
    Returns:
        allTheta[np.ndarray]:   A NumPy array containing the loaded model\b
                                parameters for all classes.
    """
    allTheta = np.loadtxt(Config.storeThetas, delimiter=",")
    Config.setColour("[INFO]", 2, " All Thetas Loaded")

    return allTheta


def savePredictions(predictions):
    """
    savePredictions(predictions: np.ndarray):

    Description:
        Saves the predicted Hogwarts house labels to a CSV file formatted\b
        for evaluation. The output file contains an index column and the\b
        corresponding predicted house name for each example.
    Parameters:
        predictions[np.ndarray]:    An array of integer house label\b
                                    predictions corresponding to the\b
                                    model output.
    Raises:
        OSError:    If the output file cannot be created or written to.
    Returns:
        None:       This function writes the predictions to a CSV file and\b
                    prints a confirmation message.
    """
    df_out = pd.DataFrame({
        "Index": np.arange(len(predictions)),
        "Hogwarts House": [Config.houses[i] for i in predictions]
    })

    df_out.to_csv(Config.predictions, index=False)

    Config.setColour("[INFO]", 2,
                     f" Saved predictions to file {Config.predictions}")
