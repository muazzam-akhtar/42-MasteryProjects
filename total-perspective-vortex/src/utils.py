"""
utils.py

Loading, filtering and epoching of the PhysioNet EEG Motor
Movement/Imagery dataset via MNE.

The PhysioNet dataset has 109 subjects, each with 14 runs:
    run 1  : baseline, eyes open
    run 2  : baseline, eyes closed
    runs 3, 7, 11  : motor EXECUTION,  left fist vs right fist
    runs 4, 8, 12  : motor IMAGERY,    left fist vs right fist
    runs 5, 9, 13  : motor EXECUTION,  both fists vs both feet
    runs 6, 10, 14 : motor IMAGERY,    both fists vs both feet

We group these into 6 "experiments" as required by the subject
("corresponding to the six types of experiment runs").
"""

from mne.datasets import eegbci
from mne.io import read_raw_edf, concatenate_raws
import mne

EXPERIMENTS = {
    0: ([3, 7, 11], "execution: left fist vs right fist"),
    1: ([4, 8, 12], "imagery: left fist vs right fist"),
    2: ([5, 9, 13], "execution: both fist vs both feet"),
    3: ([6, 10, 14], "imagery: both fist vs both feet"),
}


BAD_SUBJECTS = {88, 89, 92, 100, 104}


def load_raw(subject, runs):
    """
    Download(if needed) and concatenate the requested runs for a subject
    """
    filenames = eegbci.load_data(subject, runs, verbose=False)
    raws = [
        read_raw_edf(file, preload=True, verbose=False) for file in filenames
    ]
    raw = concatenate_raws(raws)
    eegbci.standardize(raw)
    raw.set_montage("standard_1005", on_missing="ignore")
    return raw


def preprocess(raw, l_freq=7.0, h_freq=30.0):
    """
    Band-pass filter to the mu/beta bands relevant to motor imagery.
    """
    raw = raw.copy()
    raw.filter(l_freq, h_freq, fir_design="firwin", skip_by_annotation="edge")
    return raw


def epoch_raw(raw, tmin=1.0, tmax=3.0):
    """
    Extract labeled epochs around each event annotation.

    Default window is 1s-3s *after* the cue, not centered on it: the
    first ~1s after a cue is dominated by the visual-evoked response
    to the cue itself, not the motor imagery signal, so including it
    dilutes the CSP features with irrelevant variance.

    Returns
    -------
    X : ndarray (n_epochs, n_channels, n_times)
    y : ndarray (n_epochs,)  integer labels (1 or 2)
    """
    events, event_id = mne.events_from_annotations(raw, verbose=False)
    # keep only the two "task" annotations (T1/T2), drop rest/baseline (T0)
    picks = mne.pick_types(raw.info, eeg=True, exclude="bads")
    wanted = {
        key: value for key, value in event_id.items() if key in ("T1", "T2")
    }
    if not wanted:
        raise RuntimeError("No T1/T2 annotations found in this run")

    epochs = mne.Epochs(
        raw, events, event_id=wanted, tmin=tmin, tmax=tmax,
        picks=picks, baseline=None, preload=True, verbose=False
    )
    X = epochs.get_data()
    y = epochs.events[:, -1]
    return X, y


def get_dataset(subject, experiment_id, l_freq=7.0, h_freq=30.0):
    """
    Full pipeline: load -> filter -> epoch for one subject/experiment.
    """
    runs, _ = EXPERIMENTS[experiment_id]
    raw = load_raw(subject, runs)
    raw = preprocess(raw, l_freq, h_freq)
    X, y = epoch_raw(raw)
    return X, y


def experiment_for_run(run):
    """
    Return the experiment id that contains a given raw run number.
    """
    for exp_id, (runs, _) in EXPERIMENTS.items():
        if run in runs:
            return exp_id
    raise ValueError(f"Run {run} does not belong to any known experiment")
