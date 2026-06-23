"""
agent.py - Learn2Slither Q-Learning Agent

Implements Q-learning with a Q-table to train the snake.

State encoding:
    The snake's vision is 4 directional rays. Each ray is compressed
    into the FIRST significant object seen in that direction:
        W = wall, S = snake body, G = green apple, R = red apple, 0 = empty

    This gives a state tuple of 4 symbols (up, down, left, right),
    one per direction — yielding 5^4 = 625 possible states.

Q-table:
    Keys   : state tuples  e.g. ('W', '0', 'S', 'G')
    Values : dict mapping action -> Q-value  e.g. {'UP': -1.2, 'DOWN': 0.4, ...
    }

Q-update rule (Bellman equation):
    Q(s, a) <- Q(s, a) + alpha * [r + gamma * max_a'(Q(s', a')) - Q(s, a)]
"""

import json
import random
import os

from environment import DIRECTIONS, UP, DOWN, LEFT, RIGHT

# ── Hyperparameters ──────────────────────────────────────────────────────────

ALPHA = 0.1             # Learning rate: how fast Q-values update
GAMMA = 0.9             # Discount factor: how much future rewards matter
EPSILON_START = 1.0     # Initial exploration rate (fully random)
EPSILON_MIN = 0.01      # Minimum exploration rate
EPSILON_DECAY = 0.995   # Multiplicative decay per episode

DEFAULT_Q = 0.0         # Initial Q-value for unseen state-action pairs


class QLearningAgent:
    """
    Tabular Q-learning agent for the snake game.

    Args:
        alpha        (float): Learning rate
        gamma        (float): Discount factor
        epsilon      (float): Starting exploration rate
        epsilon_min  (float): Minimum exploration rate
        epsilon_decay(float): Per-episode epsilon decay multiplier
        learning     (bool) : If False, disables Q-table updates (eval mode)
    """

    def __init__(
            self,
            alpha=ALPHA,
            gamma=GAMMA,
            epislon=EPSILON_START,
            epsilon_min=EPSILON_MIN,
            epsilon_decay=EPSILON_DECAY,
            learning=True,
            ):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epislon
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.learning = learning

        self.q_table = {}       # { state_key: { action: q_value } }
        self.episode = 0        # tracks how many episodes have been run

    # ── State encoding ───────────────────────────────────────────────────────

    def encode_state(self, vision):
        """
        Convert raw vision dict into a compact hashable state tuple.

        For each of the 4 directions, extract the FIRST meaningful object
        seen (the closest non-empty cell), or 'W' if a wall is first.

        Args:
            vision (dict): {UP: [...], DOWN: [...], LEFT: [...], RIGHT: [...]}

        Returns:
            tuple of 4 strings: (up_symbol, down_symbol, left_symbol,
            right_symbol)
        """
        state = []
        for direction in [UP, DOWN, LEFT, RIGHT]:
            ray = vision.get(direction, ['W'])
            symbol = self._first_significant(ray)
            state.append(symbol)
        return tuple(state)

    def _first_significant(self, ray):
        """
        Return the first significant object seen in a vision ray.

        - 'W' as first cell  -> 'W' (snake is immediately against a wall)
        - 'S', 'G', 'R' before wall -> that symbol
        - only '0' before wall -> '0' (open corridor)
        """
        if not ray:
            return 'W'
        if ray[0] == 'W':
            return 'W'
        for symbol in ray:
            if symbol in ('S', 'G', 'R'):
                return symbol
            if symbol == 'W':
                return '0'
        return '0'

    # ── Q-table access ───────────────────────────────────────────────────────

    def _get_q_values(self, state_key):
        """Return Q-values for a state, initialising missing entries to 0."""
        if state_key not in self.q_table:
            self.q_table[state_key] = {a: DEFAULT_Q for a in DIRECTIONS}
        return self.q_table[state_key]

    def _get_q(self, state_key, action):
        return self._get_q_values(state_key)[action]

    def _set_q(self, state_key, action, value):
        self._get_q_values(state_key)[action] = value

    def _max_q(self, state_key):
        """Return the maximum Q-value across all actions for a state."""
        return max(self._get_q_values(state_key).values())

    def _best_action(self, state_key):
        """Return the action with the highest Q-value for a state."""
        q_vals = self._get_q_values(state_key)
        return max(q_vals, key=q_vals.get)

    # ── Action selection ─────────────────────────────────────────────────────

    def choose_action(self, vision):
        """
        ε-greedy action selection.

        With probability ε: explore (random action).
        With probability 1-ε: exploit (best known action).

        Args:
            vision (dict): raw vision from environment

        Returns:
            action (str): one of UP, DOWN, LEFT, RIGHT
        """
        state_key = self.encode_state(vision)

        if self.learning and random.random() < self.epsilon:
            return random.choice(DIRECTIONS)

        return self._best_action(state_key)

    # ── Learning update ──────────────────────────────────────────────────────

    def update(self, vision, action, reward, next_vision, done):
        """
        Apply the Bellman Q-update after one environment step.

        Q(s,a) ← Q(s,a) + α * [r + γ * max_a' Q(s',a') - Q(s,a)]

        If done, the future value is 0 (no next state).

        Args:
            vision      (dict): state before action
            action      (str) : action taken
            reward      (float): reward received
            next_vision (dict): state after action
            done        (bool): whether the episode ended
        """
        if not self.learning:
            return

        state_key = self.encode_state(vision)
        next_key = self.encode_state(next_vision)

        current_q = self._get_q(state_key, action)
        future_q = 0.0 if done else self._max_q(next_key)

        new_q = current_q + self.alpha * (
            reward + self.gamma * future_q - current_q
            )
        self._set_q(state_key, action, new_q)

    def end_episode(self):
        """
        Called at the end of each training episode.
        Decays epsilon for exploration-exploitation shift.
        """
        self.episode += 1
        if self.learning:
            self.epsilon = max(
                self.epsilon_min, self.epsilon * self.epsilon_decay
                )

    # ── Model persistence ────────────────────────────────────────────────────

    def save(self, filepath):
        """
        Export the full learning state to a JSON file.

        Saved fields:
            - q_table   : all learned Q-values
            - epsilon   : current exploration rate
            - episode   : number of episodes trained
            - alpha     : learning rate
            - gamma     : discount factor
        """
        os.makedirs(
            os.path.dirname(filepath) if os.path.dirname(filepath) else '.',
            exist_ok=True)

        # Convert tuple keys to strings for json serialisation
        serialisable = {
            str(k): v for k, v in self.q_table.items()
        }

        data = {
            'q_table': serialisable,
            'epsilon': self.epsilon,
            'episode': self.episode,
            'alpha': self.alpha,
            'gamma': self.gamma,
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"[Agent] Saved model ({len(self.q_table)} states) → {filepath}")

    def load(self, filepath):
        """
        Import a learning state from a JSON file.

        Args:
            filepath (str): path to the model file
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")

        with open(filepath, 'r') as f:
            data = json.load(f)

        # Re-parse string keys back into tuples
        self.q_table = {}
        for k, v in data['q_table'].items():
            # k looks like "('W', '0', 'S', 'G')"
            key = tuple(
                k.strip("()").replace("'", "").replace(" ", "").split(",")
                )
            self.q_table[key] = v

        self.epsilon = data.get('epsilon', EPSILON_MIN)
        self.episode = data.get('episode', 0)
        self.alpha = data.get('alpha', ALPHA)
        self.gamma = data.get('gamma', GAMMA)

        print(
            f"[Agent] Loaded model ({len(self.q_table)} states, "
            f"episodes={self.episode}, ε={self.epsilon:.4f}) ← {filepath}"
        )

    # ── Diagnostics ──────────────────────────────────────────────────────────

    def stats(self):
        """Return a dict of current agent statistics."""
        return {
            'states_seen': len(self.q_table),
            'epsilon': round(self.epsilon, 4),
            'episode': self.episode,
            'learning': self.learning,
        }

    def print_q_table(self, top_n=10):
        """Print the top N most-visited / interesting Q-table entries."""
        if not self.q_table:
            print("[Agent] Q-table is empty.")
            return

        print(f"\n[Agent] Q-table ({len(self.q_table)} states). Top {top_n}:")
        print(f"{'State':<30} {'UP':>8} {'DOWN':>8} {'LEFT':>8} {'RIGHT':>8}")
        print("-" * 66)

        # Sort by max absolute Q-value (most learned states first)
        sorted_states = sorted(
            self.q_table.items(),
            key=lambda x: max(abs(v) for v in x[1].values()),
            reverse=True
        )

        for state_key, q_vals in sorted_states[:top_n]:
            best = max(q_vals, key=q_vals.get)
            row = f"{str(state_key):<30}"
            for a in DIRECTIONS:
                marker = "*" if a == best else " "
                row += f" {q_vals[a]:>7.2f} {marker}"
            print(row)
        print()
