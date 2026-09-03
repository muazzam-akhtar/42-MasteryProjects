"""
Program 2/3 - Trains the multilayer perceptron with backpropagation and
mini-batch gradient descent, then saves the model to disk.

Usage:
    python train.py --train out/train.csv --valid out/val.csv \
        --layer 24 24 --epochs 84 --batch_size 8 --learning_rate 0.0314

Network topology can also be described in a small config file and loaded with
--config (one Python-literal list per hidden layer size), e.g.:
    python train.py --train out/train.csv --valid out/val.csv
      --config network.txt
"""

import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from layers import DenseLayer
from network import Network
from data import (
    load_csv,
    prepare_features_labels,
    standardize_fit,
    standardize_apply,
    one_hot
    )
from losses import (
    categorical_cross_entropy, accuracy,
    precision_score, recall_score, f1_score
)

matplotlib.use("Agg")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Multilayer Perceptron - Training",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--train", required=True, help="Path to training CSV file"
    )
    parser.add_argument(
        "--valid", required=True, help="Path to validation CSV file"
    )
    parser.add_argument(
        "--layer", nargs="+", type=int, default=[24, 24],
        help="Sizes of the hidden layers, e.g. --layer 24 24 24"
    )
    parser.add_argument(
        "--activation", type=str, default="sigmoid",
        choices=["sigmoid", "relu", "tanh"],
        help="Activation function used by hidden layers"
    )
    parser.add_argument(
        "--weights_initializer", type=str, default="heUniform",
        choices=["heUniform", "heNormal", "xavier"]
    )
    parser.add_argument("--epochs", type=int, default=2000)
    parser.add_argument(
        "--loss", type=str, default="categoricalCrossEntropy",
        choices=["categoricalCrossEntropy"],
        help="Loss optimized during training"
    )
    parser.add_argument("--batch_size", type=int, default=8)
    parser.add_argument("--learning_rate", type=float, default=0.0314)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output", type=str, default="saved_model.pkl",
        help="Where to save the model"
    )
    parser.add_argument(
        "--early_stopping", action="store_true",
        help="Stop training once validation loss stops improving (bonus)"
    )
    parser.add_argument(
        "--patience", type=int, default=10,
        help="Epochs to wait for improvement before early stopping"
    )
    parser.add_argument(
        "--plot", type=str, default="learning_curves.png",
        help="Output path for the learning-curve figure"
    )
    return parser.parse_args()


def build_network(
        input_size, hidden_sizes, activation, weights_initializer, seed
):
    net_layers = []
    for size in hidden_sizes:
        net_layers.append(
            DenseLayer(
                size, activation=activation,
                weights_initializer=weights_initializer
            )
        )
    # Output layer: 2 neurons (benign / malignant) with softmax
    net_layers.append(
        DenseLayer(2, activation="softmax",
                   weights_initializer=weights_initializer)
    )
    net = Network(net_layers, seed=seed)
    net.compile(input_size)
    return net


def iterate_minibatches(X, Y, batch_size, rng):
    m = X.shape[0]
    indices = rng.permutation(m)
    for start in range(0, m, batch_size):
        idx = indices[start: start + batch_size]
        yield X[idx], Y[idx]


def plot_learning_curves(history, output_path):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].plot(history["loss"], label="training loss")
    axes[0].plot(
        history["val_loss"],
        label="validation loss",
        linestyle="--"
    )
    axes[0].set_xlabel("epochs")
    axes[0].set_ylabel("loss")
    axes[0].set_title("Loss")
    axes[0].legend()

    axes[1].plot(history["acc"], label="training acc")
    axes[1].plot(
        history["val_acc"],
        label="validation acc",
        linestyle="--"
    )
    axes[1].set_xlabel("epochs")
    axes[1].set_ylabel("acc")
    axes[1].set_title("Accuracy")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)


def main():
    args = parse_args()
    try:
        train_df = load_csv(args.train)
        valid_df = load_csv(args.valid)

        X_train, y_train = prepare_features_labels(train_df)
        X_valid, y_valid = prepare_features_labels(valid_df)

        # Fit normalization on TRAIN only, then apply the same stats
        # to validation
        mean, std = standardize_fit(X_train)
        X_train = standardize_apply(X_train, mean, std)
        X_valid = standardize_apply(X_valid, mean, std)

        Y_train = one_hot(y_train)
        Y_valid = one_hot(y_valid)

        print(f"x_train shape : {X_train.shape}")
        print(f"x_valid shape : {X_valid.shape}")

        net = build_network(
            X_train.shape[1], args.layer, args.activation,
            args.weights_initializer, args.seed
        )

        rng = np.random.RandomState(args.seed)
        history = {"loss": [], "val_loss": [], "acc": [], "val_acc": [],
                   "val_precision": [], "val_recall": [], "val_f1": []}

        best_val_loss = np.inf
        patience_counter = 0
        best_snapshot = None
        loss_func = {
            "categoricalCrossEntropy": categorical_cross_entropy
        }

        for epoch in range(1, args.epochs + 1):
            for X_batch, Y_batch in iterate_minibatches(
                X_train, Y_train, args.batch_size, rng
            ):
                net.forward(X_batch)
                net.backward(Y_batch)
                net.update(args.learning_rate)

            train_pred = net.forward(X_train)
            train_loss = loss_func[args.loss](Y_train, train_pred)
            train_acc = accuracy(Y_train, train_pred)

            val_pred = net.forward(X_valid)
            val_loss = loss_func[args.loss](Y_valid, val_pred)
            val_acc = accuracy(Y_valid, val_pred)
            val_precision = precision_score(Y_valid, val_pred)
            val_recall = recall_score(Y_valid, val_pred)
            val_f1 = f1_score(Y_valid, val_pred)

            history["loss"].append(train_loss)
            history["val_loss"].append(val_loss)
            history["acc"].append(train_acc)
            history["val_acc"].append(val_acc)
            history["val_precision"].append(val_precision)
            history["val_recall"].append(val_recall)
            history["val_f1"].append(val_f1)

            print(
                f"epoch {epoch:02d}/{args.epochs} - loss: {train_loss:.4f} - "
                f"val_loss: {val_loss:.4f} - acc: {train_acc:.4f} - "
                f"val_acc: {val_acc:.4f} - val_prec: {val_precision:.4f} - "
                f"val_recall: {val_recall:.4f} - val_f1: {val_f1:.4f}"
            )
            if args.early_stopping:
                if val_loss < best_val_loss - 1e-6:
                    best_val_loss = val_loss
                    patience_counter = 0
                    best_snapshot = net.get_weights_snapshot()
                else:
                    patience_counter += 1
                    if patience_counter >= args.patience:
                        print(f"> early stopping triggered at epoch {epoch}")
                        break

        if args.early_stopping and best_snapshot is not None:
            net.restore_weights_snapshot(best_snapshot)

        net.save(args.output, mean=mean, std=std)
        print(f"> saving model '{args.output}' to disk...")

        plot_learning_curves(history, args.plot)
        print(f"> learning curves saved to '{args.plot}'")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
