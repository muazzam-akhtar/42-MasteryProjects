import numpy as np


def slice_me(family: list, start: int, end: int) -> list:
    """

    Array is passed to this function along with two int values which
    is the starting and ending of the list. The function is used to create
    a new list which will have the range of the list from start to end and
    return it

    Args: family: list, start: int, end: int

    Return Values: List type

    """
    try:
        if not isinstance(family, list) or\
                not isinstance(start, int) or not isinstance(end, int):
            raise AssertionError("Input must be a list and 2 ints.")
        if not all(len(item) == len(family[0]) for item in family):
            raise AssertionError("Input list with different sizes.")
        print(f"My shape is : {np.array(family).shape}")
        print(f"My new shape is : {np.array(family)[start:end].shape}")
        return np.array(family)[start:end].tolist()
    except AssertionError as error:
        print("\033[31m", AssertionError.__name__ + ":", error, "\033[0m")
        return ""
