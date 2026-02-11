```
# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    DSLR                                               :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: hawadh <hawadh@student.42Abudhabi.ae>      +#+  +:+       +#+         #
#        makhtar <makhtar@student.42Abudhabi.ae>  +#+#+#+#+#+   +#+            #
#    Created: 2025/10/10 21:33:37 by hawadh            #+#    #+#              #
#    Updated: 2025/10/15 21:33:37 by hawadh           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
```

# 🧙‍♂️ **Data Science × Logistic Regression**  
## **Harry Potter and the Data Scientist**

Rebuilding the Sorting Hat using pure data science and a logistic regression model implemented from scratch.

---

## 📖 **Project Overview**

Hogwarts is in crisis: the Sorting Hat has been bewitched and can no longer assign students to their houses. Professor McGonagall turns to a muggle data scientist — you — to recreate the Sorting Hat using computational magic.

This project walks through the full pipeline of building a multi‑class classifier **without using any high‑level statistical shortcuts**. You will analyze the data, visualize it, implement logistic regression manually, and ultimately predict each student’s Hogwarts house.

---

## 🎯 **Objectives**

- Explore and analyze a dataset without using built‑in statistical functions.
- Visualize data to understand distributions and relationships.
- Implement logistic regression (one‑vs‑all) from scratch.
- Train a classifier using gradient descent.
- Predict Hogwarts houses for unseen students.
- Achieve at least **98% accuracy** on the test dataset.

---

## 📂 **Project Structure**

```
.
├── describe.py
├── datasets
├   ├── dataset_train.csv
├   ├── dataset_test.csv
├   └── houses.csv
├── DataVisualization
├   ├── histogram.pyhistogram.py
├   ├── scatter_plot.py
├   └── pair_plot.py
├── logreg_train.py
└── logreg_predict.py
```

---

## 🔍 **1. Data Analysis — `describe`**

A custom implementation of a statistical summary tool.

The script computes, for each numerical feature:

- Count  
- Mean  
- Standard deviation  
- Min  
- 25% percentile  
- 50% percentile (median)  
- 75% percentile  
- Max  
- Skewness
- COV (Coefficient of Variation)
- Variance

All calculations are implemented manually — no `pandas.describe()`, no `numpy.mean()`, no shortcuts.

---

## 📊 **2. Data Visualization**

Visualization helps uncover patterns and select features for the model.

### **Histogram — `histogram.py`**
<img width="420" height="222" alt="Histogram" src="https://github.com/user-attachments/assets/2738c38c-1bab-44b5-a9c5-f3d0b0a68c06" />

**Which Hogwarts course has the most homogeneous score distribution across all four houses?**

### **Scatter Plot — `scatter_plot.py`**
<img width="400" height="400" alt="Scatter Plot" src="https://github.com/user-attachments/assets/63b1e702-701a-4583-8a27-f3f140bc7a5e" />

**Which two features appear most similar?**

### **Pair Plot — `pair_plot.py`**
<img width="420" height="222" alt="Pair Plot" src="https://github.com/user-attachments/assets/0c7883e4-3895-42d9-b0e5-8ebf806d03e3" />

**Displays a scatter‑plot matrix to identify relationships and guide feature selection for logistic regression.**

---

## 🧮 **3. Logistic Regression (One‑vs‑All)**

### **Training — `logreg_train.py`**
Implements:

- Sigmoid function  
- Cost function  
- Gradient computation  
- Gradient descent optimization  
- One‑vs‑all strategy for multi‑class classification  

Outputs a weights file used for prediction.

### **Prediction — `logreg_predict.py`**
Uses the trained weights to classify each student into:

- Gryffindor  
- Hufflepuff  
- Ravenclaw  
- Slytherin  

Produces a `houses.csv` file formatted as:

```
Index,Hogwarts House
0,Gryffindor
1,Hufflepuff
2,Ravenclaw
...
```

---

## 🧪 **Evaluation**

Your model is evaluated on the test dataset using **accuracy score**.  
To be considered a worthy replacement for the Sorting Hat, the classifier must achieve:

### ⭐ **≥ 98% accuracy**

---

## How to run

Execute the shell script `setup.sh` to run the venv.

First time run:

-   Run `logreg_train.py` to run the training model and select the model type:

    1.  Batch (Standard)
    2.  Stocastic Gradient Descent (SGD)
    3.  Mini-Batch Gradient Descent (MBGD)

-   Next run the prediction model `logreg_predict.py`:

    -   This will output a prediction file houses.csv in **/data**

-   Run the accuracy program to check accuracy `accuracy.py` of prediction:
    -   Input the path to the truth file **(must be present in /datasets)**

## Logistic Regression:

Logistic regression estimates the probability that a sample x belongs
to a class y = 1 using the sigmoid (logistic) function:

    h_θ(x) = 1 / (1 + e^(−θᵀx))

    and minimizes the cost function:

    J(θ) = −[y·log(h_θ(x)) + (1 − y)·log(1 − h_θ(x))]

## One-vs-Rest (OvR) Classification (Multi-Classifier):

For multi-class problems (e.g., 4 Hogwarts houses), one binary model is
trained per class:

-   Gryffindor vs. All,
-   Hufflepuff vs. All,
-   Ravenclaw vs. All,
-   Slytherin vs. All.

Each classifier predicts the probability that a sample belongs to its
respective class.

## Stochastic Gradient Descent (SGD):

SGD updates θ using one training sample at a time:

    θ := θ − α·(h_θ(xᵢ) − yᵢ)·xᵢ

    Where α is the learning rate.

Each epoch shuffles the dataset and iteratively improves θₖ for each
class model. SGD introduces noise in updates but converges faster on
large datasets.

### OvR + SGD Combined:

        For each class k:
            1. Create binary labels yₖ = (y == k)
            2. Initialize θₖ = 0
            3. For each epoch:
                a. Shuffle samples
                b. For each sample (xᵢ, yₖᵢ):
                     h = sigmoid(θₖᵀxᵢ)
                     θₖ := θₖ − α·(h − yₖᵢ)·xᵢ
            4. Store θₖ in allTheta[k]

### Why Use SGD?

Pros:

-   Works faster on large datasets.
-   Can escape local minima due to noisy updates.
-   Starts improving accuracy after few samples
    (no need to see all data first).

Cons:

-   The updates are noisy, causing the loss to fluctuate.
-   Requires smaller learning rates and potentially more epochs.
-   Convergence is not as smooth.

## Batch Gradient Descent (reference):

MBGD splits the dataset into small random batches of size `batchSize`.
It updates model parameters based on small, randomly selected subsets
(mini-batches) of the training dataset. Each mini-batch typically
contains between 16 to 512 samples, depending on dataset size and
hardware capabilities.

It is a hybrid between:

-   Batch Gradient Descent
-   Stochastic Gradient Descent

          For each batch:
              θ := θ − α·(1/b)·Σᵢ (h_θ(xᵢ) − yᵢ)·xᵢ
          where:
              α — learning rate
              b — number of samples in the batch

This combines the efficiency of vectorized batch updates with the
faster convergence and noise robustness of SGD.

The gradient of the loss function with respect to parameter θⱼ is:

    ∂J(θ)/∂θⱼ = (1/m) Σᵢ (h_θ(xᵢ) − yᵢ)·xᵢⱼ

Standard gradient descent updates θ after computing this gradient on the
entire dataset.

### OvR + MBGD Combined:

        For each class k:
            1. Create binary labels yₖ = (y == k)
            2. Initialize θₖ = 0
            3. For each epoch:
                a. Shuffle dataset indices
                b. Split data into batches of size `batchSize`
                c. For each batch (X_batch, y_batch):
                     h = sigmoid(X_batch @ θₖ)
                     grad = (1/b) * (X_batchᵀ @ (h − y_batch))
                     θₖ := θₖ − α·grad
            4. Store θₖ in allTheta[k]

### Why use MBGD

Pros:

-   Faster convergence than Batch Gradient Descent because updates
    occur multiple times per epoch rather than once.
-   More stable than Stochastic Gradient Descent because each
    gradient update is averaged over a batch, reducing variance.
-   Supports vectorized computation and GPU acceleration efficiently.
-   Introduces controlled randomness, which can help escape local minima.
-   Requires less memory than full-batch training.

Cons:

-   Slightly more complex to implement due to batching logic.
-   Choosing the right batch size can impact performance:
    too small → noisy updates; too large → slower learning.
-   Still not as accurate as full-batch training when the dataset
    is extremely small.

MBGD is generally the preferred method for training most modern
machine learning models, balancing efficiency, stability, and
generalization.

---

## 🧩 **Bonus Ideas**

These are optional and only evaluated if the mandatory part is perfect:

- Add more statistical fields to `describe`
- Implement stochastic gradient descent
- Implement mini‑batch or batch gradient descent
- Add regularization
- Build a full ML toolkit

---

## 🚀 **How to Run**

### **1. Describe the dataset**
```
python describe.py dataset_train.csv
```

### **2. Generate visualizations**
```
python3 histogram.py dataset_train.csv
python3 scatter_plot.py dataset_train.csv Astronomy Herbology 
python3 pair_plot.py dataset_train.csv Astronomy Herbology Arithmancy Divination
```

### **3. Train the model**
```
python logreg_train.py dataset_train.csv
```

### **4. Predict houses**
```
python logreg_predict.py dataset_test.csv weights.csv
```

---

## 🏰 **Conclusion**

This project blends storytelling with rigorous machine learning fundamentals.  
By rebuilding the Sorting Hat from scratch, you gain hands‑on experience with:

- Data exploration  
- Visualization  
- Mathematical modeling  
- Optimization  
- Multi‑class classification  

A perfect mix of magic and machine learning.

---
