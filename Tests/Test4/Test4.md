# Test Log 4 — Go1 Baseline Walk (25M steps, 3 camera views)

**Date:** 2026-10-20
**Result:** Fail. Reward fell after its peak. The final policy stays upright but does not walk, and no longer turns continuously.

## Setup

| Setting | Value |
|---|---|
| Task | `Go1JoystickFlatTerrain` |
| `ppo_params.num_timesteps` | 25,000,000 (plot runs to about 29.5M) |
| Rendering | `MUJOCO_GL = "egl"`; cameras `top`, `side`, `track` from one rollout |
| GPU | Not checked |
| Note | First attempt hit the old-Flax error (`jax.core.get_opaque_trace_state`). Fixed by upgrading Flax and restarting the session. |

## Timings

| Stage | Time |
|---|---|
| Compile (JIT) | 1:14 |
| Training | 11:15 |

## Reward

Read off the plot (approximate).

| Env steps | Reward per episode |
|---|---|
| 0 – 3.3M | about 0 |
| about 6.6M | about 3.4 |
| about 9.8M | about 15 |
| about 13M | about 16.5 |
| about 16.4M | about 17.3 |
| about 19.6M | about 16.4 |
| about 22.8M | about 17.7 (peak) |
| about 26.2M | about 13 |
| about 29.5M | about 9.3 |

- The plot title shows `y=9.336`, which matches the end of the line.
- The curve matches the Test 3 rerun up to about 22.5M, so training is repeatable. After the peak it declines.
- The rollout uses the final policy (reward about 9), not the peak one (about 17.7).

## Videos (20 s each, one rollout rendered from 3 cameras)

| Command (x / y / yaw) | Result |
|---|---|
| 0 / 0 / 1 | Turns during the first 2 to 3 s, then holds still. Never falls. |
| 1 / -1 / 1 | Settles in about 1 s, then stands in place. Never falls. |
| 1 / 0 / 1 | Settles in about 1 s, then stands in place. Never falls. |

- Motion after the first few seconds is low in every clip (frame-difference score about 0.2 to 0.45).
- Test 3's yaw clip scored about 4 to 6 the whole way, so the continuous spinning is gone.
- The robot never travels across the floor in any view.
- The command arrow changes with each command, so the commands are being passed in.
- No clip shows the robot walking forward, sideways or diagonally.
- Caveat: "turns then stops" is based on the contact sheet and motion scores, not joint data.

**File problem:** `1 0 1/side.mp4` and `1 0 1/track.mp4` are byte-identical (same checksum). The track clip for that command is a copy, so it was not analysed separately.

## Compared with Test 3 (18M, clean rerun)

| | Test 3 | Test 4 |
|---|---|---|
| Final reward (plot) | about 17.8 | about 9.3 |
| Peak reward | about 17.4 | about 17.7 |
| Yaw = 1 | Spins continuously, about 0.9 rad/s | Turns briefly, then stops |
| x / y commands | No effect | No effect |
| Falls | No | No |

## Takeaway

- Training longer past about 23M made this setup worse. Reward dropped and the policy also lost its continuous turning.
- This is one run (one seed), and the cause is unknown.
- The forward-walking problem is unchanged.
- A 40M run with the same settings is unlikely to help.

**Next:**
- Look at `ppo_params` (learning rate, entropy cost, epochs) and the per-term reward breakdown to see what fell.
- Save intermediate checkpoints so the peak policy (about 23M) can be rendered.
- Plot `linvel`, `track` and `contact` from the rollout.
- Check the training command range and read the reward code.

## Evidence

- [Screenshot](./Screenshot%202026-10-20%20222138.png)
- 0 / 0 / 1: [top](./0%200%201/top.mp4), [side](./0%200%201/side.mp4), [track](./0%200%201/track.mp4)
- 1 / -1 / 1: [top](./1%20-1%201/top.mp4), [side](./1%20-1%201/side.mp4), [track](./1%20-1%201/track.mp4)
- 1 / 0 / 1: [top](./1%200%201/top.mp4), [side](./1%200%201/side.mp4), [track (duplicate of side)](./1%200%201/track.mp4)

## Open questions

- Why reward drops after about 23M steps.
- Why training time is about 11:15 for both the 18M and 25M runs, although the 25M plot covers about 7M more steps.
- Why the plot reaches about 29.5M for a 25M run.
- Whether the policy is deterministic during rollout.
- Whether push perturbations are active during the rollout.
