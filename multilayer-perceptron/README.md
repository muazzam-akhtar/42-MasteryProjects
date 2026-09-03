# Multilayer Perceptron — Breast Cancer Classifier

A from-scratch (numpy only) implementation of a multilayer perceptron trained
with backpropagation and mini-batch gradient descent, to classify tumors as
malignant (M) or benign (B).

## Files

| File          | Role                                                                |
|---------------|----------------------------------------------------------------------|
| `config.py`   | Terminal colour helpers (unchanged from original)                   |
| `data.py`     | CSV loading, feature/label extraction, standardization               |
| `layers.py`   | Activations (sigmoid, relu, tanh, softmax) + `DenseLayer` class      |
| `network.py`  | `Network` container: forward/backward pass, weight updates, save/load|
| `losses.py`   | Categorical cross-entropy, binary cross-entropy (subject's formula), accuracy |
| `split.py`    | **Program 1** — splits the raw dataset into train/val CSVs           |
| `train.py`    | **Program 2** — trains the network (backprop + gradient descent)     |
| `predict.py`  | **Program 3** — loads a saved model and evaluates it                 |

Expects the raw CSV with **no header row**: `id, diagnosis(M/B), 30 numeric features`
(32 columns total), matching the Wisconsin breast cancer dataset described in the subject.

## Usage

### 1. Split the dataset
```bash
python split.py --input data.csv --train ./out --valid_size 0.2 --seed 42
```
Writes `out/train.csv` and `out/val.csv`.

### 2. Train
```bash
python train.py --train out/train.csv --valid out/val.csv \
    --layer 24 24 --epochs 84 --loss categoricalCrossentropy \
    --batch_size 8 --learning_rate 0.0314 --output saved_model.pkl
```
- `--layer` sets the hidden layer sizes (at least 2 by default, per the subject).
- `--activation {sigmoid,relu,tanh}` for hidden layers; output layer is always
  softmax over 2 classes (benign/malignant), as required.
- `--weights_initializer {heUniform,heNormal,xavier}`
- `--early_stopping --patience 10` enables the bonus early-stopping feature.
- Prints per-epoch `loss` / `val_loss` / `acc` / `val_acc`, saves the trained
  model (topology + weights + normalization stats) to `--output`, and writes
  a loss/accuracy learning-curve figure to `--plot` (default `learning_curves.png`).

### 3. Predict / evaluate
```bash
python predict.py --dataset out/val.csv --model saved_model.pkl
```
Prints the binary cross-entropy error (exact formula from the subject, section IV.4)
and accuracy on the given set, plus a few sample predictions.

## Implementation notes

- **Feedforward**: each `DenseLayer.forward` computes `Z = A_prev @ W + b`
  then `A = activation(Z)`.
- **Backpropagation**: output layer uses softmax + categorical cross-entropy,
  whose combined gradient simplifies to `dZ = A - Y`; every earlier layer then
  applies the ordinary chain rule with its own activation's derivative.
- **Gradient descent**: mini-batch, shuffled every epoch, `W -= lr * dW`.
- **Preprocessing**: mean/std are computed on the **training set only** and
  the same statistics are reused for validation/prediction (saved inside the
  model file) — never refit normalization on validation data.
- No machine-learning libraries are used anywhere in the algorithm itself;
  only numpy (linear algebra), pandas (CSV I/O) and matplotlib (plotting),
  which the subject explicitly allows.

## Sources

1. [Concept](https://hediyetapan.medium.com/understanding-the-mathematics-behind-multilayer-perceptrons-mlps-0de46159fe5a)
2. [G4G](https://www.geeksforgeeks.org/deep-learning/multi-layer-perceptron-learning-in-tensorflow/)