# Test Log 1 — Go1 Baseline Walk (6M steps)

**Date:** 2026-10-20
**Result:** Not a pass. The robot walks for about 8 s, then falls.

## Setup

| Setting | Value |
|---|---|
| Task | `Go1JoystickFlatTerrain` |
| `ppo_params.num_timesteps` | 6,000,000 (ran about 6.3M) |
| Command | X vel = 1, Y vel = 0, yaw vel = 0 |
| Hardware | Colab, T4 GPU |

## Timings

| Stage | Time |
|---|---|
| Compile (JIT) | 5:15 |
| Training | 7:10 |

## Reward

| Env steps | Reward per episode |
|---|---|
| 0 – 3.3M | about 0 |
| about 4.9M | about 0.65 (peak, very noisy: -0.85 to 2.1) |
| about 6M | about 0.37 |

Reward is low and noisy. It peaked and then dropped.

## Video (20 s)

| Time | What happens |
|---|---|
| 0 – 8 s | Upright and stepping |
| 8.0 – 8.5 s | Falls |
| 8.5 – 20 s | Stays collapsed near the floor |

## Takeaway

6M steps is too short. The policy has learned to step but not to stay up.

**Next:** run 40M steps (about 45 min plus compile).

## Evidence

- [Screenshot](./Screenshot%202026-10-20%20160555.png)
- [Simulation recording](./download.mp4)

## Open questions

- The plot's x-axis seems to go to about 6.6M, but the run is noted as about 6.3M. Check which is right.
- The video details (fall at about 8 s) come from Claude.md. I haven't verified them myself.
