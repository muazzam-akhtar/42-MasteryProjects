"""
snake.py - Learn2Slither Entry Point

Usage:
    python snake.py [options]

Options:
    -sessions N         Number of training sessions (default: 1)
    -visual on/off      Enable/disable graphical display (default: on)
    -speed SPEED        slow/normal/fast/turbo (default: normal)
    -step-by-step       Wait for SPACE between steps
    -save FILE          Save model after training
    -load FILE          Load model before running
    -dontlearn          Disable learning (evaluation mode)
    -silent             Suppress terminal output
    -board-size N       Board size NxN (default: 10)
    -stats              Print Q-table summary after training
"""

import argparse

from environment import Environment
from interpreter import Interpreter
from agent import QLearningAgent


def parse_args():
    parser = argparse.ArgumentParser(
        description="Learn2Slither — Snake Reinforcement Learning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-sessions", type=int, default=1)
    parser.add_argument("-visual", choices=["on", "off"], default="on")
    parser.add_argument("-speed", choices=["slow", "normal", "fast", "turbo"],
                        default="normal")
    parser.add_argument("-step-by-step", action="store_true",
                        dest="step_by_step")
    parser.add_argument("-save", type=str, default=None, metavar="FILE")
    parser.add_argument("-load", type=str, default=None, metavar="FILE")
    parser.add_argument("-dontlearn", action="store_true")
    parser.add_argument("-silent", action="store_true")
    parser.add_argument("-board-size", type=int, default=10, dest="board_size")
    parser.add_argument("-stats", action="store_true")
    return parser.parse_args()


def run(args):
    try:
        env = Environment(board_size=args.board_size)
        interp = Interpreter()
        agent = QLearningAgent(learning=not args.dontlearn)

        if args.load:
            agent.load(args.load)
            print(f"Load trained model from {args.load}")

        # ── Display setup ────────────────────────────────────────────────────
        display = None
        if args.visual == "on":
            try:
                from display import Display
                display = Display(
                    speed=args.speed,
                    step_by_step=args.step_by_step,
                    board_size=args.board_size,
                )
                display.set_session_info(0, args.sessions)
                display.show_lobby(model_path=args.load)
            except ImportError as e:
                print(f"[Warning] Display unavailable: {e}")

        if args.dontlearn:
            print("[Mode] Evaluation only — learning disabled.\n")

        overall_best = 0
        overall_steps = 0
        log_interval = 1 if args.sessions <= 100 else max(1,
                                                          args.sessions // 100)

        print(f"Starting {args.sessions} trained session(s)...\n")

        for session in range(1, args.sessions + 1):
            env.reset()
            vision = interp.get_state(env)

            if display:
                display.set_session_info(session, args.sessions, overall_best)

            last_action = None
            session_done = False
            max_steps = args.board_size * args.board_size * 10

            while not session_done:
                if env.steps >= max_steps:
                    info = {
                        'cause': 'timeout',
                        'length': len(env.snake),
                        'steps': env.steps
                        }
                    session_done = True
                    break
                action = agent.choose_action(vision)

                if not args.silent:
                    interp.print_state(vision, action)

                _, reward, done, info = env.step(action)
                next_vision = interp.get_state(env)

                agent.update(vision, action, reward, next_vision, done)

                vision = next_vision
                last_action = action

                if display:
                    display.render(
                        env,
                        action=last_action,
                        extra_info={
                            'Reward':   f"{reward:.1f}",
                            'Epsilon':  f"{agent.epsilon:.3f}",
                            'States':   str(len(agent.q_table)),
                            'Episode':  str(agent.episode),
                        }
                    )
                    if done:
                        display.show_game_over(info)

                if done:
                    session_done = True

            agent.end_episode()

            final = env.get_info()
            max_len = final['max_length']
            steps = final['steps']
            cause = info.get('cause', 'unknown')

            overall_best = max(overall_best, max_len)
            overall_steps = max(overall_steps, steps)

            if display:
                display.record_session(max_len, steps, overall_best)

            if session % log_interval == 0 or session == args.sessions:
                print(
                    f"Session {session:>6}/{args.sessions} | "
                    f"best length = {overall_best:>3} | "
                    f"this session = {max_len:>3} | "
                    f"steps = {steps:>5} | "
                    f"epsilon = {agent.epsilon:.4f} | "
                    f"cause = {cause}"
                )
        print(f"\nGame over, max length = {overall_best}, "
              f"max duration = {overall_steps}")

        if args.stats:
            agent.print_q_table(top_n=15)
            print(f"[Agent stats] {agent.stats()}")

        if args.save:
            agent.save(args.save)
            print(f"Save learning state in {args.save}")

        if display:
            display.show_results(overall_best, overall_steps, args.sessions)
            display.close()
    except Exception as e:
        print(f"Error: {e}")


def main():
    args = parse_args()
    run(args)


if __name__ == '__main__':
    main()
