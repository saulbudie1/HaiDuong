"""Plot distance, velocity and rotation from a rollout's motion data.

rollout.py saves motion_<...>.npz; this script turns it into three graphs.

    python plot_motion.py motion_x1.0_y0.0_yaw0.0_go1_final.npz
    python plot_motion.py motion_*.npz -o out_dir
"""
import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # no display in WSL
import matplotlib.pyplot as plt
import numpy as np


def yaw_from_quat(q):
    # MuJoCo quaternion order is (w, x, y, z)
    w, x, y, z = q.T
    return np.arctan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z))


def plot(path, out_dir):
    d = np.load(path, allow_pickle=True)
    dt, cmd = float(d["dt"]), d["command"]
    t = (np.arange(len(d["pos"])) + 1) * dt
    xy = d["pos"][:, :2] - d["pos"][0, :2]
    dist = np.linalg.norm(xy, axis=1)
    path_len = np.linalg.norm(np.diff(xy, axis=0), axis=1).sum()
    yaw = np.degrees(np.unwrap(yaw_from_quat(d["quat"])))
    yaw -= yaw[0]
    vx, vy = d["linvel"][:, 0], d["linvel"][:, 1]
    yaw_rate = d["gyro"][:, 2]

    print(f"\n{Path(path).name}  (command x={cmd[0]}, y={cmd[1]}, yaw={cmd[2]})")
    print(f"  distance from start at end : {dist[-1]:.3f} m")
    print(f"  path length                : {path_len:.3f} m")
    print(f"  mean velocity x, y         : {vx.mean():+.3f}, {vy.mean():+.3f} m/s")
    print(f"  yaw turned                 : {yaw[-1]:+.1f} deg, mean rate {yaw_rate.mean():+.3f} rad/s")

    fig, axs = plt.subplots(3, 1, figsize=(9, 10), sharex=True)

    ax = axs[0]
    ax.plot(t, xy[:, 0], label="x")
    ax.plot(t, xy[:, 1], label="y")
    ax.plot(t, dist, "k", label="distance from start")
    ax.set_ylabel("position (m)")
    ax.set_title(f"Distance  (ends {dist[-1]:.2f} m from start)")
    ax.legend(loc="upper left")

    ax = axs[1]
    ax.plot(t, vx, color="C0", label="velocity x")
    ax.plot(t, vy, color="C1", label="velocity y")
    ax.axhline(cmd[0], color="C0", ls="--", label=f"command x = {cmd[0]}")
    ax.axhline(cmd[1], color="C1", ls="--", label=f"command y = {cmd[1]}")
    ax.set_ylabel("body-frame velocity (m/s)")
    ax.set_title(f"Velocity vs command  (mean track {float(np.mean(d['track'])):.3f})")
    ax.legend(loc="upper left", ncol=2)

    ax = axs[2]
    ax.plot(t, yaw, color="C2", label="yaw angle")
    ax.set_ylabel("yaw angle (deg)", color="C2")
    ax.set_xlabel("time (s)")
    ax.set_title("Rotation")
    ax2 = ax.twinx()
    ax2.plot(t, yaw_rate, color="C3", alpha=0.6, label="yaw rate")
    ax2.axhline(cmd[2], color="C3", ls="--", label=f"command yaw = {cmd[2]}")
    ax2.set_ylabel("yaw rate (rad/s)", color="C3")
    lines = ax.get_lines() + ax2.get_lines()
    ax.legend(lines, [l.get_label() for l in lines], loc="upper left")

    for a in axs:
        a.grid(alpha=0.3)
    fig.suptitle(f"{d['ckpt']}: command x={cmd[0]}, y={cmd[1]}, yaw={cmd[2]}")
    fig.tight_layout()

    out = Path(out_dir) / (Path(path).stem + ".png")
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"  saved {out}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("files", nargs="+", help="motion_*.npz files from rollout.py")
    ap.add_argument("-o", "--out-dir", default=".", help="folder for the PNGs (default: current)")
    args = ap.parse_args()
    Path(args.out_dir).mkdir(parents=True, exist_ok=True)
    for f in args.files:
        plot(f, args.out_dir)


if __name__ == "__main__":
    main()
