"""Loss functions and metrics, implemented from scratch (numpy only)."""

import numpy as np


EPS = 1e-15


def categorical_cross_entropy(Y_true, Y_pred):
    """Y_true, Y_pred: (m, num_classes) one_hot / probability matrices."""
    Y_pred = np.clip(Y_pred, EPS, 1 - EPS)
    return -np.mean(np.sum(Y_true * np.log(Y_pred), axis=1))


def binary_cross_entropy(y_true, p_pred):
    """
    The exact metric requested by the subject (IV.4):
        E = -(1/N) * sum( y*log(p) + (1-y)*log(1-p) )
    y_true: (m,) of 0/1 ; p_pred: (m,) probability of the positive class (M).
    """
    p_pred = np.clip(p_pred, EPS, 1 - EPS)
    return -np.mean(
        y_true * np.log(p_pred) + (1 - y_true) * np.log(1 - p_pred)
    )


def accuracy(Y_true, Y_pred):
    """
    Y_true, Y_pred: (m, num_classes) -> fraction of correctly
    predicted classes.
    """
    true_labels = np.argmax(Y_true, axis=1)
    pred_labels = np.argmax(Y_pred, axis=1)
    return float(np.mean(true_labels == pred_labels))


def confusion_counts(Y_true, Y_pred, positive_class=1):
    """
    Y_true, Y_pred: (m, num_classes) one-hot / probability matrices.
    positive_class: index of the "positive" class (1 = malignant,
    per one_hot()).
    Returns (tp, fp, tn, fn) as plain ints.
    """
    true_labels = np.argmax(Y_true, axis=1)
    pred_labels = np.argmax(Y_pred, axis=1)

    tp = int(np.sum((pred_labels == positive_class) & (
        true_labels == positive_class)))
    fp = int(np.sum((pred_labels == positive_class) & (
        true_labels != positive_class)))
    tn = int(np.sum((pred_labels != positive_class) & (
        true_labels != positive_class)))
    fn = int(np.sum((pred_labels != positive_class) & (
        true_labels == positive_class)))
    return tp, fp, tn, fn


def precision_score(Y_true, Y_pred, positive_class=1):
    """Of everything predicted positive (malignant), fraction
    that truly was."""
    tp, fp, _, _ = confusion_counts(Y_true, Y_pred, positive_class)
    denom = tp + fp
    return tp / denom if denom > 0 else 0.0


def recall_score(Y_true, Y_pred, positive_class=1):
    """Of everything truly positive (malignant), fraction correctly caught.
    Also called sensitivity. The clinically costly failure mode (missed
    cancers) shows up here, not in accuracy."""
    tp, _, _, fn = confusion_counts(Y_true, Y_pred, positive_class)
    denom = tp + fn
    return tp / denom if denom > 0 else 0.0


def f1_score(Y_true, Y_pred, positive_class=1):
    """Harmonic mean of precision and recall; balances both failure modes."""
    p = precision_score(Y_true, Y_pred, positive_class)
    r = recall_score(Y_true, Y_pred, positive_class)
    return 2 * p * r / (p + r) if (p + r) > 0 else 0.0


def compute_metrics(Y_true, Y_pred, positive_class=1):
    """Convenience bundle: every metric at once, for logging/history."""
    return {
        "accuracy": accuracy(Y_true, Y_pred),
        "precision": precision_score(Y_true, Y_pred, positive_class),
        "recall": recall_score(Y_true, Y_pred, positive_class),
        "f1": f1_score(Y_true, Y_pred, positive_class),
    }
