"""
interpreter.py - Learn2Slither Interpreter Module

Translates the raw board state into the snake's vision (State),
and prints that vision to the terminal.

Symbols:
    W = Wall
    H = Snake Head
    S = Snake body segment
    G = Green apple
    R = Red apple
    0 = Empty space
"""

from environment import DIRECTIONS, DELTA, UP, DOWN, LEFT, RIGHT


class Interpreter:
    """
    Reads the environment and produces the snake's vision state.

    The snake can only see in 4 directions from its head.
    Each directional ray lists every cell from head outward until
    a wall is reached (wall symbol included at the end).
    """

    def get_state(self, env):
        """
        Compute the snake's vision from the current environment state.

        Args:
            env (Environment): the current game environment

        Returns:
            dict: {UP: [...], DOWN: [...], LEFT: [...], RIGHT: [...]}
                  Each value is a list of symbol characters.
        """
        if not env.snake:
            return {d: ['W'] for d in DIRECTIONS}

        head_r, head_c = env.snake[0]
        vision = {}

        for direction, (dr, dc) in DELTA.items():
            ray = []
            r, c = head_r + dr, head_c + dc
            while 0 <= r < env.board_size and 0 <= c < env.board_size:
                ray.append(self._cell_symbol(env, r, c))
                r += dr
                c += dc
            ray.append('W')
            vision[direction] = ray

        return vision

    def _cell_symbol(self, env, r, c):
        """Return the vision symbol for a single board cell."""
        if (r, c) == env.snake[0]:
            return 'H'
        if (r, c) in env.snake[1:]:
            return 'S'
        if (r, c) in env.green_apples:
            return 'G'
        if (r, c) == env.red_apple:
            return 'R'
        return '0'

    def print_state(self, state, action=None):
        """
        Print the snake's vision to the terminal in the required cross format.

            W          <- top of UP ray
            0
            G
            H 0 0 R W  <- horizontal ray (LEFT W ... H ... RIGHT W)
            S
            0
            W          <- bottom of DOWN ray

        Args:
            state  (dict): vision dict from get_state()
            action (str) : last action taken (optional, printed below vision)
        """
        up_ray = state[UP]
        down_ray = state[DOWN]
        left_ray = state[LEFT]
        right_ray = state[RIGHT]

        # Vertical: top of board first, then H, then down
        up_col = list(reversed(up_ray))
        vertical = up_col + ['H'] + list(down_ray)

        # Horizontal: left edge first, then H, then right
        left_strip = list(reversed(left_ray))
        horizontal = left_strip + ['H'] + list(right_ray)

        h_col = len(left_strip)     # column index of H in horizontal line
        h_row = len(up_col)         # row index of H in vertical list

        lines = []
        for i, symbol in enumerate(vertical):
            if i == h_row:
                lines.append(''.join(horizontal))
            else:
                lines.append(' ' * h_col + symbol)

        print('\n'.join(lines))
        if action:
            print(f'\n{action}\n')
