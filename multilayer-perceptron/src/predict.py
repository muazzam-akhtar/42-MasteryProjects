"""
Program 3/3 - Loads a trained model, predicts on a given dataset, and
evaluates it with the binary cross-entropy error function from the subject:

    E = -(1/N) * sum_n [ y_n * log(p_n) + (1 - y_n) * log(1 - p_n) ]

Usage:
    python predict.py --dataset out/val.csv --model saved_model.pkl
"""

import argparse

from network import Network
from losses import (
    binary_cross_entropy, accuracy, precision_score,
    recall_score, f1_score, confusion_counts
)
from data import (
    load_csv,
    prepare_features_labels,
    one_hot,
    standardize_apply
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Multilayer Perceptron - Prediction",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--dataset", required=True,
        help="CSV file to run predictions on"
    )
    parser.add_argument(
        "--model", default="saved_model.pkl",
        help="Path to the saved model"
    )
    parser.add_argument(
        "--show", type=int, default=10,
        help="Number of individual example predictions to print"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        net, mean, std = Network.load(args.model)

        df = load_csv(args.dataset)
        X, y = prepare_features_labels(df)
        X = standardize_apply(X, mean, std)
        Y = one_hot(y)

        predictions = net.forward(X)    # (m, 2) -> [P(benign), P(malignant)]
        p_malignant = predictions[:, 1]
        loss = binary_cross_entropy(y, p_malignant)
        acc = accuracy(Y, predictions)
        precision = precision_score(Y, predictions)
        recall = recall_score(Y, predictions)
        f1 = f1_score(Y, predictions)
        tp, fp, tn, fn = confusion_counts(Y, predictions)

        print(f"x_shape: {X.shape}")
        print(f"Binary cross-entropy error: {loss:.4f}")
        print(f"Accuracy:  {acc:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1-score:  {f1:.4f}")
        print(f"Confusion matrix: TP={tp}  FP={fp}  TN={tn}  FN={fn}")
        n_show = min(args.show, len(y))
        if n_show > 0:
            print("\nSample predictions:")
            for i in range(n_show):
                true_label = "M" if y[i] == 1 else "B"
                pred_label = "M" if p_malignant[i] > 0.5 else "B"
                print(
                    f"  example {i:3d}: true= {true_label} pred={pred_label} "
                    f"P(M)={p_malignant[i]:.4f}"
                )
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
