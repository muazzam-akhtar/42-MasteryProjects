from __future__ import annotations


def give_bmi(height: list[int | float], weight: list[int | float])\
        -> list[int | float]:

    """
    Calculate the BMI with given weight and height.

    Args:
        height: list[int | float], weight: list[int | float]

    Returns:
        Returns te list of BMI based on the height and weight values
    """

    # -------------------- >	Check for Errors	< --------------------

    try:
        if len(height) != len(weight):
            raise AssertionError("The size is unequal!")
        if not isinstance(height, list) or not isinstance(weight, list):
            raise AssertionError("The type of arguments are not valid")
        for i in range(len(height)):
            if (not isinstance(height[i], int) and
                not isinstance(height[i], float) or
                not isinstance(weight[i], int)
                    and not isinstance(weight[i], float)):
                raise AssertionError("The type of element of list is invalid")

    # --------------------------->	Execution	<---------------------------

        bmi = []
        for i in range(len(height)):
            bmi.append(weight[i] / (height[i] * height[i]))
        return bmi
    except AssertionError as error:
        print("\033[31m]", AssertionError.__name__ + ":", error, "\033[0m")
        return ""


def apply_limit(bmi: list[int | float], limit: int) -> list[bool]:
    """
    Comparing the elements of BMI with the limit.

    Args:
        bmi: list[int | float], limit: int

    Returns:
        Returns the list of elements which is greater than the limit.
    """

    # ------------------->	Check for Errors	<-------------------

    try:
        if not isinstance(bmi, list) and not isinstance(limit, int):
            raise AssertionError("The type of arguments are not valid")
        for elem in bmi:
            if not isinstance(elem, int) and not isinstance(elem, float):
                raise AssertionError("The type of element of list is invalid")

    # -------------------------->	Execution	<--------------------------

        _result = []
        for i in bmi:
            _values = True if i > limit else False
            _result.append(_values)
        return _result

    except AssertionError as error:
        print("\033[31m]", AssertionError.__name__ + ":", error, "\033[0m")
        return ""
