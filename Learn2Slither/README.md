# Learn2Slither 🐍

> A snake that learns how to behave in an environment through trial and error.

**Project type:** Reinforcement Learning (Q-learning)
**Version:** 1.00

---

## Overview

Learn2Slither is an AI project where you implement a snake game controlled by a reinforcement learning agent. The agent learns to navigate a board, eat apples, avoid walls, and survive as long as possible — purely through trial and error across thousands of training sessions.

The core loop: the agent observes the snake's vision → picks an action → receives a reward from the environment → updates its Q-function → repeats.

---

## Objectives Checklist

### Part 1 — Environment / Board

- [ ] 10×10 grid board
- [ ] 2 green apples placed at random positions
- [ ] 1 red apple placed at a random position
- [ ] Snake starts with length 3, placed randomly and contiguously
- [ ] Game over if snake hits a wall
- [ ] Game over if snake collides with its own tail
- [ ] Game over if snake length drops to 0
- [ ] Eating a green apple: +1 length, new green apple spawns
- [ ] Eating a red apple: −1 length, new red apple spawns
- [ ] Multiple training sessions supported via command-line argument (`-sessions N`)
- [ ] Graphical display of the board updated each step
- [ ] Configurable display speed (at least one human-readable speed)
- [ ] Step-by-step mode available

### Part 2 — State (Snake Vision)

- [ ] Snake can only see in 4 directions from its head (UP, DOWN, LEFT, RIGHT)
- [ ] Vision output is printed to terminal before each agent decision
- [ ] Vision uses the following symbols:
  - `W` = Wall
  - `H` = Snake Head
  - `S` = Snake body segment
  - `G` = Green apple
  - `R` = Red apple
  - `0` = Empty space
- [ ] **Only** vision-based information is passed to the agent (no global board state)

> ⚠️ Providing more information than the snake can see results in a **−42 penalty**.

### Part 3 — Action

- [ ] Agent supports exactly 4 actions: `UP`, `LEFT`, `DOWN`, `RIGHT`
- [ ] Action is chosen solely from the snake's vision (State)
- [ ] Chosen action is printed to the terminal alongside the current state

### Part 4 — Rewards

- [ ] Define a reward for eating a green apple (positive)
- [ ] Define a reward for eating a red apple (negative)
- [ ] Define a reward for a step with no apple eaten (small negative)
- [ ] Define a reward for game over / death (large negative)
- [ ] Rewards influence future action probabilities for the same state

### Part 5 — Q-Learning

- [ ] Implement a Q-function using either a **Q-table** or a **Neural Network**
- [ ] Q-values update after each action based on received reward
- [ ] Exploration vs. exploitation strategy implemented (e.g. ε-greedy)
- [ ] Iterative learning across multiple training sessions
- [ ] **Export** current model state to a file at any time
- [ ] **Import** a saved model to restore a learning state
- [ ] `--dontlearn` flag: runs the agent without updating the Q-function (evaluation mode)
- [ ] Training can run without graphical display or terminal output (for speed)

> ⚠️ Only Q-table or Neural Network models are allowed. Any other model results in a **score of 0**.

### Part 6 — Technical Structure

- [ ] Code is modular with clearly separated components:
  - **Environment** — board logic, apple placement, collision detection
  - **Interpreter** — translates board state into snake vision
  - **Agent** — Q-function, action selection, learning
- [ ] Modules communicate cleanly with well-defined interfaces

---

## Deliverables

### Models (required in `models/` folder)

| File | Training sessions | Notes |
|------|-------------------|-------|
| `1sess.txt` | 1 | Baseline — nearly untrained |
| `10sess.txt` | 10 | Early learning |
| `100sess.txt` | 100 | Intermediate |
| *(additional)* | 1000+ | Strongly recommended for good performance |

Each model file must be loadable and runnable in `--dontlearn` mode during evaluation.

### Command-Line Interface

```bash
# Train and save a model (no display)
./snake -sessions 10 -save models/10sess.txt -visual off

# Evaluate a saved model (no learning, visual, step-by-step)
./snake -visual on -load models/100sess.txt -sessions 10 -dontlearn -step-by-step

# Run a well-trained model with display
./snake -visual on -load models/1000sess.txt
```

---

## Goal

- Snake must reach **length ≥ 10** by the end of a session
- Snake must survive as long as possible
- Models must show clear improvement as training sessions increase

---

## Bonus Objectives

*Only evaluated if all mandatory parts are complete.*

- [ ] Snake reaches length 15 / 20 / 25 / 30 / 35
- [ ] Visually enhanced display (lobby, config panel, stats/results screen)
- [ ] Board size configurable via argument (model must generalize across board sizes)

---

## Tech Notes

- Language: **Python** recommended (many useful libraries available)
- Python code must comply with **flake8** (`pip install flake8`)
- Submit via Git — only what's in the repo is graded
- Program must not crash unexpectedly (undefined behavior = score 0)
- Train models **in advance** — training thousands of sessions takes significant time

---

## Project Structure (suggested)

```
learn2slither/
├── snake.py            # Entry point / CLI
├── environment.py      # Board, apples, collision logic
├── interpreter.py      # Snake vision / state encoding
├── agent.py            # Q-learning agent
├── models/
│   ├── 1sess.txt
│   ├── 10sess.txt
│   └── 100sess.txt
└── README.md
```