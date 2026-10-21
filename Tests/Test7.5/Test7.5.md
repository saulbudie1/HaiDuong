# Test Log 7.5 — Test 5 policy on a sideways command (about 101.6M steps, local RTX 5060)

**Date:** 2026-10-21
**Result:** The Test 5 policy walks 1 / -0.5 / 0 (`track` 0.935) but stood still at 1 / -1 / 0 (`track` 0.0004). The range, not sideways walking, is the likelier cause.

**Purpose:** In [Test 7](../Test7/Test7.md) the Test 5 policy stood still on 1 / -1 / 0, while the new 120M policy walked it. y = -1 is outside the trained range (±0.8), but I had not tried the Test 5 policy on any in-range sideways command. So the failure could have been about the range, or about sideways walking in general. This test separates the two.

## Setup

| Setting | Value |
|---|---|
| Policy | Test 5 `go1_final` (101.6M steps, `num_evals` 3, `num_envs` 4096) |
| Training | None. It is a rollout of the existing policy. The file was checked identical to the original in `~/backup_run1`. |
| Hardware | NVIDIA GeForce RTX 5060 Laptop (8 GB), WSL2 Ubuntu 24.04 |
| Rollout | `rollout.py`, folder `~/go1_test7`, 20 s, `PRNGKey(0)`, deterministic policy |
| Commands (x / y / yaw) | 1 / 0 / 0 (control), **1 / -0.5 / 0 (this test)**, 1 / -1 / 0 (from Test 7) |

Only the command changes between the three rows, so any difference comes from the command.

## Rollout numbers (Test 5 policy, 20 s)

| Command | mean `track` | mean `linvel` x, y, z (body frame) | Distance from start | Yaw turned |
|---|---|---|---|---|
| 1 / 0 / 0 | 0.941 | 0.963, 0.010, 0.018 | 19.2 m | -13.5° |
| **1 / -0.5 / 0** | **0.935** | 0.958, -0.447, 0.012 | 21.1 m | -16.6° |
| 1 / -1 / 0 | 0.0004 | 0.004, -0.003, 0.002 | 0.09 m | +7.7° |

- At y = -0.5 it walks forward and right at about the commanded speed. y is -0.447 against -0.5, and x is 0.958 against 1.
- At y = -1 it stands still and the speed is about 0.
- The mean z is a little higher than the 120M policy's (0.012 against about 0.004), meaning a little more bobbing. It is close to this policy's own 1 / 0 / 0 value (0.018).

### Against the 120M policy from Test 7

| Command | Test 5 policy `track` | 120M policy `track` |
|---|---|---|
| 1 / 0 / 0 | 0.941 | 0.942 |
| 1 / -0.5 / 0 | 0.935 | 0.953 |
| 1 / -1 / 0 | 0.0004 | 0.932 |

Both policies handle the in-range commands about equally. They differ only at y = -1.

## Videos (20 s each, 3 cameras)

- Made for 1 / -0.5 / 0 and 1 / -1 / 0. The control was run with `--no-video`.
- I did not watch these videos. The motion graphs and the numbers above are what the claims rest on.

## Takeaway

- In my runs, the Test 5 policy follows an in-range sideways command and fails when y is outside the trained range (±0.8). This fits the idea that out-of-range commands are not blocked but are an input the policy never trained on.
- The 120M policy extrapolated to y = -1 anyway. So two policies, two outcomes, on the same out-of-range command.
- It is not proven. Only y = -0.5 and y = -1 were tried, so the failure could start anywhere between them, and it could be partly about the combined speed (about 1.41 m/s), not y alone. Both are one training run each (one seed).

## Open questions

- Where between y = -0.5 and -1 does the Test 5 policy stop following? Try -0.7, -0.8 and -0.9.
- Is the failure about y alone, or the combined speed? Try 0 / -1 / 0 and 0.5 / -1 / 0.
- Do other seeds and checkpoints behave the same way?

## Next

1. Roll out the Test 5 policy on y = -0.8 and -0.9 (`--no-video`, about 2 minutes each).
2. Roll out 0 / -1 / 0 on both policies.
3. Second seed of the 120M run (see Test 7).

## Evidence

- Control (1 / 0 / 0) motion graph: [motion_x1.0_y0.0_yaw0.0_go1_final.png](./motion_x1.0_y0.0_yaw0.0_go1_final.png)
- 1 / -0.5 / 0: [motion graph](./x1.0_y-0.5_yaw0.0/motion_x1.0_y-0.5_yaw0.0_go1_final.png), [side](./x1.0_y-0.5_yaw0.0/side_x1.0_y-0.5_yaw0.0_go1_final.mp4), [top](./x1.0_y-0.5_yaw0.0/top_x1.0_y-0.5_yaw0.0_go1_final.mp4), [track](./x1.0_y-0.5_yaw0.0/track_x1.0_y-0.5_yaw0.0_go1_final.mp4)
- 1 / -1 / 0: [motion graph](./x1.0_y-1.0_yaw0.0/motion_x1.0_y-1.0_yaw0.0_go1_final.png), [side](./x1.0_y-1.0_yaw0.0/side_x1.0_y-1.0_yaw0.0_go1_final.mp4), [top](./x1.0_y-1.0_yaw0.0/top_x1.0_y-1.0_yaw0.0_go1_final.mp4), [track](./x1.0_y-1.0_yaw0.0/track_x1.0_y-1.0_yaw0.0_go1_final.mp4)
- Training log of the Test 5 policy: `run1.log` (in WSL `~/go1_test7` and `~/backup_run1`, not copied here)
