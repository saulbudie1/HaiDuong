# Test Log 2 — Go1 Baseline Walk (18M steps)

**Date:** 2026-10-20
**Result:** Partial. Stays upright for the full 20 s but barely moves.

## Setup

| Setting | Value |
|---|---|
| Task | `Go1JoystickFlatTerrain` |
| `ppo_params.num_timesteps` | 18,000,000 |
| Command | X vel = 1, Y vel = 0, yaw vel = 0 |
| How it was run | Same session as Test 1. Only the changed cells were rerun (no restart). |
| GPU | Not checked |

## Timings

| Stage | Time |
|---|---|
| Compile (JIT) | 0:00:59 |
| Training | 11:38 |

## Reward

| Env steps | Reward per episode |
|---|---|
| 0 – 3.3M | about 0 |
| about 6.5M | about 0.4 |
| about 9.8M | about 2.1 |
| about 13M | about 3.1 |
| about 16.4M | about 2.75 |
| about 19.6M | about 3.0 |
| about 22.5M | about 3.3 |

- The plot title shows `y=2.440`.
- The error bars are wide (about -2 to 8), so reward is still noisy.
- The curve flattens out after about 13M steps.
- The plot's x-axis ends at about 22.5M, which is more than 18M. Not explained.

## Video (20 s)

| Time | What happens |
|---|---|
| 0 – 1 s | Settles into a stance |
| 1 – 20 s | Stays upright, almost no movement |

- It never falls.
- The robot stays in the same spot. The floor grid shifts by less than 1 pixel.

## Compared with Test 1

| | Test 1 (6M) | Test 2 (18M) |
|---|---|---|
| Peak reward | about 0.65 | about 3.3 |
| Falls | Yes, at about 8 s | No |
| Walks forward | Briefly | No (stands in place) |

## Takeaway

More training fixed the falling. It did not teach the robot to follow the speed command. It may be getting reward for staying upright without moving, but this is a guess.

**Next:** try `x_vel` = 0.5 and 1.5 (inside the trained range), then a longer run (40M).

## Evidence

- [Screenshot](./Screenshot%202026-10-20%20164442.png)
- [Simulation recording](./download.mp4)

## Open questions

- Why the plot reaches about 22.5M steps for an 18M run.
- Why training was faster than Test 1 (11:38 for more steps, JIT 0:59 vs 5:15). Possibly a different GPU or cached compile.
