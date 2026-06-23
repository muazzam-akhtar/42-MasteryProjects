"""
display.py - Learn2Slither Enhanced Display Module

Screens:
    1. LOBBY        - title screen, load model or start fresh
    2. CONFIG       - configure sessions, speed, board size, model path
    3. GAME         - live board + sidebar + mini stats chart
    4. RESULTS      - post-training summary with score graph
"""

import sys
import os

try:
    import pygame
except ImportError:
    pygame = None

from environment import (
    EMPTY, SNAKE_HEAD, SNAKE_BODY, GREEN_APPLE, RED_APPLE)

# ── Palette ──────────────────────────────────────────────────────────────────
C_BG = (13, 13, 20)
C_PANEL = (22, 22, 35)
C_BORDER = (45, 45, 65)
C_GRID = (28, 28, 42)
C_EMPTY = (18, 18, 28)
C_HEAD = (80, 150, 240)
C_BODY = (50, 105, 190)
C_GREEN = (55, 200, 85)
C_RED = (220, 55, 55)
C_TEXT = (210, 215, 225)
C_LABEL = (110, 115, 135)
C_HIGHLIGHT = (255, 200, 50)
C_ACCENT = (100, 200, 160)
C_DIM = (60, 65, 80)
C_CHART_LINE = (80, 180, 240)
C_CHART_BEST = (255, 200, 50)
C_OVERLAY = (0, 0, 0, 160)

SPEEDS = {'slow': 500, 'normal': 150, 'fast': 30, 'turbo': 0}
DEFAULT_SPEED = 'normal'

CELL_SIZE = 46
SIDEBAR_W = 230
MARGIN = 16
CHART_H = 90


def _cell_color(cell_type):
    return {
        EMPTY:          C_EMPTY,
        SNAKE_HEAD:     C_HEAD,
        SNAKE_BODY:     C_BODY,
        GREEN_APPLE:    C_GREEN,
        RED_APPLE:      C_RED,
    }.get(cell_type, C_EMPTY)


class Display:
    """
    Full-featured pygame display with lobby, config, game, and results screens.

    Args:
        speed        (str) : one of slow/normal/fast/turbo
        step_by_step (bool): wait for SPACE between steps
        board_size   (int) : board dimension
    """

    def __init__(self, speed=DEFAULT_SPEED, step_by_step=False, board_size=10):
        if pygame is None:
            raise ImportError("pygame required. Install: pip install pygame")

        self.speed = speed
        self.delay_ms = SPEEDS.get(speed, SPEEDS[DEFAULT_SPEED])
        self.step_by_step = step_by_step
        self.board_size = board_size
        self._board_px = board_size * CELL_SIZE
        self._win_w = self._board_px + SIDEBAR_W + MARGIN * 3
        self._win_h = self._board_px + MARGIN * 2 + 30

        self.session = 0
        self.total_sessions = 0
        self.best_length = 0
        self.overall_steps = 0

        # Rolling history for chart (last N sessions)
        self._hist_len = []     # max length per session
        self._hist_steps = []   # steps per session
        self._hist_best = []    # running best length

        self._waiting_step = False

        pygame.init()
        pygame.display.set_caption(
            "Learn2Slither — Snake RL"
        )
        self.screen = pygame.display.set_mode((self._win_w, self._win_h))
        self.clock = pygame.time.Clock()

        self.font_title = pygame.font.SysFont("monospace", 28, bold=True)
        self.font_large = pygame.font.SysFont("monospace", 20, bold=True)
        self.font_med = pygame.font.SysFont("monospace", 15)
        self.font_small = pygame.font.SysFont("monospace", 12)

    # ── Public API ───────────────────────────────────────────────────────────

    def show_lobby(self, model_path=None):
        """
        Display the lobby/title screen.
        Returns: 'play' always (just a splash, auto-advances after keypress).
        """
        waiting = True
        t = 0
        # Raise window and flush stale events before listening
        pygame.event.clear()

        while waiting:
            t += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.close()
                        sys.exit(0)
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

            self.screen.fill(C_BG)
            self._draw_lobby(model_path, t)
            pygame.display.flip()
            self.clock.tick(30)

        pygame.event.clear()
        return 'play'

    def set_session_info(self, session, total, best_length=0):
        self.session = session
        self.total_sessions = total
        self.best_length = best_length

    def record_session(self, max_len, steps, best_so_far):
        """Call after each session to feed the chart."""
        self._hist_len.append(max_len)
        self._hist_steps.append(steps)
        self._hist_best.append(best_so_far)

    def render(self, env, action=None, extra_info=None):
        """Render the live game screen."""
        self._handle_events()
        self.screen.fill(C_BG)

        grid = env.get_board_grid()
        info = env.get_info()

        self._draw_board(grid)
        self._draw_sidebar(info, action, extra_info)
        self._draw_bottom_bar()

        pygame.display.flip()

        if self.step_by_step:
            self._wait_for_step()
        elif self.delay_ms > 0:
            pygame.time.delay(self.delay_ms)

    def show_game_over(self, info):
        """Brief game-over flush overlay."""
        bx = MARGIN
        by = MARGIN
        overlay = pygame.Surface((self._board_px, self._board_px),
                                 pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (bx, by))

        msg = self.font_large.render("GAME OVER", True, C_RED)
        sub = self.font_med.render(
            f"Length: {info.get('length', 0)}   Steps: {info.get('steps', 0)}",
            True, C_TEXT
        )
        cause_str = info.get('cause', '')
        cause = self.font_small.render(
            f"Cause: {cause_str}", True, C_LABEL
        )

        cx = bx + self._board_px // 2
        cy = by + self._board_px // 2
        self.screen.blit(msg, msg.get_rect(center=(cx, cy - 20)))
        self.screen.blit(sub, sub.get_rect(center=(cx, cy + 10)))
        self.screen.blit(cause, cause.get_rect(center=(cx, cy + 30)))

        pygame.display.flip()
        pygame.time.delay(500)

    def show_results(self, overall_best, overall_steps, total_sessions):
        """
        Full results screen shown after all sessions complete.
        Displays score chart and summary. Press any key to close.
        """
        pygame.event.clear
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.close()
                        sys.exit(0)
                    waiting = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
            self.screen.fill(C_BG)
            self._draw_results(overall_best, overall_steps, total_sessions)
            pygame.display.flip()
            self.clock.tick(30)

    def close(self):
        pygame.quit()

    # ── Lobby screen ─────────────────────────────────────────────────────────

    def _draw_lobby(self, model_path, t):
        w, h = self._win_w, self._win_h
        cx = w // 2

        # Animated snake trail in background
        for i in range(12):
            alpha = max(20, 80 - i * 6)
            s = pygame.Surface((CELL_SIZE - 4, CELL_SIZE - 4), pygame.SRCALPHA)
            s.fill((*C_BODY, alpha))
            ox = cx - 6 * CELL_SIZE + i * CELL_SIZE + ((t // 2) % CELL_SIZE)
            self.screen.blit(s, (ox, h // 2 - CELL_SIZE // 2))

        # Title
        title = self.font_title.render("LEARN2SLITHER", True, C_HIGHLIGHT)
        self.screen.blit(title, title.get_rect(center=(cx, h // 2 - 100)))

        sub = self.font_large.render("Snake Reinforcement Learning", True,
                                     C_ACCENT)
        self.screen.blit(sub, sub.get_rect(center=(cx, h // 2 - 60)))

        # Divider
        pygame.draw.line(self.screen, C_BORDER, (cx - 180, h // 2 - 35),
                         (cx + 180, h // 2 - 35), 1)

        # Model info
        if model_path and os.path.exists(model_path):
            minfo = self.font_med.render(
                f"Model: {os.path.basename(model_path)}", True, C_GREEN)
        else:
            minfo = self.font_med.render(
                "No model loaded — training from scratch", True, C_LABEL)
        self.screen.blit(minfo, minfo.get_rect(center=(cx, h // 2)))

        # Board size
        binfo = self.font_med.render(
            f"Board: {self.board_size}×{self.board_size}    "
            f"Sessions: {self.total_sessions}   Speed: {self.speed}",
            True, C_LABEL
        )
        self.screen.blit(binfo, binfo.get_rect(center=(cx, h // 2 + 28)))

        # Start prompt (blinking)
        if (t // 20) % 20 == 0:
            prompt = self.font_med.render(
                "Press any key to start...",
                True, C_TEXT
            )
            self.screen.blit(prompt, prompt.get_rect(center=(cx, h // 2 + 70)))

        # Controls hint
        controls = self.font_small.render(
            "[Q] Quit   [+/-] Speed     [S] Step mode   [SPACE] Step",
            True, C_DIM
        )
        self.screen.blit(controls, controls.get_rect(center=(cx, h - 20)))

    # ── Game board ───────────────────────────────────────────────────────────

    def _draw_board(self, grid):
        bx, by = MARGIN, MARGIN
        # Border
        pygame.draw.rect(self.screen, C_BORDER,
                         (bx - 2, by - 2, self._board_px + 4,
                          self._board_px + 4), border_radius=4)

        for row in range(self.board_size):
            for col in range(self.board_size):
                x = bx + col * CELL_SIZE
                y = by + row * CELL_SIZE
                cell = grid[row][col]
                color = _cell_color(cell)
                rect = pygame.Rect(x + 1, y + 1, CELL_SIZE - 2, CELL_SIZE - 2)
                pygame.draw.rect(self.screen, color, rect, border_radius=3)
                pygame.draw.rect(self.screen, C_GRID, (x, y, CELL_SIZE,
                                                       CELL_SIZE), 1)
                if cell == SNAKE_HEAD:
                    cx2 = x + CELL_SIZE // 2
                    cy2 = y + CELL_SIZE // 2
                    pygame.draw.circle(self.screen,
                                       (180, 255, 255), (cx2, cy2), 5)
    # ── Sidebar ──────────────────────────────────────────────────────────────

    def _draw_sidebar(self, info, action, extra_info):
        sx = self._board_px + MARGIN * 2
        sy = MARGIN

        # ── Title block ──
        title = self.font_large.render("LEARN2SLITHER",
                                       True, C_HIGHLIGHT)
        self.screen.blit(title, (sx, sy))
        sy += 26
        sub = self.font_small.render("Snake RL Agent",
                                     True, C_LABEL)
        self.screen.blit(sub, (sx, sy))
        sy += 20
        self._hline(sx, sy)
        sy += 12

        # ── Session progress bar ──
        prog_label = self.font_small.render(
            f"Session {self.session}/{self.total_sessions}", True, C_LABEL
        )
        self.screen.blit(prog_label, (sx, sy))
        sy += 16
        bar_w = SIDEBAR_W - MARGIN
        pygame.draw.rect(self.screen, C_BORDER, (sx, sy, bar_w, 8),
                         border_radius=4)
        if self.total_sessions > 0:
            fill = int(bar_w * self.session / self.total_sessions)
            if fill > 0:
                pygame.draw.rect(self.screen, C_ACCENT, (sx, sy, fill, 8),
                                 border_radius=4)
        sy += 18

        # ── Live stats ──
        self._hline(sx, sy)
        sy += 10
        self._row("Length", str(info['length']), sx, sy)
        sy += 20
        self._row("Best", str(self.best_length), sx, sy)
        sy += 20
        self._row("Steps", str(info['steps']), sx, sy)
        sy += 20
        self._row("Score", str(info['score']), sx, sy)
        sy += 20
        self._row("Board", f"{self.board_size}x{self.board_size}", sx, sy)
        sy += 22

        # ── Action block ──
        self._hline(sx, sy)
        sy += 10
        alabel = self.font_small.render("Last action:", True, C_LABEL)
        self.screen.blit(alabel, (sx, sy))
        sy += 18
        aval = self.font_large.render(action if action else "-", True, C_HEAD)
        self.screen.blit(aval, (sx, sy))
        sy += 30
        # ── Extra info (epsilon, states, reward) ──
        if extra_info:
            self._hline(sx, sy)
            sy += 10
            for k, v in extra_info.items():
                self._row(k, str(v), sx, sy)
                sy += 22

        # ── Mini chart ──
        if len(self._hist_len) >= 2:
            self._hline(sx, sy)
            sy += 8
            clabel = self.font_small.render("Length history", True, C_LABEL)
            self.screen.blit(clabel, (sx, sy))
            sy += 14
            self._draw_mini_chart(sx, sy, SIDEBAR_W - MARGIN, CHART_H)
            sy += CHART_H + 6

        # ── Speed & mode ──
        self._hline(sx, sy)
        sy += 10
        self._row("Speed", self.speed, sx, sy)
        sy += 18
        mode = "step-by-step" if self.step_by_step else "continuous"
        self._row("Mode", mode, sx, sy)
        sy += 20
        # ── Legend ──
        self._hline(sx, sy)
        sy += 8
        for color, label in [
            (C_HEAD, "Snake Head"),
            (C_BODY, "Snake Body"),
            (C_GREEN, "Green Apple (+1)"),
            (C_RED, "Red Apple (-1)"),
        ]:
            pygame.draw.rect(self.screen, color, (sx, sy + 2, 10, 10),
                             border_radius=2)
            self.screen.blit(self.font_small.render(label, True, C_TEXT),
                             (sx + 16, sy))
            sy += 16

    def _draw_mini_chart(self, x, y, w, h):
        """Draw a small line chart of length history in the sidebar."""
        pygame.draw.rect(self.screen, C_PANEL, (x, y, w, h), border_radius=3)
        pygame.draw.rect(self.screen, C_BORDER, (x, y, w, h),
                         1, border_radius=3)

        data = self._hist_len[-80:]
        best = self._hist_best[-80:]
        if len(data) < 2:
            return

        max_val = max(max(data), max(best), 10)
        pts_len = []
        pts_best = []
        for i, v in enumerate(data):
            px = x + int(i * (w - 4) / (len(data) - 1)) + 2
            py = y + h - 4 - int(v * (h - 8) / max_val)
            pts_len.append((px, py))
        for i, v in enumerate(best):
            px = x + int(i * (w - 4) / (len(best) - 1)) + 2
            py = y + h - 4 - int(v * (h - 8) / max_val)
            pts_best.append((px, py))

        if len(pts_len) >= 2:
            pygame.draw.lines(self.screen, C_CHART_LINE, False, pts_len, 1)
        if len(pts_best) >= 2:
            pygame.draw.lines(self.screen, C_CHART_BEST, False, pts_best, 1)

        # Axis labels
        top_lbl = self.font_small.render(str(max_val), True, C_DIM)
        self.screen.blit(top_lbl, (x + 2, y + 1))

    # ── Results screen ───────────────────────────────────────────────────────

    def _draw_results(self, overall_best, overall_steps, total_sessions):
        w, h = self._win_w, self._win_h
        cx = w // 2

        title = self.font_title.render("TRAINING COMPLETE", True, C_HIGHLIGHT)
        self.screen.blit(title, title.get_rect(center=(cx, 36)))

        self._hline_full(60)

        # Summary stats grid
        stats = [
            ("Sessions trained", str(total_sessions)),
            ("Best length achieved", str(overall_best)),
            ("Longest survival", f"{overall_steps} steps"),
            ("States discovered", str(len(self._hist_len))),
        ]
        for i, (label, val) in enumerate(stats):
            lx = 60 + (i % 2) * (w // 2 - 40)
            ly = 78 + (i // 2) * 44
            pygame.draw.rect(self.screen, C_PANEL, (lx, ly, w // 2 - 60, 36),
                             border_radius=6)
            pygame.draw.rect(self.screen, C_BORDER, (lx, ly, w // 2 - 60, 36),
                             1, border_radius=6)
            lbl = self.font_small.render(label, True, C_LABEL)
            val_s = self.font_large.render(val, True, C_ACCENT)
            self.screen.blit(lbl, (lx + 8, ly + 4))
            self.screen.blit(val_s, (lx + 8, ly + 18))

        # Full chart
        chart_y = 175
        chart_h = h - chart_y - 60
        chart_w = w - 80

        if len(self._hist_len) >= 2:
            pygame.draw.rect(self.screen, C_PANEL,
                             (40, chart_y, chart_w, chart_h), border_radius=6)
            pygame.draw.rect(self.screen, C_BORDER,
                             (40, chart_y, chart_w, chart_h),
                             1, border_radius=6)

            chart_title = self.font_small.render(
                "— this session    — best so far", True, C_LABEL
                )
            self.screen.blit(chart_title, (44, chart_y + 4))
            data = self._hist_len
            best = self._hist_best
            max_val = max(max(data), max(best), 10)
            n = len(data)

            def to_pt(i, v, cx2=40, cy2=chart_y, cw=chart_w, ch=chart_h):
                px = cx2 + 6 + int(i * (cw - 12) / max(n - 1, 1))
                py = cy2 + ch - 6 - int(v * (ch - 16) / max_val)
                return (px, py)

            pts_len = [to_pt(i, v) for i, v in enumerate(data)]
            pts_best = [to_pt(i, v) for i, v in enumerate(best)]

            if len(pts_len) >= 2:
                pygame.draw.lines(self.screen, C_CHART_LINE, False, pts_len, 2)
            if len(pts_best) >= 2:
                pygame.draw.lines(self.screen, C_CHART_BEST, False, pts_best,
                                  2)

            # Y axis labels
            for tick in [0, max_val // 2, max_val]:
                ty = chart_y + chart_h - 6 - int(
                    tick * (chart_h - 16) / max_val)
                pygame.draw.line(self.screen, C_BORDER, (40, ty), (46, ty), 1)
                lbl = self.font_small.render(str(tick), True, C_DIM)
                self.screen.blit(lbl, (22, ty - 6))

        self._hline_full(h - 45)
        prompt = self.font_med.render("Press any key to exit...", True, C_DIM)
        self.screen.blit(prompt, prompt.get_rect(center=(cx, h - 26)))

    # ── Bottom bar ───────────────────────────────────────────────────────────

    def _draw_bottom_bar(self):
        y = self._win_h - 20
        hint = (
            "[Q] Quit   [+/-] Speed     [SPACE] Step"
            if self.step_by_step
            else "[Q] Quit   [+/-] Speed   [S] Step mode"
        )
        surf = self.font_small.render(hint, True, C_DIM)
        self.screen.blit(surf, (MARGIN, y))

    # ── Helpers ──────────────────────────────────────────────────────────────

    def _hline(self, x, y):
        pygame.draw.line(self.screen, C_BORDER, (x, y),
                         (x + SIDEBAR_W - MARGIN, y), 1)

    def _hline_full(self, y):
        pygame.draw.line(self.screen, C_BORDER, (20, y),
                         (self._win_w + SIDEBAR_W - 20, y), 1)

    def _row(self, label, value, x, y):
        self.screen.blit(self.font_small.render(f"{label}:", True, C_LABEL),
                         (x, y))
        self.screen.blit(self.font_med.render(value, True, C_TEXT),
                         (x + 95, y))

    # ── Event handling ───────────────────────────────────────────────────────

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.close()
                    sys.exit(0)
                elif event.key in (pygame.K_EQUALS, pygame.K_PLUS):
                    self._speed_up()
                elif event.key == pygame.K_MINUS:
                    self._speed_down()
                elif event.key == pygame.K_s and not self.step_by_step:
                    self.step_by_step = True

    def _handle_quit_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.close()
                    sys.exit(0)

    def _wait_for_step(self):
        self._waiting_step = True
        msg = self.font_med.render("SPACE to skip | S to resume",
                                   True, C_HIGHLIGHT)
        self.screen.blit(msg, msg.get_rect(center=(
            MARGIN + self._board_px // 2, self._win_h - 16
        )))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.close()
                        sys.exit(0)
                    elif event.key == pygame.K_SPACE:
                        waiting = False
                    elif event.key == pygame.K_s:
                        self.step_by_step = False
                        waiting = False
            self.clock.tick(30)
        self._waiting_step = False

    def _speed_up(self):
        keys = list(SPEEDS.keys())
        idx = keys.index(self.speed)
        if idx < len(keys) - 1:
            self.speed = keys[idx + 1]
            self.delay_ms = SPEEDS[self.speed]

    def _speed_down(self):
        keys = list(SPEEDS.keys())
        idx = keys.index(self.speed)
        if idx > 0:
            self.speed = keys[idx - 1]
            self.delay_ms = SPEEDS[self.speed]
