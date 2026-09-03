"""
Network: chains DenseLayer objects, runs feedforward/backpropagation,
and persists (topology + weights + normalization stats) to disk.
"""


import pickle
import numpy as np

from layers import DenseLayer


class Network:
    def __init__(self, layers: DenseLayer, seed=None):
        self.layers = layers
        self.seed = seed

    def compile(self, input_size):
        """Initialize every layer's weights given the input feature count."""
        rng = np.random.RandomState(self.seed)
        prev = input_size
        for layer in self.layers:
            layer.initialize(prev, rng)
            prev = layer.output_size

    def forward(self, X):
        A = X
        for layer in self.layers:
            A = layer.forward(A)
        return A

    def backward(self, Y):
        """
        Y: (m, num_classes) one-hot ground truth.
        Assumes the output layer uses softmax + categorical cross-entropy
        (or sigmoid + binary cross-entropy), both of which simplify the
        output layer's dZ to (A - Y). Every earlier layer uses the ordinary
        chain rule with its own activation derivative.
        """
        output_layer = self.layers[-1]
        dZ = output_layer.A - Y
        dA = output_layer.backward(dZ, is_dZ=True)
        for layer in reversed(self.layers[:-1]):
            dA = layer.backward(dA)

    def update(self, learning_rate):
        for layer in self.layers:
            layer.update(learning_rate)

    def get_weights_snapshot(self):
        return [(layer.W.copy(), layer.b.copy()) for layer in self.layers]

    def restore_weights_snapshot(self, snapshot):
        for layer, (W, b) in zip(self.layers, snapshot):
            layer.W = W
            layer.b = b

    def save(self, path, mean=None, std=None):
        state = {
            "output_sizes": [layer.output_size for layer in self.layers],
            "activations": [layer.activation_name for layer in self.layers],
            "weights_initializers": [
                layer.weights_initializer for layer in self.layers
            ],
            "weights": [layer.W for layer in self.layers],
            "biases": [layer.b for layer in self.layers],
            "mean": mean,
            "std": std,
        }
        with open(path, "wb") as f:
            pickle.dump(state, f)

    @staticmethod
    def load(path):
        with open(path, "rb") as f:
            state = pickle.load(f)

        layers = []
        for size, act, winit in zip(
            state["output_sizes"],
            state["activations"],
            state["weights_initializers"]
        ):
            layers.append(
                DenseLayer(
                    size, activation=act,
                    weights_initializer=winit
                )
            )
        net = Network(layers)
        for layer, W, b in zip(
            net.layers, state["weights"], state["biases"]
        ):
            layer.W = W
            layer.b = b
            layer.input_size = W.shape[0]

        return net, state["mean"], state["std"]
