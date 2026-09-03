"""
Program 1/3 - Splits the raw dataset into a training set and a validation set.

Usage:
    python split.py --input data.csv --train ./out --valid_size 0.2 --seed 42
"""

import os
import csv
import argparse
import config

from data import load_csv
from colorama import init


def parse_args():
    parser = argparse.ArgumentParser(
        description="Multilayer Perceptron - Dataset splitting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--input", required=True, help="Input CSV file path"
    )
    parser.add_argument(
        "--train", required=True,
        help="Output folder where train.csv / val.csv will be written"
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--valid_size", type=float, default=0.3,
        help="Fraction of the dataset for validation (default 0.3)"
    )
    return parser.parse_args()


def write_csv(path, dataframe):
    with open(path, "w", newline="\n") as f:
        writer = csv.writer(f)
        for row in dataframe.values:
            writer.writerow(row)


def split(data, valid_size, seed):
    train = data.sample(frac=1 - valid_size, random_state=seed)
    val = data.drop(train.index)
    return train, val


def main():
    args = parse_args()
    try:
        data = load_csv(args.input)
        train, val = split(data, args.valid_size, args.seed)

        os.makedirs(args.train, exist_ok=True)
        train_path = os.path.join(args.train, "train.csv")
        val_path = os.path.join(args.train, "val.csv")
        write_csv(train_path, train)
        write_csv(val_path, val)

        title = "Splitting completed successfully!"
        row1 = f"Training data shape: {train.shape}"
        row2 = f"Validation data shape: {val.shape}"
        lines = [title, row1, row2]
        width = max(len(line) for line in lines) + 4

        init(autoreset=True)
        print(config.B_WHITE + "-" * width)
        print(
            "| " + config.B_YELLOW + title.center(width - 4)
            + config.B_WHITE + " |"
        )
        print(config.B_WHITE + f"| {row1.center(width - 4)} |")
        print(config.B_WHITE + f"| {row2.center(width - 4)} |")
        print(config.B_WHITE + "-" * width)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
