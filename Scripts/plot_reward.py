"""Print the eval reward per step from training logs and save a plot.

Reads the `steps=... reward=... t=...` lines that train_test.py prints.

    python plot_reward.py                      # ctrl.log -> reward_plot.png
    python plot_reward.py ctrl.log -o out.png
    python plot_reward.py test5.log ctrl.log   # overlay several runs
"""
import argparse
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # no display in WSL
import matplotlib.pyplot as plt

LINE = re.compile(r"steps=\s*(\d+)\s+reward=(-?[\d.]+)\s+t=(\d+):(\d+):([\d.]+)")


def parse(path):
    rows = []
    for line in Path(path).read_text(errors="replace").splitlines():
        m = LINE.search(line)
        if m:
            h, mi, s = int(m[3]), int(m[4]), float(m[5])
            rows.append((int(m[1]), float(m[2]), h * 3600 + mi * 60 + s))
    return rows


def print_table(name, rows):
    print(f"\n{name}")
    print(f"{'steps':>12} {'reward':>9} {'change':>9} {'elapsed':>9}")
    prev = None
    for steps, reward, secs in rows:
        change = "" if prev is None else f"{reward - prev:+.3f}"
        print(f"{steps:>12,} {reward:>9.3f} {change:>9} {secs / 60:>7.1f} m")
        prev = reward


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("logs", nargs="*", default=["ctrl.log"], help="training log files (default: ctrl.log)")
    ap.add_argument("-o", "--out", default="reward_plot.png", help="output image (default: reward_plot.png)")
    args = ap.parse_args()

    fig, ax = plt.subplots(figsize=(9, 5))
    for log in args.logs:
        rows = parse(log)
        if not rows:
            print(f"{log}: no 'steps=... reward=...' lines found")
            continue
        print_table(log, rows)
        steps = [r[0] / 1e6 for r in rows]
        rewards = [r[1] for r in rows]
        ax.plot(steps, rewards, marker="o", label=Path(log).name)
        ax.annotate(f"{rewards[-1]:.1f}", (steps[-1], rewards[-1]),
                    textcoords="offset points", xytext=(6, 0), va="center")

    ax.set_xlabel("environment steps (millions)")
    ax.set_ylabel("eval episode reward")
    ax.set_title("Go1 joystick: eval reward vs steps")
    ax.grid(alpha=0.3)
    if len(args.logs) > 1:
        ax.legend()
    fig.tight_layout()
    fig.savefig(args.out, dpi=150)
    print(f"\nsaved {args.out}")


if __name__ == "__main__":
    main()
