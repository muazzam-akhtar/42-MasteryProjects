from typing import Any


def callLimit(limit: int):
    """
    A decorator factory that limits the number of times a function
    can be called.

    Args:
        limit (int): The maximum number of times the decorated function
        can be called.
                     Once this limit is exceeded, an AssertionError
                     will be raised.

    Returns:
        Callable: A decorator (callLimiter) that wraps the target function
        and enforces the call limit.

    The decorator maintains a count of how many times the function
    has been called.
    If the function is called more than `limit` times, an AssertionError
    is raised.

    Examples:
        ->> @callLimit(3)
        ... def say_hello():
        ...     print("Hello!")
        ...
        ->> say_hello()
        Hello!
        ->> say_hello()
        Hello!
        ->> say_hello()
        Hello!
        ->> say_hello()
        Error:  <function say_hello at 0x...> call too many times
    """
    count = 0

    def callLimiter(function):
        """
        The actual decorator that enforces the call limit on the
        target function.

        Args:
            function (Callable): The function to be decorated.

        Returns:
            Callable: The wrapped function (limit_function) that enforces the
            call limit.
        """
        def limit_function(*args: Any, **kwds: Any):
            """
            The wrapper function that tracks the number of calls and enforces
            the limit.

            Args:
                *args: Positional arguments passed to the decorated function.
                **kwds: Keyword arguments passed to the decorated function.

            Returns:
                Any: The result of the decorated function if the call limit
                has not been exceeded.

            Raises:
                AssertionError: If the function is called more than
                `limit` times.
            """
            try:
                nonlocal count
                count += 1
                if count <= limit:
                    return function(*args, **kwds)
                else:
                    raise AssertionError(f"{function} call too many times")
            except AssertionError as error:
                print("Error: ", error)
        return limit_function

    return callLimiter
