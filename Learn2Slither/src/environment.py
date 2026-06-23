"""
environment.py - Learn2Slither Board/Environment Module

Handles the 10x10 grid, snake placement, apple placement,
movement, collisions, and reward signals.

Vision/state is handled by interpreter.py.
"""

import random


BOARD_SIZE = 10

# Cell Types
EMPTY = 0
SNAKE_HEAD = 1
SNAKE_BODY = 2
GREEN_APPLE = 3
RED_APPLE = 4
WALL = 5

# Directions
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

DELTA = {
    UP: (-1, 0),
    DOWN: (1, 0),
    LEFT: (0, -1),
    RIGHT: (0, 1),
}

# Reward values
REWARD_GREEN_APPLE = 10.0
REWARD_RED_APPLE = -5.0
REWARD_STEP = -0.1
REWARD_DEATH = -20.0


class Environment:
    """
    Manages the snake game board state.

    Board uses (row, col) indexing where (0,0) is top-left.
    """

    def __init__(self, board_size=BOARD_SIZE):
        self.board_size = board_size
        self.reset()

    def reset(self):
        """Reset the board to a fresh game state."""
        self.snake = []             # list of (row, col), head is index 0
        self.green_apples = []      # list of (row, col)
        self.red_apple = None       # (row, col)
        self.done = False
        self.steps = 0
        self.score = 0              # apples eaten net (green - red)
        self.max_length = 3

        self._place_snake()
        self._place_green_apple()
        self._place_green_apple()
        self._place_red_apple()

        return None  # call interpreter.get_state(env) for vision

    # ------------------------------------------------------------------
    # Placement helpers
    # ------------------------------------------------------------------

    def _occupied_cells(self):
        """Return a set of all currently occupied cells."""
        cells = set(self.snake)
        cells.update(self.green_apples)
        if self.red_apple:
            cells.add(self.red_apple)
        return cells

    def _random_empty_cell(self):
        """Return a random cell not occupied by anything."""
        occupied = self._occupied_cells()
        empty = [
            (r, c)
            for r in range(self.board_size)
            for c in range(self.board_size)
            if (r, c) not in occupied
        ]
        if not empty:
            return None
        return random.choice(empty)

    def _place_snake(self):
        """Place the snake (length 3) randomly and contiguously."""
        placed = False
        while not placed:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
            direction = random.choice(DIRECTIONS)
            dr, dc = DELTA[direction]

            # Build body going OPPOSITE of head direction
            body = [(row, col)]
            valid = True
            for i in range(1, 3):
                nr = row - dr * i
                nc = col - dc * i
                if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                    body.append((nr, nc))
                else:
                    valid = False
                    break

            if valid and len(body) == 3:
                self.snake = body
                placed = True

    def _place_green_apple(self):
        """Place a new green apple on a random empty cell."""
        cell = self._random_empty_cell()
        if cell:
            self.green_apples.append(cell)

    def _place_red_apple(self):
        """Place a new red apple on a random empty cell."""
        cell = self._random_empty_cell()
        if cell:
            self.red_apple = cell

    # ------------------------------------------------------------------
    # Step logic
    # ------------------------------------------------------------------

    def step(self, action):
        """
        Apply an action and advance the game by one step.

        Args:
            action (str): One of UP, DOWN, LEFT, RIGHT

        Returns:
            reward  (float)
            done    (bool)
            info    (dict): extra diagnostic info
        """
        if self.done:
            raise RuntimeError(
                "Game is over. Call reset() to start a new session.")

        if action not in DELTA:
            raise ValueError(
                f"Invalid action: {action}. Must be one of {DIRECTIONS}.")

        self.steps += 1
        dr, dc = DELTA[action]
        head_r, head_c = self.snake[0]
        new_head = (head_r + dr, head_c + dc)

        # --- Check wall collision ---
        if not (0 <= new_head[0] < self.board_size and
                0 <= new_head[1] < self.board_size):
            self.done = True
            reward = REWARD_DEATH
            info = {'cause': 'wall', 'length': len(self.snake),
                    'steps': self.steps}
            return None, reward, self.done, info

        # --- Check self collision (ignore tail since it will move) ---
        if new_head in self.snake[:-1]:
            self.done = True
            reward = REWARD_DEATH
            info = {'cause': 'self', 'length': len(self.snake),
                    'steps': self.steps}
            return None, reward, self.done, info

        # Move snake: add new head
        self.snake.insert(0, new_head)

        # --- Check apple collisions ---
        reward = REWARD_STEP
        info = {'cause': 'step', 'length': len(self.snake),
                'steps': self.steps}

        if new_head in self.green_apples:
            # Eat green apple: grow (don't remove tail)
            self.green_apples.remove(new_head)
            self._place_green_apple()
            reward = REWARD_GREEN_APPLE
            self.score += 1
            info['cause'] = 'green_apple'

        elif new_head == self.red_apple:
            # Eat red apple: net length decreases by 1.
            # Normal move already added head;
            # do NOT remove tail (snake grew by 1),
            # then remove tail once to cancel growth,
            # and remove tail again to shrink.
            # Net effect: snake shrinks by 1 compared to before the step.
            self.snake.pop()    # cancel the growth (back to original length)
            self.snake.pop()    # shrink by 1 (red apple penalty)
            self.red_apple = None
            self._place_red_apple()
            reward = REWARD_RED_APPLE
            self.score -= 1
            info['cause'] = 'red_apple'

            # Check if length dropped to 0
            if len(self.snake) == 0:
                self.done = True
                reward = REWARD_DEATH
                info['cause'] = 'null_length'
                return None, reward, self.done, info
        else:
            # Normal move: remove tail
            self.snake.pop()

        self.max_length = max(self.max_length, len(self.snake))
        info['length'] = len(self.snake)

        return None, reward, self.done, info

    # ------------------------------------------------------------------
    # Board grid for display
    # ------------------------------------------------------------------

    def get_board_grid(self):
        """
        Return the full board as a 2D list of cell types (int constants).
        Used by the display module.
        """
        grid = [[EMPTY] * self.board_size for _ in range(self.board_size)]

        for r, c in self.snake[1:]:
            grid[r][c] = SNAKE_BODY
        if self.snake:
            hr, hc = self.snake[0]
            grid[hr][hc] = SNAKE_HEAD
        for r, c in self.green_apples:
            grid[r][c] = GREEN_APPLE
        if self.red_apple:
            rr, rc = self.red_apple
            grid[rr][rc] = RED_APPLE

        return grid

    def get_info(self):
        """Return current game stats."""
        return {
            'length': len(self.snake),
            'steps': self.steps,
            'score': self.score,
            'max_length': self.max_length,
            'done': self.done,
        }
