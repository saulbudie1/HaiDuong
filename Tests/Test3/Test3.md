# Test Log 3 — Go1 Baseline Walk (18M steps, clean rerun)

**Date:** 2026-10-20
**Result:** Fail. High reward, but the robot ignores the forward command. It turns in place when told to.

## Setup

| Setting | Value |
|---|---|
| Task | `Go1JoystickFlatTerrain` |
| `ppo_params.num_timesteps` | 18,000,000 |
| How it was run | Fresh session, all cells rerun |
| Rendering | `MUJOCO_GL = "egl"` set before importing `mujoco` |
| GPU | Not checked |

## Timings

| Run | JIT | Training |
|---|---|---|
| First attempt (session crashed while rendering) | 1:14 | 11:36 |
| Rerun | 1:11 | 11:17 |

## Reward

Rerun, read off the plot (approximate). The saved screenshot is assumed to be this run.

| Env steps | Reward per episode |
|---|---|
| 0 – 3.3M | about 0 |
| about 6.5M | about 3.5 |
| about 9.8M | about 15 |
| about 13M | about 16.5 |
| about 16.4M | about 17.4 (peak) |
| about 19.6M | about 16.4 |
| about 22.5M | about 17.8 |

- The plot title shows `y=19.284`.
- Error bars are wide (about 10 to 23 at later points).
- The first attempt peaked at about 16.3, dropped to about 6 at about 20M, and ended near 13 (title `y=17.562`). The rerun is smoother.
- The x-axis ends at about 22.5M for an 18M run, same as Test 2. Not explained.

## Videos (20 s each)

| File | Command | What happens |
|---|---|---|
| `download.mp4` | X = 1, Y = 0, yaw = 0 | Stays upright, stands in place |
| `test3 x1_49 y 0 yaw 0.mp4` | X = 1.49, Y = 0, yaw = 0 | Stays upright, stands in place |
| `test3 yaw_vel 1.mp4` | X = 0, Y = 0, yaw = 1 | Steps and turns in place, no falls |
| `test3 x 0.3.mp4` | X = 0.3, Y = 0, yaw = 0 | Stands in place |
| `test3 xvel -0.5.mp4` | X = -0.5, Y = 0, yaw = 0 | Stands in place |
| `y vel 0.8.mp4` | X = 0, Y = 0.8, yaw = 0 | Stands in place |
| `x vel 1 y vel 1.mp4` | X = 1, Y = 1, yaw = 0 | Stands in place |
| `x vel 1 y vel -1 yaw vel 1.mp4` | X = 1, Y = -1, yaw = 1 | Steps and spins in place, no falls |

Only the two videos with a yaw command show real leg motion (frame-difference score about 3.5 to 6). The other six are about 0.2 to 0.5, with the robot in the same spot.

**Extra command tests (x 0.3, x -0.5, y 0.8, x 1 y 1, x 1 y -1 yaw 1)**
- Forward, backward, sideways and diagonal commands have no visible effect. The robot just stands.
- With yaw added (X = 1, Y = -1, yaw = 1), it spins in place. It does not travel, and the floor grid stays put.
- The command arrow rotates with the robot's heading, so the command is displayed relative to the robot's body.
- My floor-shift measurement showed about the same offset in every video, including the standing ones. I treated it as a measurement bias and ignored it.

**X = 1.49 video**
- The robot never falls and never moves across the floor. The floor grid shifts by less than 1 px.
- Motion levels and floor shift are almost the same as the X = 1 video, so the policy does not seem to respond to the forward command.
- The command arrow is about 1.5 times longer than in the Test 2 video, so the higher command was being passed to the display.

**Yaw video**
- The heading rotates through the clip and repeats about every 10 s (rough estimate from frames 2 s apart).
- Leg motion is much higher than in the standing videos, about 4 to 6 vs about 0.25 (frame-difference score).
- It stays in the same spot on the floor.

## Compared with Test 1 and Test 2

| | Test 1 (6M) | Test 2 (18M) | Test 3 (18M) |
|---|---|---|---|
| Peak reward | about 0.65 | about 3.3 | about 17.4 |
| Falls | Yes, at about 8 s | No | No |
| Walks forward | Briefly | No | No |
| Turns in place | Not tested | Not tested | Yes |

## Takeaway

- The command reaches the policy, since yaw works through the same rollout code.
- The policy learned to stay up and to turn. It does not respond to forward, backward or sideways commands, alone or combined (7 command combinations tested). Yaw wins when combined with x and y.
- Reward is much higher than Test 2, so Test 2 was probably affected by leftover state from the shared session. This is a guess.

**Next:**
- Backward, sideways, diagonal and slow forward are now tested (see above). None work.
- Print the command range used in training and check that x is covered.
- Read the reward code, then consider a longer run (40M).

## Evidence

- [Screenshot](./Screenshot%202026-10-20%20172818.png)
- [X = 1 recording](./download.mp4)
- [X = 1.49 recording](./test3%20x1_49%20y%200%20yaw%200.mp4)
- [Yaw = 1 recording](./test3%20yaw_vel%201.mp4)
- [X = 0.3 recording](./test3%20x%200.3.mp4)
- [X = -0.5 recording](./test3%20xvel%20-0.5.mp4)
- [Y = 0.8 recording](./y%20vel%200.8.mp4)
- [X = 1, Y = 1 recording](./x%20vel%201%20y%20vel%201.mp4)
- [X = 1, Y = -1, yaw = 1 recording](./x%20vel%201%20y%20vel%20-1%20yaw%20vel%201.mp4)

## Open questions

- Why the policy ignores x and y commands while following yaw.
- Whether training commands cover forward speeds (not checked).
- Why the plot reaches about 22.5M steps for an 18M run.
- Which run the saved screenshot is from.
