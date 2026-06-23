# 42-MasteryProjects

This repository contains a collection of projects developed as part of the **42 curriculum**, focusing on mathematics, data science, and machine learning fundamentals. Each project is designed to build strong problem‑solving skills and a deep understanding of core concepts through hands‑on implementation.

---

## 📌 Projects Overview

### 1. ft_linear_regression

A simple implementation of **linear regression** used to predict car prices based on mileage.

#### Features
- **Prediction Program**
  - Estimates car price using the formula:
    ```
    estimatePrice = theta0 + (theta1 × mileage)
    ```
- **Training Program**
  - Uses **gradient descent** to optimize `theta0` and `theta1` on a given dataset.

#### Bonus
- Data visualization (scatter plot + regression line)
- Model precision evaluation

📚 *This project serves as an introduction to machine learning concepts such as optimization, cost functions, and model evaluation.*

---

### 2. Python Piscine

An introduction to the **Python programming language**, covering fundamental to advanced programming concepts.

#### Modules
- **P00**: Variables, Packages, Algorithms  
- **P01**: Arrays  
- **P02**: Data Tables  
- **P03**: Object-Oriented Programming  
- **P04**: Data-Oriented Design  

🎯 *The goal is to develop clean, efficient, and Pythonic code while understanding core language principles.*

---

### 3. computorv1

A mathematical program that parses and solves **polynomial equations**.

#### Capabilities
- Solves polynomial equations of degree:
  - **0**
  - **1**
  - **2**
- For higher degrees:
  - Displays the **reduced form** of the polynomial

📐 *This project reinforces algebraic manipulation, parsing, and numerical problem solving.*

---

### 4. DSLR

A machine learning project implementing **multivariable logistic regression** from scratch.

#### Data Visualization
- Histogram of features with the highest homogeneity score
- Scatter plots of:
  - Feature 1 vs Feature 2 (grouped by houses)
- Pair plot of 4 selected features

#### Model Training
- **Batch Gradient Descent**
- **Mini-Batch Gradient Descent**
- **Stochastic Gradient Descent**

#### Statistical Summary
- Average
- Standard Deviation
- Variance
- Skewness
- Coefficient of Variation (COV)
- Percentiles
- Minimum & Maximum values

📊 *This project combines statistics, visualization, and optimization techniques to build an interpretable classification model.*

---

### 5. Learn2Slither

A reinforcement learning project implementing **Q-Learning** from scratch to train an autonomous snake agent.

#### Game Environment
- **10×10 grid** with snake, green apples (+1), and red apples (-1)
- Multi-reward system:
  - Green apple: `+10`
  - Red apple: `-5`
  - Survival penalty: `-0.1` per step
  - Death penalty: `-20`
- Random initialization with configurable board size

#### Vision System (State Encoding)
- **4 directional rays** (up, down, left, right) from snake's head
- Symbol encoding: `W` (wall), `S` (body), `G` (green apple), `R` (red apple), `0` (empty)
- Efficient state space: **5⁴ = 625 possible states**

#### Q-Learning Agent
- **Algorithm**: Tabular Q-Learning with Bellman equation
  ```
  Q(s,a) ← Q(s,a) + α[r + γ × max(Q(s',a')) - Q(s,a)]
  ```
- **Hyperparameters**: α=0.1 (learning rate), γ=0.9 (discount factor)
- **Exploration**: ε-greedy with decay from 1.0 to 0.01

#### Features
- **Training Modes**: Batch training, continuous learning from saved models
- **Evaluation Mode**: Test models without updating Q-table (`-dontlearn`)
- **Step-by-Step Analysis**: Pause between steps for detailed study
- **Visual Interface**: Pygame-based GUI with:
  - Live game view with colored snake and apples
  - Sidebar dashboard (length, score, epsilon, Q-table size)
  - Mini chart showing training progress
  - Results screen with performance graphs
- **Model Persistence**: Full JSON save/load of Q-table + hyperparameters
- **Terminal Mode**: ASCII visualization and real-time logs

#### Command-Line Interface
```bash
# Training
python snake.py -sessions 100 -speed fast -save model.json

# Evaluation
python snake.py -load model.json -dontlearn -visual on

# Analysis Mode
python snake.py -load model.json -step-by-step -visual on

# Model Inspection
python snake.py -load model.json -stats
```

#### Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                       SNAKE.PY                             │
│                   (Orchestrator)                           │
├───────────────┬────────────────┬───────────────┬───────────┤
│  Environment  │  Interpreter   │    Agent      │  Display  │
│  (Game Logic) │ (Vision System)│ (Q-Learning)  │  (GUI)    │
└───────────────┴────────────────┴───────────────┴───────────┘
```

🎮 *This project combines reinforcement learning theory, state space optimization, interactive visualization, and practical ML engineering to build an intelligent agent that learns entirely through trial and error.*

---

## 🛠 Technologies & Concepts
- Python
- Linear & Logistic Regression
- Gradient Descent Optimization
- Reinforcement Learning (Q-Learning)
- Data Visualization
- Statistics & Probability
- Object-Oriented Design
- Mathematical Modeling
- State Space Optimization

---

## 🚀 Purpose

These projects aim to:
- Strengthen mathematical and algorithmic thinking
- Build machine learning models **from scratch**
- Understand the inner workings of popular ML algorithms
- Develop clean, maintainable, and efficient code

---

## 📂 Repository Structure
Each project is self-contained and includes:
- Source code
- Dataset(s) (if applicable)
- Documentation or usage instructions

---

## ✅ Status
Projects are complete and functional, with optional enhancements included where applicable.

---

Feel free to explore, test, and learn!