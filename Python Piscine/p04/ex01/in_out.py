def square(x: int | float) -> int | float:
    """
    Calculate the square of a given number.

    Args:
        x (int | float): The number to be squared.
        Can be either an integer or a float.

    Returns:
        int | float: The square of the input number.
        The return type will match the input type.
            If the input is an integer, the output will be an integer.
            If the input is a float, the output will be a float.

    Examples:
        ->> square(4)
        16
        ->> square(2.5)
        6.25
    """
    return x * x


def pow(x: int | float) -> int | float:
    """
    Calculate the power of a number raised to itself.

    Args:
        x (int | float): The base number. Can be either an integer or a float.

    Returns:
        int | float: The result of raising `x` to the power of `x`.
        The return type will match the input type.
                     If the input is an integer, the output will be an integer.
                     If the input is a float, the output will be a float.

    Examples:
        ->> pow(2)
        4
        ->> pow(3.0)
        27.0
    """
    return x ** x


def outer(x: int | float, function) -> object:
    """
    Create a closure that applies a given function to a value and updates
    the value with the result.

    Args:
        x (int | float): The initial value to be used by the inner function.
        Can be either an integer or a float.
        function (callable): A function that takes a single argument (of type
        int or float) and returns a value.
                             This function will be applied to `x` each time
                             the inner function is called.

    Returns:
        object: A closure (inner function) that, when called, applies
        `function` to the current value of `x`,
                updates `x` with the result, and returns the result.

    Examples:
        ->> def square(y):
        ...     return y * y
        ->> closure = outer(2, square)
        ->> closure()
        4
        ->> closure()
        16
        ->> closure()
        256
    """
    def inner() -> float:
        nonlocal x
        res = function(x)
        x = res
        return res
    return inner
