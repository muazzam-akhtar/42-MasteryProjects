from typing import Any


def ft_statistics(*args: Any, **kwargs: Any) -> None:
    """
    This function computes various statistical measures, such as mean, median,
    quartiles, standard deviation, and variance, based on the input values
    provided as positional arguments. It also allows the user to specify which
    statistical measures to print using keyword arguments.

    Parameters:

    *args (Any): A variable number of positional arguments representing the
    values for statistical calculations.
    **kwargs (Any): Keyword arguments that specify which statistical measures
    to print.
    Returns:

    None: The function does not return any value. Instead, it prints the
    requested statistical measures.
    Notes:

    The function calculates mean, median, quartiles, standard deviation, and
    variance from the given positional arguments. Specific statistical measures
    can be printed by specifying them in the keyword arguments.
    """
    args_list = list(args)
    total = 0
    values = []
    num_args = 0
    for arg in args_list:
        num_args += 1
        total += arg
        values.append(arg)

    if num_args == 0:
        for value in kwargs.items():
            print("ERROR")
        return
    mean = total / num_args
    i = 0
    while i < num_args - 1:
        j = 0
        while j < num_args - i - 1:
            if values[j] > values[j + 1]:
                values[j], values[j + 1] = values[j + 1], values[j]
            j += 1
        i += 1
    median_index = num_args // 2
    if num_args % 2 == 0:
        median = (values[median_index - 1] + values[median_index]) / 2
    else:
        median = values[median_index]

    q1_index = num_args // 4
    if num_args % 2 == 0:
        lower_half = values[:median_index]
        upper_half = values[median_index:]
    else:
        lower_half = values[:median_index]
        upper_half = values[median_index + 1:]
    q1_index = len(lower_half) // 2
    if len(lower_half) % 2 == 0:
        q1 = (lower_half[q1_index - 1] + lower_half[q1_index]) / 2
    else:
        q1 = lower_half[q1_index]

    q3_index = len(upper_half) // 2
    if len(upper_half) % 2 == 0:
        q3 = (upper_half[q3_index - 1] + upper_half[q3_index]) / 2
    else:
        q3 = upper_half[q3_index]
    quartile = [q1, q3]

    variance_total = 0
    for value in values:
        variance_total += (value - mean) ** 2
    variance = variance_total / num_args
    std_deviation = (variance ** 0.5)
    result = {"mean": mean, "median": median, "quartile": quartile,
                            "std": std_deviation, "var": variance}

    for key, value in kwargs.items():
        if value in result:
            print(f"{value} : {result[value]}")
