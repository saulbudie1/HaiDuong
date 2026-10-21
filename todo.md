# To do

Newest date first. When a new day starts, add its heading at the top.

---

## 2026-10-21

**Next tests (rollouts only, no training, about 2 minutes each with `--no-video`)**
- [ ] Roll out `ckpt_57344000` and `ckpt_65536000` of the 120M run on 1 / 0 / 0 (where does walking start?)
- [ ] Checkpoint sweep of all 16 checkpoints, plus a small `plot_sweep.py` for `track` against steps
- [ ] Test 5 policy on y = -0.8 and -0.9 (where does it stop following?)
- [ ] 0 / -1 / 0 on both policies (is it y alone, or the combined speed?)
- [ ] 120M policy on y = -1.5 and -2
- [ ] Untested commands on the 120M policy: backward (-0.5 / 0 / 0), sideways (0 / 0.5 / 0), turn in place (0 / 0 / 1), mixed (1 / 0.5 / 0.5)

**Terrain (follow-ups to Test 8)**
- [ ] Rerun the rough training to reach 111M steps (fewer envs, e.g. 2048, to avoid the GPU running out of memory)
- [ ] Test 7 flat policy on all four Test 8 commands on rough terrain (only 1 / 0 / 0 and 1 / -1 / 1 tried)
- [ ] Harder terrain: stairs or larger bumps (stairs scene exists but is not wired up), or a custom heightfield
- [ ] Consider moving the "states to CPU" fix into `Scripts/rollout.py` (it makes video rollouts slower, about 11 min each)

**Heading drift (the slow turn at yaw = 0)**
- [ ] Add a seed option to `rollout.py` and roll out several starting seeds (does the drift follow the sideways command?)
- [ ] Heading-hold controller script (yaw command from the heading error), then a before-and-after trail map
- [ ] 200 s rollout to see whether the path closes into a circle

**Bigger runs**
- [ ] Second seed of the 120M run (about 30 minutes, plug the laptop in)
- [ ] 200M steps, and `num_envs` 8192
- [ ] Print each reward term in the rollout to see what the standing policy earns

**Ideas**
- [ ] Chase mode: a controller that steers the policy toward a moving target (no chase task in Playground)
- [ ] Gait modes (bound, pronk) only exist for Spot, not Go1, so a Go1 version needs a custom task

**Fixes and housekeeping**
- [ ] Rotation graph: line up the zeros of the two vertical axes (angle and rate)
- [ ] Loading line (animated dots) in the next Ubuntu paste
- [ ] Point the git remote at the new repo URL (`HaiDuong___a_Mujoco_Diary`)
- [ ] Delete the unused `side.gif` and `top.gif` in `Tests/Test7/preview/` (3.3 MB)
- [ ] The 50.8M checkpoint rollout (stands still, `track` 0.019) is in WSL `~/go1_test7`, not in the repo yet
- [ ] Short write-up with figures for the prof (limits: one seed per run, "in my runs")

**Done today**
- [x] Test 7: 120M run and diagonal commands
- [x] Test 7.5: Test 5 policy on 1 / -0.5 / 0
- [x] `Scripts/`: train, rollout, `plot_reward.py`, `plot_motion.py`, `plot_trail.py`
- [x] README preview, Test7.md images and trail maps, RunGuide sections 3.1 and 3.2
- [x] Test 8: rough terrain, stopped at 91.75M steps (GPU out of memory), four commands rolled out
- [x] Diary, `TestingAndFinding.md` and `todo.md` updated for Tests 7, 7.5 and 8
