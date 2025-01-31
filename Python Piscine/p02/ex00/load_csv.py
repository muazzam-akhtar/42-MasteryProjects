import os
import pandas as pd


def load(path: str) -> pd.DataFrame:
    """
    Loads the csv file and returns the dataframe.
    """
    try:
        if not os.path.exists(path):
            raise FileNotFoundError("The file doesn't exist")
        if not path.lower().endswith('.csv'):
            raise ValueError("The file format is not .csv")
        if not os.access(path, os.R_OK):
            raise PermissionError("The file cannot be read")
        if os.path.isdir(path):
            raise ValueError("The file is the directory")
        dataset = pd.read_csv(path)
        if dataset.empty:
            raise ValueError("The file is empty")
        print(f"Loading dataset of dimensions {dataset.shape}")
        return dataset
    except FileNotFoundError as error:
        print(FileNotFoundError.__name__ + ":", error)
        return None
    except pd.errors.EmptyDataError:
        print("EmptyDataError: The file is empty")
        return None
    except ValueError as error:
        print(ValueError.__name__ + ":", error)
        return None
    except PermissionError as error:
        print(PermissionError.__name__ + ":", error)
    except Exception as error:
        print("An unexpected error occurred:", error)
        return None
