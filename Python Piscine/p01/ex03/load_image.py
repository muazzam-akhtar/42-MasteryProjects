import numpy as np
from PIL import Image
import os


def print_rows_first_elem(arr, int):
    """
    A function that reads and prints the first element of each row.
    """
    count = 0
    for row in arr:
        count += 1
    length = count
    count = 0
    for row in arr:
        if count == 0:
            print("[[[" if int == 1 else "[[", row[0], "]", sep="")
        if count > 0 and count < 3 or count > length - 4:
            if int == 1:
                if count == length - 1:
                    print("  [", row[0], "]]]", sep="")
                elif count < length - 1:
                    print("  [", row[0], "]", sep="")
            else:
                print("  ", row[0], "]]" if count == (length - 1)
                      else "", sep="")
        if count == 2:
            print(" ...")
        count += 1


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
        print(
            f"The shape of Image is: "
            f"({img.size[0]}, {img.size[1]}, {img.layers})"
            )
        print_rows_first_elem(np.array(img), 1)
        return np.array(img)

    except AssertionError as error:
        print("\033[31m", AssertionError.__name__ + ":", error, "\033[0m")
        return ""
