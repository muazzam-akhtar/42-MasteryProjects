"""
Data loading & preprocessing helpers shared by split.py,
train.py and predict.py.

Expected raw CSV format (Wisconsin Breast Cancer dataset, no header row):
    column 0  -> id (dropped)
    column 1  -> diagnosis ('M' or 'B')
    columns 2..31 -> 30 numeric features
"""

import numpy as np
import pandas as pd

LABEL_MAP = {"M": 1, "B": 0}


def load_csv(path: str) -> pd.DataFrame:
    """Load a raw or split CSV file. No header is expected in this dataset."""
    df = pd.read_csv(path, header=None)
    if df.empty:
        raise ValueError(f"'{path}' is empty.")
    return df


def prepare_features_labels(df: pd.DataFrame):
    """
    Split a raw dataframe into:
        X: (m, 30) float feature matrix
        y: (m,) int labels (1 = malignant, 0 = benign)
    """
    # Guard against a stray header/column-index row (e.g. produced by an old
    # buggy split script that wrote "0,1,2,...,31" as a literal first line).
    # If the diagnosis column's first value isn't M/B, drop that one row.
    first_val = df.iloc[0, 1]
    if first_val not in ("M", "B"):
        print(
            f"Warning: dropping unexpected first row "
            f"(diagnosis='{first_val}'); "
            f"looks like a leftover header row."
        )
        df = df.iloc[1:].reset_index(drop=True)

    labels = df.iloc[:, 1].map(LABEL_MAP)
    if labels.isnull().any():
        bad_values = df.iloc[:, 1][labels.isnull()].unique()
        raise ValueError(
            f"Found diagnosis value(s) other than 'M'/'B': {list(bad_values)}."
            f" Check that column 1 of your CSV really is the diagnosis column "
            f"and that the file has no header row."
        )
    y = labels.values.astype(int)
    X = df.iloc[:, 2:].values.astype(float)
    return X, y


def standardize_fit(X: np.ndarray):
    """Compute mean / std on TRAINING data only."""
    mean = X.mean(axis=0)
    std = X.std(axis=0)
    std[std == 0] = 1.0
    return mean, std


def standardize_apply(
        X: np.ndarray, mean: np.ndarray, std: np.ndarray
) -> np.ndarray:
    return (X - mean) / std


def one_hot(y: np.ndarray, num_classes: int = 2) -> np.ndarray:
    Y = np.zeros((y.shape[0], num_classes))
    Y[np.arange(y.shape[0]), y.astype(int)] = 1
    return Y
