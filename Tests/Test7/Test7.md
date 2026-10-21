# Test Log 7 — Diagonal commands (about 123M steps, local RTX 5060)

**Date:** 2026-10-21
**Result:** Pass. The policy walks forward and sideways together, including 1 / -1 / 0, which is outside the trained y range.

**Purpose:** New training run at about 120M steps with more evaluation points. Then roll it out on diagonal commands (forward plus left or right) to see whether it tracks them, and to see whether the 100M policy from Test 5 stood still on 1 / -1 / 0 because of the policy or the command.

## Setup

| Setting | Value |
|---|---|
| Task | `Go1JoystickFlatTerrain` (default config, domain randomization on) |
| `ppo_params.num_timesteps` | 120,000,000 |
| `ppo_params.num_evals` | 16 |
| **Steps actually run** | **122,880,000** (15 epochs of 8,192,000) |
| `num_envs` | 4096 |
| Hardware | NVIDIA GeForce RTX 5060 Laptop (8 GB), WSL2 Ubuntu 24.04 |
| Run | `train_test.py` in `~/go1_test8`, log `run8.log`, 16 checkpoints (every 8.2M steps) |
| Rollout | `rollout.py`, checkpoint `go1_final`, 20 s, commands below |

`num_evals` 16 was picked so the real total lands close to 120M (see RunGuide section 6). Asking for 120M with `num_evals` 20 would have run 124.5M.

## Timings

| Stage | Time |
|---|---|
| Compile (JIT) | 0:00:59 |
| Training | 0:29:31 |
| Total | 0:30:30 |
| Speed | about 69,000 steps/s |

Slower than Test 5 (about 92,000 steps/s), probably because this run has more evaluations. Test 6 saw the same slowdown.

## Reward (from `run8.log`)

| Env steps | Reward per episode |
|---|---|
| 0 | 0.001 |
| 8,192,000 | 8.332 |
| 16,384,000 | 16.898 |
| 24,576,000 | 19.284 |
| 49,152,000 | 19.186 |
| 57,344,000 | 20.082 |
| 65,536,000 | 22.410 |
| 73,728,000 | 24.411 |
| 98,304,000 | 26.697 |
| 106,496,000 | 26.961 |
| 122,880,000 | 26.936 |

Reward sits at about 19 from 25M to 57M steps (the level of the standing policies in Tests 5 and 6), climbs from about 57M to 100M, then flattens at about 27. Test 5 reached 26.2 at 101.6M. Only the 25M to 57M part looks like a standing level, and I did not roll out those checkpoints, so this is a hint and not a result.

## Rollout numbers (go1_final, 20 s)

| Command (x / y / yaw) | mean `track` | mean `linvel` x, y, z (body frame) | Distance from start | Yaw turned |
|---|---|---|---|---|
| 1 / 0 / 0 | 0.942 | 0.943, -0.003, 0.003 | 18.8 m | -16.6° |
| 1 / 0.5 / 0 | 0.943 | 0.965, 0.464, 0.005 | 21.2 m | +21.1° |
| 1 / -0.5 / 0 | 0.953 | 0.955, -0.477, 0.004 | 21.2 m | -19.7° |
| 1 / -1 / 0 | 0.932 | 0.950, -0.930, 0.005 | 26.0 m | -36.4° |

- The velocity matches the command in every row: x about 0.95 and y within about 0.07 of the command.
- Heading drifts a little in all four (yaw is commanded 0), and most at 1 / -1 / 0 (-36° over 20 s).
- +y is left in this simulator, so 0.5 is forward-left and -0.5 and -1 are forward-right.

### 1 / -1 / 0 against the Test 5 policy

| Policy | mean `track` | mean `linvel` x, y | Distance from start |
|---|---|---|---|
| Test 5 (101.6M, `num_evals` 3) | 0.0004 | 0.004, -0.003 | 0.09 m |
| This run (122.9M, `num_evals` 16) | 0.932 | 0.950, -0.930 | 26.0 m |

The Test 5 row is from a rollout in WSL (`~/go1_test7`) that is not copied here. The trained y range is ±0.8 (`command_config.a = [1.5, 0.8, 1.2]`), so y = -1 is outside it. I did not roll out the Test 5 policy on any in-range sideways command, so I do not know whether its failure comes from the range or from sideways walking in general.

## Videos (20 s each, 3 cameras)

- Made for the three diagonal commands. The control (1 / 0 / 0) was run with `--no-video`.
- I looked at 8-frame contact sheets (2.5 s apart) of the three 1 / -1 / 0 videos only. The other videos are not watched.
- Robot upright in every frame. The legs are in a different pose each frame, which fits stepping. The floor grid and lighting move past the tracking camera, so it travels.
- 2.5 s between frames is too coarse to see sliding or hopping, so gait quality is not checked.
- The README preview gifs are 6 s clips (2 s to 8 s) of the 1 / -1 / 0 videos.

## Takeaway

- In this run, the policy follows forward-left and forward-right diagonals at about the commanded speed (`track` 0.93 to 0.95).
- It also follows y = -1, outside the trained range. Out-of-range commands are not blocked, since the policy only receives them as an input it never trained on. It can extrapolate or fail.
- The Test 5 policy failed on that command. The two runs differ in steps, seed and `num_evals`, so I cannot say which matters.
- This is one training run (one seed). The wording should be "in my runs".

## Open questions

- Does the Test 5 policy walk an in-range sideways command (1 / -0.5 / 0)? That separates "range" from "sideways in general".
- Where does the 120M policy stop following y (try -1.5 and -2)?
- Is the 1 / -1 / 0 result typical, or lucky? Needs a second seed.
- Where between 49M and 66M does walking appear? Rolling out `ckpt_57344000` and `ckpt_65536000` would show.
- Gait quality (sliding, hopping) and the extra yaw drift at 1 / -1 / 0.

## Next

1. Roll out the Test 5 checkpoint on 1 / -0.5 / 0.
2. Roll out `ckpt_57344000` and `ckpt_65536000` of this run on 1 / 0 / 0.
3. Roll out this run on y = -1.5 and -2.
4. Second seed at the same settings.

## Evidence

- Reward graph: [reward_plot.png](./reward_plot.png)
- Training log: [run8.log](./run8.log), rollout numbers: [results.txt](./results.txt)
- Motion graph of the control: [motion_x1.0_y0.0_yaw0.0_go1_final.png](./motion_x1.0_y0.0_yaw0.0_go1_final.png)
- 1 / 0.5 / 0: [motion graph](./x1.0_y0.5_yaw0.0/motion_x1.0_y0.5_yaw0.0_go1_final.png), [side](./x1.0_y0.5_yaw0.0/side_x1.0_y0.5_yaw0.0_go1_final.mp4), [top](./x1.0_y0.5_yaw0.0/top_x1.0_y0.5_yaw0.0_go1_final.mp4), [track](./x1.0_y0.5_yaw0.0/track_x1.0_y0.5_yaw0.0_go1_final.mp4)
- 1 / -0.5 / 0: [motion graph](./x1.0_y-0.5_yaw0.0/motion_x1.0_y-0.5_yaw0.0_go1_final.png), [side](./x1.0_y-0.5_yaw0.0/side_x1.0_y-0.5_yaw0.0_go1_final.mp4), [top](./x1.0_y-0.5_yaw0.0/top_x1.0_y-0.5_yaw0.0_go1_final.mp4), [track](./x1.0_y-0.5_yaw0.0/track_x1.0_y-0.5_yaw0.0_go1_final.mp4)
- 1 / -1 / 0: [motion graph](./x1.0_y-1.0_yaw0.0/motion_x1.0_y-1.0_yaw0.0_go1_final.png), [side](./x1.0_y-1.0_yaw0.0/side_x1.0_y-1.0_yaw0.0_go1_final.mp4), [top](./x1.0_y-1.0_yaw0.0/top_x1.0_y-1.0_yaw0.0_go1_final.mp4), [track](./x1.0_y-1.0_yaw0.0/track_x1.0_y-1.0_yaw0.0_go1_final.mp4)
- Checkpoints: WSL `~/go1_test8`, not copied here
