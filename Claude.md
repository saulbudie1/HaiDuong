# HaiDuong: project context for Claude Code

## Goal
Train and evaluate a Unitree Go1 quadruped in simulation (MuJoCo Playground, MJX/Brax PPO) as a personal research project. It supports UREx/UROP applications to NUS robotics labs (Fan Shi, Rajat Talak, Xingyu Liu and others), with Sem 2 registration opening around 21 Dec 2026.

## How to help me (important)
- I want to write the code myself. Guide, explain and review. Don't write the project for me or create files I didn't ask for.
- Explain terms plainly. I'm a Year 1 CDE/EE student and new to RL and Colab.
- Don't invent results. If a number or behaviour isn't in my logs, say it's unknown.
- I'm on Windows (Command Prompt/PowerShell). Training runs on Google Colab (T4 GPU), not locally.

## Setup that works (Colab, Locomotion notebook from google-deepmind/mujoco_playground)
Task: `Go1JoystickFlatTerrain`. Policy input: 48-value `state`. Output: 12 joint targets.
The notebook needed three fixes, in this order, before Train would run:
1. `!pip install -q warp-lang`. The Go1 task uses the Warp backend and the notebook didn't install it.
2. `!pip install -q -U flax`, then Runtime > Restart session. The old Flax called a JAX function removed in JAX 0.11.
3. A shim cell above Train that restores `jax.device_put_replicated` (Brax 0.14.2 still calls it). It rebuilds the function with `Mesh` and `NamedSharding`.
After every restart, rerun the setup cells, the `ppo_params` cell, my `num_timesteps` override, the shim, and the plot-data reset cell (`x_data, y_data, y_dataerr = [], [], []`, `times = [datetime.now()]`). Skip the notebook's "Install MuJoCo Playground" cell.

## Training settings
`num_envs` 8192, default `num_timesteps` 200,000,000 (about 3.8 h on a T4, too long for free Colab). Policy MLP 512-256-128. The value network uses `privileged_state`.

## Results so far
- Short run: `num_timesteps` = 6,000,000, which ran about 6.3M steps.
- Compile (JIT) 5:15, training 7:10 (about 14,600 steps/s).
- Reward per episode: about 0 until ~3.3M steps, about 0.65 near 4.9M (large spread, roughly -0.85 to 2.1), about 0.37 near 6M. Noisy and low.
- 6M policy video (20 s): upright and stepping for about 8 s, falls between roughly 8.0 and 8.5 s, then stays collapsed or near the floor line until the end. Command used: [fill in x/y/yaw values].
- Next: 40M steps (about 45 min plus compile).

## Reward (from Playground source, v0.2.0)
Paid for: `tracking_lin_vel` 1.0, `tracking_ang_vel` 0.5, `pose` 0.5, `feet_air_time` 0.1.
Penalised: `orientation` -5.0, `termination` -1.0, `dof_pos_limits` -1.0, `stand_still` -1.0, `lin_vel_z` -0.5, `feet_clearance` -2.0, `feet_height` -0.2, `feet_slip` -0.1, `ang_vel_xy` -0.05, small torque/energy/action-rate terms.
Trained command range: x up to ±1.5 m/s, y ±0.8, yaw ±1.2 rad/s. Push perturbations exist in `pert_config` but are off by default.

## Plan
1. Baseline walking policy (in progress).
2. Read the reward code, and explain two terms in my own words.
3. Push-recovery test: success rate vs push strength, with a plot.
4. Optional: Handstand as a bonus demo.
5. README, demo video, and 2-3 lines on what broke.

## Repo conventions
Keep large files (videos, weights) out of git (see .gitignore). Credit MuJoCo Playground, MuJoCo, Brax and the Unitree Go1 model (MuJoCo Menagerie, BSD-3).