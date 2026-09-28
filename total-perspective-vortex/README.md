# Total Perspective Vortex — starter implementation

A brain-computer interface that classifies motor-imagery EEG signals
(PhysioNet dataset) using a custom CSP (Common Spatial Patterns)
dimensionality-reduction step feeding into a scikit-learn classifier.

## Files

- `csp.py` — custom `MyCSP` transformer (`BaseEstimator` + `TransformerMixin`),
  implements the CSP algorithm from scratch using `scipy.linalg.eigh`.
- `data_utils.py` — downloads/loads PhysioNet EEG data via MNE, band-pass
  filters it, epochs it into labeled trials. Defines the 6 "experiments"
  (pairs/groups of raw runs) required by the subject.
- `mybci.py` — CLI entry point: train, predict, or full report across all
  subjects/experiments.

## Setup

```bash
pip install mne scikit-learn scipy numpy joblib
```

The first run of any command will trigger MNE to download the requested
subject's EDF files from PhysioNet (needs internet access; files are cached
locally by MNE after the first download).

## Usage

Train on one subject/run (run number picks the experiment group it
belongs to — see `EXPERIMENTS` in `data_utils.py`):

```bash
python mybci.py 4 14 train
```

Predict (simulated real-time playback) using the model just trained:

```bash
python mybci.py 4 14 predict
```

Full report — trains and evaluates every subject (1-109, minus a few
with known-corrupt PhysioNet annotations) across all 6 experiments, and
prints the mean accuracy table:

```bash
python mybci.py
```

## Design notes / what to check against the subject requirements

- **Preprocessing**: `data_utils.preprocess` applies a 7-30 Hz band-pass
  (mu + beta bands), the frequency range most informative for motor
  imagery. Add `raw.plot()` / `raw.plot_psd()` calls before/after
  filtering if you need the "visualize raw, then visualize filtered"
  deliverable explicitly.
- **Dimensionality reduction**: `MyCSP` is written from scratch (only
  `numpy`/`scipy` linear algebra primitives), matching the requirement
  to implement — not just call — the algorithm, and it plugs into
  `sklearn.pipeline.Pipeline` via `BaseEstimator`/`TransformerMixin`.
- **Classifier**: LDA is used for now — swap freely (SVM, etc.).
- **cross_val_score**: used on the *whole pipeline* in `train()`, not
  just the classifier, per the subject's requirement.
- **Real-time constraint**: `predict()` times every single-epoch
  prediction; on this pipeline it's on the order of milliseconds, well
  under the 2s ceiling.
- **60% accuracy requirement**: not guaranteed by this starter as-is —
  you'll likely need to tune `n_components` in `MyCSP`, the epoch
  window (`tmin`/`tmax` in `epoch_raw`), the filter band, and possibly
  the classifier to hit it reliably across all subjects/experiments.

## Bonus ideas (not implemented here)

- Replace the Fourier/band-pass preprocessing with a wavelet-transform
  based feature extraction.
- Implement your own classifier instead of `LinearDiscriminantAnalysis`.
- Implement your own eigenvalue/SVD or covariance-matrix estimator
  instead of relying on `scipy.linalg.eigh` / `np.cov` (hardest bonus,
  noted in the subject as difficult due to noisy, non-square data).
- Try the pipeline on a different EEG dataset.

## Sources:

- https://www.sciencedirect.com/topics/engineering/common-spatial-pattern