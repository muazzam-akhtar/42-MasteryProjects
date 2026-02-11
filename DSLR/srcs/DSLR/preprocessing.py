from .config import Config

import pandas as pd
import numpy as np
import os as os


def labelsAndClasses(houses: np.ndarray) -> tuple[int, np.ndarray]:
    """
    labelsAndClasses(houses: np.ndarray):

    Description:
        Function that sorts the 'target' column into unique classes, and\b
        replaces the str labels with integers from 0 - 3 for training\b
        purposes of y.
    Parameters:
        houses[np.ndarray]:     Numpy Array of 'Hogwarts House' column in\b
                                DataFrame.
    Raises:
        None
    Returns:
        tuple[int, np.ndarray]: Total classes and array of classes.
    """
    uniqueClasses = sorted(set(houses))
    totalClasses = len(uniqueClasses)

    labelToIndex = {label: i for i, label in enumerate(uniqueClasses)}
    y = np.array([labelToIndex[label] for label in houses])

    return totalClasses, y


def normaliseData(X: np.ndarray, mode=0) -> tuple[np.ndarray, int, int]:
    """
    normaliseData(X: np.ndarray):

    Description:
        Function to normalise and scale data to avoid exploding values with\b
        bias column added. Mean and STD are calculated and stored in \b
        Config.normData as file.
    Parameters:
        X[np.ndarray]:      Numpy array with feature values for x.
    Raises:
        e:      If any errors load/save file or calculating values.
    Returns:
        tuple[np.ndarray, int, int]:    Array X for normalised data and shape\b
                                        (m, n)
    """
    m, _ = X.shape

    try:
        if mode == 1:
            norm = np.load(Config.normData)
            mean, std = norm["mean"], norm["std"]

        else:
            if os.path.exists(Config.normData):
                Config.setColour("[INFO]",
                                 2,
                                 " Old norm_params.npz found and Removed.")

                os.remove(Config.normData)

            mean = np.mean(X, axis=0)
            std = np.std(X, axis=0)

            Config.setColour("[INFO]", 2,
                             " STD and MEAN stored in norm_params.npz.")

            np.savez(Config.normData, mean=mean, std=std)

    except Config.exceptions as e:
        raise e

    X = (X - mean) / std
    X = np.c_[np.ones((m, 1)), X]

    return X, m, X.shape[1]


def fillTrainDataNaN(df: pd.DataFrame, numCols: list[str]) -> pd.DataFrame:
    """
    fillTrainDataNaN(df: pd.DataFrame, numCols: list[str]):

    Desciption:
        Fills NaN Values with mean values of each class.
    Parameters:
        df[pd.dataFrame]:       The DataFrame.
        numCols[list[str]]:     The columns with numbers.
    Raises:
        None
    Returns:
        df[pd.DataFrame]:       The DataFrame with NaNs filled in.
    """
    if "Hogwarts House" in df.columns:
        for col in numCols:
            if col != "Index":
                df[col] = df.groupby("Hogwarts House")[col].transform(
                    lambda x: x.fillna(x.mean())
                )

    return df


def cleanDF(df: pd.DataFrame, caller=None) -> pd.DataFrame:
    """
    cleanDF(df: pd.DataFrame, caller=None):

    Description:
        Function to clean DataFrame from NaN values in features by filling\b
        all NaNs with mean of class feature values depending on Training or\b
        prediction models. This function will fill NaN values with mean of\b
        each class if 'caller=train', or mode of column if 'caller=predict'.
    Parameters:
        df[pd.DataFrame]:   The pandas DataFrame to clean.
        caller[str | None]: The model calling the function to clean.\b
    Raises:
        AssertionError:     If no caller added.
    Returns:
        df[pd.DataFrame]:   The cleaned DataFrame.
    """
    assert caller is not None, "cleanDF need caller='train/predict'"

    dropCols = ["First Name", "Last Name", "Birthday", "Best Hand"]
    df = df.drop(columns=dropCols, errors='ignore')

    numCols = df.select_dtypes(include=['float64']).columns.tolist()

    if caller == "train":
        df = fillTrainDataNaN(df, numCols)

    else:
        for col in numCols:
            mean_val = df[col].mean()
            df[col] = df[col].fillna(mean_val)

    return df
