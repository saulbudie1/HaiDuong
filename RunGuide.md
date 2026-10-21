# Run Guide — Go1 training and testing (local, WSL2)

How to train the Go1 policy, test it, and judge whether it walks. Written for my laptop setup (RTX 5060, WSL2 Ubuntu 24.04, env `go1env`).

---

## 0. One-time facts

| Thing | Where |
|---|---|
| Python environment | `~/go1env` |
| Working folder | `~/go1` (training script `train_test.py`, rollout script `rollout.py`) |
| Scripts in the repo | `Scripts/` (`train_test.py`, `rollout.py`, `plot_reward.py`, `plot_motion.py`). Copy them into the run folder, see 2.1. |
| First 100M run (backup) | `~/backup_run1` |
| Open the folder from Windows | `\\wsl$\Ubuntu-24.04\home\thanh\go1` |
| Project on Windows | `C:\Users\Admin\Documents\HaiDuong` (WSL path `/mnt/c/Users/Admin/Documents/HaiDuong`) |

---

## 1. Every new Ubuntu window

```
source ~/go1env/bin/activate
cd ~/go1
export XLA_PYTHON_CLIENT_PREALLOCATE=false
```
The prompt should start with `(go1env)`. Type commands **one at a time**. Pasting several lines at once caused problems before.

---

## 2. Train

### 2.1 Make a folder per run
Saved files have fixed names (`go1_final`, `ckpt_<step>`), so a new run in the same folder overwrites them. Use one folder per run:
```
mkdir -p ~/go1_run2
cp ~/go1/train_test.py ~/go1/rollout.py ~/go1/plot_reward.py ~/go1/plot_motion.py ~/go1_run2/
cd ~/go1_run2
```

### 2.2 Check the settings
```
grep -n "num_timesteps\|num_evals\|num_envs" train_test.py
```
Edit with `nano train_test.py` (`Ctrl+O`, `Enter` to save, `Ctrl+X` to exit).

| Setting | What it does |
|---|---|
| `num_timesteps` | Requested steps. The real total is rounded up (see section 6). |
| `num_evals` | How many evaluation points (graph points and checkpoints). Use 10 to 20. |
| `num_envs` | Robots simulated in parallel. 4096 fits 8 GB. Must divide 8192. |

Change **one thing at a time** between runs and write down what changed.

### 2.3 Start it in tmux
```
tmux new -s run2
```
Inside tmux (green bar at the bottom):
```
source ~/go1env/bin/activate
cd ~/go1_run2
export XLA_PYTHON_CLIENT_PREALLOCATE=false
python train_test.py 2>&1 | grep -v -E "iterations limit|To disable the print warning" | tee run2.log
```
- Detach (leave it running): `Ctrl+B`, release, then `D`.
- Come back: `tmux attach -t run2`.
- Scroll inside tmux: `Ctrl+B`, then `[`, arrows, `q` to quit.
- If tmux says "duplicate session": `tmux kill-session -t run2` and start again.

Before leaving a long run: laptop plugged in, sleep set to Never, lid open, vents clear.

### 2.4 What you should see
- A pause of 1 to 3 minutes (compile), then lines like `steps=  50790400  reward=19.556  t=0:10:50`.
- Lots of solver warnings. They are normal.
- At the end: `time to jit`, `time to train`, `last step count`.

Check progress from a second window:
```
grep "steps=" ~/go1_run2/run2.log | tail -5
ls ~/go1_run2
nvidia-smi
```
Normal under load: GPU in the 70s °C. The first checkpoint file appearing proves saving works.

### 2.5 Outputs
`go1_final` (final weights), `ckpt_<step>` (one per evaluation), the log file.

Measured speed so far: about 92,000 steps/s (100M steps in about 19 minutes at `num_envs` 4096).

---

## 3. Rollout (test the policy and make videos)

```
cd ~/go1_run2
python rollout.py <x> <y> <yaw> <checkpoint>
```
Example (walk forward at 1 m/s with the final policy):
```
python rollout.py 1 0 0 go1_final
```
- `x`: forward speed (m/s), `y`: sideways speed (m/s), `yaw`: turn rate (rad/s).
- Checkpoint: `go1_final`, `ckpt_50790400`, `ckpt_0` (untrained), and so on.
- It prints `mean track` and `mean linvel`, saves the motion data (`motion_<...>.npz`, see 3.1), then renders three videos (`top`, `side`, `track`). Wait for `done`.
- It takes a few minutes. Nothing prints until the end.
- To skip the videos and only save the motion data (faster, less GPU memory):
```
python rollout.py 1 0 0 go1_final --no-video
```

**Trained command range (stay inside it):** x ±1.5 m/s, y ±0.8 m/s, yaw ±1.2 rad/s. Larger values mean nothing.

If rendering fails with an EGL/OpenGL error:
```
sudo apt install -y libosmesa6-dev libgl1
```
then change `"egl"` to `"osmesa"` on the `MUJOCO_GL` line at the top of `rollout.py` (slower, but works).

### 3.1 Motion graphs (distance, velocity, rotation)

`plot_motion.py` reads the `.npz` that `rollout.py` saved. It never touches the GPU, so run it as a separate step:
```
python plot_motion.py motion_x1.0_y0.0_yaw0.0_go1_final.npz
```
It prints a short summary and saves `motion_x1.0_y0.0_yaw0.0_go1_final.png` with three graphs:

| Graph | Shows |
|---|---|
| Distance | x and y position and distance from the start, in metres. A standing robot gives flat lines. |
| Velocity vs command | Body-frame x and y velocity, with the commanded values as dashed lines. |
| Rotation | Yaw angle (degrees) and yaw rate (rad/s), with the yaw command dashed. |

- Several files at once, PNGs into a folder: `python plot_motion.py motion_*.npz -o plots`
- The `.npz` also holds the accelerometer reading (`accel`) if you ever want acceleration. It is not plotted.
- Test 6 check (29.5M steps, command 1 / 0 / 0): ends 0.04 m from the start, mean velocity about 0.002 m/s, `track` 0.019. This is standing still.

---

## 4. Get files to Windows

```
mkdir -p /mnt/c/Users/Admin/Documents/HaiDuong/Tests/TestN
cp ~/go1_run2/*.mp4 ~/go1_run2/*.png /mnt/c/Users/Admin/Documents/HaiDuong/Tests/TestN/
```
Name or sort videos by checkpoint and command. Keep weights and logs in WSL (backups: `cp ~/go1_run2/ckpt_* ~/go1_run2/go1_final ~/go1_run2/*.log ~/backup_run2/`).

### Reward graph from the log
```
python plot_reward.py run2.log -o reward_plot.png
```
It prints a table (steps, reward, change, elapsed time) and saves the graph. More `num_evals` means more points.

To compare runs on one graph, list several logs: `python plot_reward.py run1.log run2.log -o compare.png`. It needs matplotlib, so run it inside `go1env`.

---

## 5. What to look for when testing walks

Reward alone does not tell you whether it walks (a robot that just stands can earn about 17 of about 40). Use the rollout numbers and the video together.

### 5.1 The numbers

**`mean track`** is the average of `exp(-error² / 0.25)` over the run, where `error` is the gap between the commanded and actual x/y speed (m/s). Reading it:

| Velocity error | track |
|---|---|
| 0.1 m/s | about 0.96 |
| 0.2 m/s | about 0.85 |
| 0.3 m/s | about 0.70 |
| 0.5 m/s | about 0.37 |
| 1.0 m/s (e.g. standing still at x = 1) | about 0.02 |

**`mean linvel`** (body frame, x / y / z): x should be close to the commanded x, y close to the commanded y, and z close to 0. A big z or y when you asked for pure forward means bouncing or drifting.

Suggested rough pass criteria (my own, not a standard): `mean track` above about 0.8, mean `linvel` within about 0.2 m/s of the command, and no fall for the whole 20 s.

Notes:
- The mean includes the start-up transient.
- `track` only covers x/y speed. For yaw, use the Rotation graph from `plot_motion.py` (3.1) and the video.
- One rollout is one sample. Rerun a command, or compare checkpoints, before trusting small differences.

### 5.2 The video

- **Stays upright** for the whole 20 s. No collapse or flipping.
- **Actually travels.** Watch the floor grid and the lighting: they should move past the robot for forward commands. If they don't, it's standing.
- **Gait looks like walking:** feet lifting and landing in turn, not sliding or hopping on all four.
- **Steady speed and heading:** no stopping and starting, no drifting sideways when you didn't ask.
- **Body level**, no big tilt or wobble.
- Compare cameras: `side` for the legs, `top` for heading and drift, `track` for an overview.
- Quick numeric check on video: leg motion (frame-difference score) of about 5 to 10 means moving, about 0.2 to 0.5 means standing (from my earlier measurements).

### 5.3 Test grid (all inside the trained range)

| Command (x / y / yaw) | Checks |
|---|---|
| 0 / 0 / 0 | Stands still and stable |
| 1 / 0 / 0 | Forward at a normal speed |
| 0.5 / 0 / 0 | Slower speed |
| 1.5 / 0 / 0 | Top of the range |
| -0.5 / 0 / 0 | Backward |
| 0 / 0.5 / 0 | Sideways |
| 0 / 0 / 1 | Turning in place |
| 1 / 0.5 / 0.5 | Mixed |

Also compare checkpoints on the same command (`ckpt_0`, a middle one, `go1_final`) to see when walking appears.

### 5.4 Log each test

| Run | Steps | Checkpoint | Command | mean track | mean linvel | Upright? | Travels? | Notes |
|---|---|---|---|---|---|---|---|---|

Always record: steps actually run, `num_envs`, `num_evals`, GPU, and which folder the files came from.

---

## 6. Step-count facts (so the log is right)

- One training step = `batch_size × unroll_length × num_minibatches` = 256 × 20 × 32 = 163,840 env steps.
- Each evaluation epoch is rounded up: `ceil(num_timesteps / ((num_evals - 1) × 163,840 × 10)) × 10 × 163,840`.
- Total = `(num_evals - 1)` epochs. Examples seen: `num_evals` 3 and 100M asked gave 101,580,800; `num_evals` 10 and 18M or 25M asked gave about 29.5M.
- So always read the real total from `last step count` in the log, not from `num_timesteps`.

---

## 7. Troubleshooting

| Problem | Likely fix |
|---|---|
| Nothing prints for minutes | It's compiling. Wait up to about 5 minutes. |
| Red out-of-memory error | Lower `num_envs` (4096 to 2048). Must divide 8192. |
| `duplicate session` in tmux | `tmux kill-session -t <name>` and start again. |
| Window closed, run died | Use tmux. Resume from a `ckpt_*` only if you wrote restore code. |
| Overwrote old results | Use one folder per run. Restore from `~/backup_run1`. |
| `device_put_replicated` error | The shim lines near the top of `train_test.py` are missing. |
| Rollout EGL/OpenGL error | Use `osmesa` (section 3). |
| Rollout stops with `RESOURCE_EXHAUSTED` (before `command:` prints) | GPU memory is full. Run `export XLA_PYTHON_CLIENT_PREALLOCATE=false` first (section 1), or add `--no-video`. |
| `plot_motion.py` says file not found | Run `rollout.py` first (it creates the `.npz`) and check the name with `ls motion_*.npz`. |
| `ModuleNotFoundError: matplotlib` | You are not in `go1env`. Run `source ~/go1env/bin/activate`. |
| Constant `iterations limit reached` lines | Normal solver warnings. Hidden by the `grep -v` filter. |
| Videos look the same as an older run | You loaded the same checkpoint. Check the name in the file and the folder. |
| Laptop too hot (above about 90°C) | Stop, cool it, then continue. |

---

## 8. Things not yet verified

- Whether `num_envs` 8192 vs 4096 changes the result.
- Control run done (Test 6): the same setup at about 29.5M steps stands still (`track` 0.0187), so steps are the main driver in my runs (one seed).
- Seed-to-seed variation.
- Yaw, sideways and backward tracking of the 100M policy.
