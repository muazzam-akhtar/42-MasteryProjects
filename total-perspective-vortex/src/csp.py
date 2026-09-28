"""
csp.py

Custom implementation of the Common Spatial Patterns (CSP) algorithm,
used here as the dimensionality-reduction step of the pipeline
(as required by the "Total Perspective Vortex" subject).

CSP finds a set of spatial filters W such that the variance of the
projected signal is maximal for one class and minimal for the other.
This makes it particularly well suited to EEG motor-imagery data,
where the discriminative information lives in *band power* differences
between channels, not in the raw waveform shape.

Math (binary case):
    Given two classes, compute the average (normalized) spatial
    covariance matrix per class: C1, C2.
    Solve the generalized eigenvalue problem:
        C1 * w = lambda * (C1 + C2) * w
    The eigenvectors with eigenvalues close to 1 maximize variance for
    class 1 (and minimize it for class 2); eigenvectors with eigenvalues
    close to 0 do the opposite. We keep the n_components/2 filters from
    each extreme.

Only numpy/scipy linear-algebra primitives are used (eigh), as allowed
explicitly by the subject ("Numpy or scipy functions to find eigenvalues,
singular values, and covariance matrix estimation" are allowed).
"""

from sklearn.base import BaseEstimator, TransformerMixin
from scipy.linalg import eigh
import numpy as np


class MyCSP(BaseEstimator, TransformerMixin):
    """
    Common Spatial Patterns, sklearn-compatible transformer.

    Parameters
    ----------
    n_components : int
        Number of spatial filters to keep (must be even; split evenly
        between the two extremes of the eigenvalue spectrum).
    reg : float, default 0.05
        Shrinkage regularization strength (0 = none, 1 = fully diagonal).
        With ~64 channels and only a few dozen trials per class, raw
        covariance estimates are noisy/ill-conditioned; shrinking them
        toward a scaled identity matrix stabilizes the eigen-decomposition
        and tends to noticeably improve held-out accuracy.
    """

    def __init__(self, n_components=6, reg=0.05, eig_method="scipy"):
        self.n_components = n_components
        self.reg = reg
        self.eig_method = eig_method

    # ---- internal helpers -------------------------------------------------

    def _epoch_cov(self, epoch):
        """
        Regularized, normalized spatial covariance of a single epoch.

        epoch: array (n_channels, n_times)
        """
        cov = np.cov(epoch)
        # normalize by trace so that epochs of different energy
        # contribute comparably to the class-averaged covariance
        trace = np.trace(cov)
        if trace == 0:
            trace = 1e-12
        cov /= trace
        # shrinkage: blend toward (trace/n_channels) * I
        n_ch = cov.shape[0]
        target = np.eye(n_ch) * (np.trace(cov) / n_ch)
        cov = (1 - self.reg) * cov + self.reg * target
        return cov

    def _class_covariance(self, X):
        """
        Average normalized covariance across all epochs of one class.

        X: array (n_epochs, n_channels, n_times)
        """
        covs = np.array([self._epoch_cov(epoch) for epoch in X])
        return covs.mean(axis=0)

    # ---- sklearn API --------------------------------------------------

    def fit(self, X, y):
        """
        Learn the spatial filters.

        X: array (n_epochs, n_channels, n_times)
        y: array (n_epochs,) with exactly 2 distinct labels
        """
        X = np.asarray(X)
        y = np.asarray(y)
        classes = np.unique(y)
        if classes.shape[0] != 2:
            raise ValueError(
                f"MyCSP only supports binary classfication, got "
                f"{classes.shape[0]} classes: {classes}"
            )

        cov1 = self._class_covariance(X[y == classes[0]])
        cov2 = self._class_covariance(X[y == classes[1]])

        # Generalized eigenvalue problem: cov1 w = lambda (cov1 + cov2) w
        if self.eig_method == "scipy":
            eigvals, eigvecs = eigh(cov1, cov1 + cov2)
        else:
            raise ValueError(
                f"Unknown eig_method '{self.eig_method}', "
                f"use 'scipy'"
            )
        # eigvals are sorted ascending by eigh. Filters near eigval=1
        # explain class1 variance best, filters near eigval=0 explain
        # class2 variance best -> take from both ends of the spectrum.
        n_pairs = self.n_components // 2
        idx = np.concatenate([
            np.arange(len(eigvals))[:n_pairs],  # near 0 -> class2
            np.arange(len(eigvals))[-n_pairs:][::-1],  # near 1 -> class1
        ])

        self.filters_ = eigvecs[:, idx].T   # shape(n_components, n_channels)
        self.classes_ = classes
        return self

    def transform(self, X):
        """
        Project epochs and return log-variance features.

        X: array (n_epochs, n_channels, n_times)
        returns: array (n_epochs, n_components)
        """
        X = np.asarray(X)
        # W^T X for every epoch -> (n_epochs, n_components, n_times)
        X_csp = np.array([self.filters_ @ epoch for epoch in X])
        variances = np.var(X_csp, axis=2)
        # log-variance is the standard CSP feature: makes the
        # distribution closer to Gaussian, helping linear classifiers
        variances = np.clip(variances, 1e-12, None)
        return np.log(variances)
