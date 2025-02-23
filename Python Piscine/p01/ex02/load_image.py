import numpy as np
from PIL import Image
import os


def ft_load(path: str) -> np.ndarray:
    """

    The function is to load the .jpeg or .jpg file which is passed
    to the function and return the values in array which is in
    3 x 3 dimension.

    Args: Path of the .jpg or .jpeg file

    Return Values: np.ndarray

    """
    try:
        if not path.lower().endswith(("jpg", "jpeg")):
            raise AssertionError("Only JPG or JPEG formats are supported.")
        if not os.path.exists(path):
            raise AssertionError("File not found", path)
        img = Image.open(path)
        print(f"The shape of Image is: {img.size[1]},\
              {img.size[0]}, {img.layers}")
        return np.array(img)

    except AssertionError as error:
        print("\033[31m", AssertionError.__name__ + ":", error, "\033[0m")
        return ""
