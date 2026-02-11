import numpy as np


def count(values: str) -> int:
    return len(values)


def mean(values: str) -> float:
    if len(values) == 0:
        return float('nan')
    return sum(values) / len(values)


def minimum(values: str) -> float:
    if len(values) == 0:
        return float('nan')
    return min(values)


def maximum(values: str) -> float:
    if len(values) == 0:
        return float('nan')
    return max(values)


def var(values: str) -> float:
    if len(values) < 2:
        return float('nan')
    mean_value = mean(values)
    variance = sum((x - mean_value) ** 2 for x in values) / (len(values) - 1)
    return variance


def std(values: str) -> float:
    if len(values) < 2:
        return float('nan')
    return var(values) ** 0.5


def cov(values: str) -> float:
    if len(values) < 2:
        return float('nan')
    return (std(values) / mean(values))


def skew(values: str) -> float:
    if len(values) < 2:
        return float('nan')
    n = len(values)
    sum_cubed_deviations = sum([(x - mean(values)) ** 3 for x in values])
    return (n / ((n - 1) * (n - 2))
            ) * (sum_cubed_deviations / (std(values) ** 3))


def percentile(values: str, percent: float) -> float:
    if len(values) == 0:
        return float('nan')
    sorted_values = sorted(values)
    k = (len(sorted_values) - 1) * percent
    f = int(k)
    c = k - f
    if f + 1 < len(sorted_values):
        return sorted_values[f] + c * (sorted_values[f + 1] - sorted_values[f])
    else:
        return sorted_values[f]


def sigmoid(z: np.ndarray):
    """
    sigmoid(z: np.ndarray):

    Description:
        The sigmoid logistic function with clipping of values > < 500 to \b
        avoid exploding values to NaN or Inf.

        g(z) = 1 / 1 + e^-z

        g is the resulting probability between 1 and 0.
        e is eulers number (~2.71828)
        -z is the negative of the input used in exponent to squash +ve/-ve\b
        values.
    Parameters:
        z[np.ndarray]:     The dot product of features and weights.
    Raises:
        None
    Returns:
        z[any]
    """
    z = np.clip(z, -20, 20)
    z = 1 / (1 + np.exp(-z))

    return z
