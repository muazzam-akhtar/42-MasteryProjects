#!/usr/bin/env python3
"""
mybci.py

Usage
-----
    python mybci.py <subject> <run> train
        Train the pipeline on the given subject/run's experiment group,
        print the per-fold cross_val_score and its mean, and save the
        fitted pipeline to disk.

    python mybci.py <subject> <run> predict
        Reload the saved pipeline and "replay" the held-out test epochs
        one at a time (simulating a live data stream), printing the
        prediction vs. ground truth for each epoch, and the final
        accuracy. Each prediction is timed to confirm it completes
        well under the 2s constraint.

    python mybci.py
        No arguments: run train+predict for all 6 experiments across
        all subjects, and print the mean accuracy table.

Example
-------
    python mybci.py 4 14 train
    python mybci.py 4 14 predict
    python mybci.py
"""

import sys
import numpy as np
import warnings
import time
from Config import Config
from errors import errorHandler
from utils import BAD_SUBJECTS, EXPERIMENTS, get_dataset, experiment_for_run
from csp import MyCSP
from sklearn.pipeline import Pipeline
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import (
    StratifiedShuffleSplit, cross_val_score, train_test_split
)
from joblib import dump, load

warnings.filterwarnings("ignore")
MODEL_PATH_TEMPLATE = "model_subject{subject}_exp{exp_id}.joblib"


def build_pipeline():
    """
    Dimensionality reduction (CSP) -> classification (shrinkage LDA).

    shrinkage='auto' + solver='lsqr' uses the Ledoit-Wolf estimate for
    the within-class covariance, which matters a lot here: with only
    a handful of CSP features but few dozen trials, plain LDA's
    covariance estimate is noisy and shrinkage consistently helps.
    """
    return Pipeline([
        ("csp", MyCSP(n_components=6, reg=0.05)),
        ("lda", LinearDiscriminantAnalysis(solver="lsqr", shrinkage="auto"))
    ])


def full_report():
    """
    Train+predict every subject on every experiment, print mean accuracies.
    """
    subjects = [
        subject for subject in range(1, 110) if subject not in BAD_SUBJECTS
    ]

    exp_means = {}
    for exp_id in EXPERIMENTS:
        accs = []
        for subject in subjects:
            try:
                X, y = get_dataset(subject, exp_id)
                clf = build_pipeline()
                cv = StratifiedShuffleSplit(
                    n_splits=5, test_size=0.2, random_state=42
                )
                scores = cross_val_score(clf, X, y, cv=cv)
                acc = scores.mean()
            except Config.EXCEPTIONS as e:
                print(
                    f"experiment {exp_id}: subject {subject:03d}: "
                    f"skipped {e}"
                )

            accs.append(acc)
            print(
                f"experiment {exp_id}: subject {subject:03d}: "
                f"accuracy = {acc:.4f}"
            )
            exp_means[exp_id] = float(np.mean(accs)) if accs else float("nan")

    print()
    print(
        f"Mean accuracy of the six different experiment for all "
        f"{len(subjects)} subjects:"
    )
    for exp_id, mean_acc in exp_means.items():
        print(f"experiment {exp_id}: \t\taccuracy = {mean_acc:.4f}")

    overall = float(np.nanmean(list(exp_means.values())))
    print(f"\nMean accuracy of 6 experiments: {overall:.4f}")
    return overall


def train(subject, exp_id):
    X, y = get_dataset(subject, exp_id)

    clf = build_pipeline()
    # stratified so every fold keeps the same class balance as the
    # full dataset -- important with only ~20-40 trials per class
    cv = StratifiedShuffleSplit(n_splits=10, test_size=0.2, random_state=None)
    scores = cross_val_score(clf, X, y, cv=cv)

    print(np.round(scores, 4).tolist())
    print(f"cross_val_score: {scores.mean():.4f}")

    # fit on everything except a held-out chunk we keep for `predict`
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    clf.fit(X_train, y_train)
    path = MODEL_PATH_TEMPLATE.format(subject=subject, exp_id=exp_id)
    dump({"pipeline": clf, "X_test": X_test, "y_test": y_test}, path)
    return scores.mean()


def predict(subject, exp_id):
    path = MODEL_PATH_TEMPLATE.format(subject=subject, exp_id=exp_id)
    saved = load(path)

    clf = saved["pipeline"]
    X_test, y_test = saved["X_test"], saved["y_test"]

    print("epoch nb: [prediction] [truth] equal?")
    correct = 0
    for i, (chunk, truth) in enumerate(zip(X_test, y_test)):
        start = time.time()
        pred = clf.predict(chunk[np.newaxis, ...])[0]
        elapsed = time.time() - start
        is_correct = pred == truth
        correct += int(is_correct)
        print(
            f"epoch {i:02d}: [{pred}] [{truth}] {is_correct}  "
            f"({elapsed * 1000:.1f} ms)"
        )
    accuracy = correct / len(y_test)
    print(f"Accuracy: {accuracy:.4f}")
    return accuracy


def main():
    try:
        if len(sys.argv) == 1:
            full_report()
            return
        if len(sys.argv) != 4:
            print(__doc__)
            sys.exit(1)

        subject, run, mode = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
        print(f"subject {subject}, run {run}, mode '{mode}'")
        exp_id = experiment_for_run(run)

        if mode == "train":
            train(subject, exp_id)
        elif mode == "predict":
            predict(subject, exp_id)
        else:
            print(f"Unknown mode '{mode}'. Use 'train' or 'predict'.")
            sys.exit(1)
    except Config.EXCEPTIONS as e:
        return errorHandler(type(e), e)
    return 0


if __name__ == '__main__':
    sys.exit(main())
