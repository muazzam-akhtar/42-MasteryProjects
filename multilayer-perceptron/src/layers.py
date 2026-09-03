"""
Activation functions and the DenseLayer building block.
Everything here is implemented from scratch with numpy only (no ML libraries).
"""

import numpy as np

# ---------------------------------------------------------------------------
# Activation functions.
# Each "derivative" is expressed in terms of the activation's OWN OUTPUT (A),
# which is the convenient form for backprop since we already have A cached.
# ---------------------------------------------------------------------------


def sigmoid(z):
    z = np.clip(z, -500, 500)
    return 1.0 / (1.0 + np.exp(-z))


def sigmoid_derivative(a):
    return a * (1.0 - a)


def relu(z):
    return np.maximum(0.0, z)


def relu_derivative(a):
    return (a > 0).astype(float)


def tanh(z):
    return np.tanh(z)


def tanh_derivative(a):
    return 1.0 - a ** 2


def softmax(z):
    # numerical stability
    z = z - np.max(z, axis=1, keepdims=True)
    exp_z = np.exp(z)
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)


# softmax's derivative is not applied element-wise like the others: when paired
# with categorical cross-entropy it collapses to (A - Y),
# which Network.backward
# handles directly. We still register a placeholder so the lookup table is
# complete.

ACTIVATIONS = {
    "sigmoid": (sigmoid, sigmoid_derivative),
    "relu": (relu, relu_derivative),
    "tanh": (tanh, tanh_derivative),
    "softmax": (softmax, None),
}


class DenseLayer:
    """A fully connected layer: Z = A_prev @ W + b; A = activation(Z)."""

    def __init__(
            self, output_size, activation="sigmoid",
            weights_initializer="heUniform"
    ):
        if activation not in ACTIVATIONS:
            raise ValueError(f"Unknown activation '{activation}'")
        self.output_size = output_size
        self.activation_name = activation
        self.activation, self.activation_deriv = ACTIVATIONS[activation]
        self.weights_initializer = weights_initializer

        self.input_size = None
        self.W = None
        self.b = None

        # cached values for backprop
        self.input = None
        self.Z = None
        self.A = None

        # gradients
        self.dW = None
        self.db = None

    def initialize(self, input_size, rng: np.random.RandomState):
        """Initialize W (input_size, output_size) and b(1, output_size)."""
        self.input_size = input_size
        if self.weights_initializer == "heUniform":
            limit = np.sqrt(6.0 / input_size)
            self.W = rng.uniform(
                -limit, limit, size=(input_size, self.output_size)
            )
        elif self.weights_initializer == "heNormal":
            std = np.sqrt(2.0 / input_size)
            self.W = rng.normal(
                0.0, std, size=(input_size, self.output_size)
            )
        elif self.weights_initializer == "xavier":
            limit = np.sqrt(6.0 / (input_size + self.output_size))
            self.W = rng.uniform(
                -limit, limit, size=(input_size, self.output_size)
            )
        else:
            self.W = rng.normal(
                0.0, 0.01, size=(input_size, self.output_size)
            )
        self.b = np.zeros((1, self.output_size))

    def forward(self, A_prev):
        self.input = A_prev
        self.Z = A_prev @ self.W + self.b
        self.A = self.activation(self.Z)
        return self.A

    def backward(self, dA_or_dZ, is_dZ=False):
        """
        Backprop through this layer.
        If is_dZ is True, dA_or_dZ IS already dZ (used for the output layer,
        where softmax+cross-entropy / sigmoid+BCE simplify to dZ = A - Y).
        Otherwise dA_or_dZ is dA and we multiply by the local activation
        derivative.
        Returns dA_prev to propagate to the previous layer.
        """
        m = self.input.shape[0]
        if is_dZ:
            dZ = dA_or_dZ
        else:
            dZ = dA_or_dZ * self.activation_deriv(self.A)

        self.dW = self.input.T @ dZ / m
        self.db = np.sum(dZ, axis=0, keepdims=True) / m
        dA_prev = dZ @ self.W.T
        return dA_prev

    def update(self, learning_rate):
        self.W -= learning_rate * self.dW
        self.b -= learning_rate * self.db
