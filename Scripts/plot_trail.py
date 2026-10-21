"""Bird's-eye trail of the robot from a rollout's motion data.

rollout.py saves motion_<...>.npz; this script draws a square top-down map with
the path of the body centre and the path of the head tip, both shaded from
start to end, so you can see where the robot was and which way it faced.

    python plot_trail.py motion_x1.0_y-1.0_yaw0.0_go1_final.npz
    python plot_trail.py motion_*.npz -o out_dir
    python plot_trail.py motion_x1.0_y-1.0_yaw0.0_go1_final.npz --head-length 2

On a long walk the real head length (0.3 m) is tiny next to the map, so the head
trail sits on top of the body trail. A bigger --head-length pulls them apart to
show which way the robot faces.
"""
import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # no display in WSL
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.cm import ScalarMappable
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.lines import Line2D

GROUND = "#1d1d26"
GRID = "#2e2e3a"
TEXT = "#c9c9d6"
BODY_CMAP = LinearSegmentedColormap.from_list("body", ["#82782f", "#5bd117"])
HEAD_CMAP = LinearSegmentedColormap.from_list("head", ["#1d1c85", "#f0569e"])
HEAD_LENGTH = 0.3  # m, the `head` site in the Go1 trunk frame (go1_mjx.xml)


def yaw_from_quat(q):
    # MuJoCo quaternion order is (w, x, y, z)
    w, x, y, z = q.T
    return np.arctan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))


def trail(ax, xy, t, cmap, norm, width):
    segs = np.stack([xy[:-1], xy[1:]], axis=1)
    lc = LineCollection(segs, cmap=cmap, norm=norm, linewidth=width, capstyle="round", zorder=3)
    lc.set_array(0.5 * (t[:-1] + t[1:]))
    ax.add_collection(lc)


def colorbar(fig, rect, cmap, norm, label):
    cax = fig.add_axes(rect)
    cb = fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), cax=cax, orientation="horizontal")
    cb.set_label(label, color=TEXT)
    cb.ax.tick_params(colors=TEXT)
    cb.outline.set_edgecolor(GRID)


def plot(path, out_dir, head_length, tick_every):
    d = np.load(path, allow_pickle=True)
    dt, cmd = float(d["dt"]), d["command"]
    centre = d["pos"][:, :2]
    yaw = yaw_from_quat(d["quat"])
    head = centre + head_length * np.stack([np.cos(yaw), np.sin(yaw)], axis=1)
    t = (np.arange(len(centre)) + 1) * dt
    norm = Normalize(0, t[-1])

    fig = plt.figure(figsize=(8, 9), facecolor=GROUND)
    ax = fig.add_axes([0.12, 0.27, 0.8, 0.65], facecolor=GROUND)

    # thin lines from the centre to the head tip show the heading over time
    idx = np.arange(0, len(centre), tick_every)
    ticks = np.stack([centre[idx], head[idx]], axis=1)
    tc = LineCollection(ticks, cmap=HEAD_CMAP, norm=norm, linewidth=0.8, alpha=0.45, zorder=2)
    tc.set_array(t[idx])
    ax.add_collection(tc)

    trail(ax, centre, t, BODY_CMAP, norm, 3)
    trail(ax, head, t, HEAD_CMAP, norm, 2)

    ax.scatter(*centre[0], s=60, facecolor="none", edgecolor=TEXT, linewidth=1.2, zorder=5)
    ax.scatter(*centre[-1], s=70, color=BODY_CMAP(1.0), edgecolor=TEXT, linewidth=0.8, zorder=6)
    ax.scatter(*head[-1], s=45, color=HEAD_CMAP(1.0), edgecolor=TEXT, linewidth=0.8, zorder=6)

    marks = [
        Line2D([], [], marker="o", ls="", mfc="none", mec=TEXT, ms=8, label="start"),
        Line2D([], [], marker="o", ls="", mfc=BODY_CMAP(1.0), mec=TEXT, ms=8, label="body centre, end"),
        Line2D([], [], marker="o", ls="", mfc=HEAD_CMAP(1.0), mec=TEXT, ms=6, label="head tip, end"),
    ]
    ax.legend(handles=marks, loc="best", fontsize=9, facecolor=GROUND, edgecolor=GRID, labelcolor=TEXT)

    # square map, centred on everything drawn, never smaller than 1.5 m wide
    pts = np.vstack([centre, head])
    lo, hi = pts.min(axis=0), pts.max(axis=0)
    mid = (lo + hi) / 2
    half = max((hi - lo).max() / 2 * 1.15, 0.75)
    ax.set_xlim(mid[0] - half, mid[0] + half)
    ax.set_ylim(mid[1] - half, mid[1] + half)
    ax.set_aspect("equal", adjustable="box")
    ax.grid(color=GRID, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlabel("x (m)", color=TEXT)
    ax.set_ylabel("y (m)", color=TEXT)
    ax.tick_params(colors=TEXT)
    for side in ax.spines.values():
        side.set_edgecolor(GRID)

    dist = np.linalg.norm(centre[-1] - centre[0])
    fig.suptitle(
        f"{d['ckpt']}: command x={cmd[0]}, y={cmd[1]}, yaw={cmd[2]}\n"
        f"bird's-eye view, ends {dist:.2f} m from start (open circle = start)",
        color=TEXT, fontsize=11,
    )
    colorbar(fig, [0.12, 0.15, 0.8, 0.02], BODY_CMAP, norm, "body centre, time (s)")
    colorbar(fig, [0.12, 0.07, 0.8, 0.02], HEAD_CMAP, norm, "head tip, time (s)")

    out = Path(out_dir) / (Path(path).stem.replace("motion_", "trail_", 1) + ".png")
    fig.savefig(out, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"{Path(path).name}: saved {out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("files", nargs="+", help="motion_*.npz files from rollout.py")
    ap.add_argument("-o", "--out-dir", default=".", help="folder for the PNGs (default: current)")
    ap.add_argument("--head-length", type=float, default=HEAD_LENGTH,
                    help=f"distance from the body centre to the head tip in m (default: {HEAD_LENGTH})")
    ap.add_argument("--tick-every", type=int, default=25,
                    help="draw a heading line every N steps (default: 25, about 0.5 s)")
    args = ap.parse_args()
    Path(args.out_dir).mkdir(parents=True, exist_ok=True)
    for f in args.files:
        plot(f, args.out_dir, args.head_length, args.tick_every)


if __name__ == "__main__":
    main()
