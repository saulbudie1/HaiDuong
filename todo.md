# To do

Newest date first. When a new day starts, add its heading at the top.

---

## 2026-10-22

**Message Fan Shi (target: Oct 28 to 29), one small step each**
- [ ] Roll out `go1_final` of seeds 2 to 5 on 1 / 0 / 0 with `--no-video` (about 6 minutes) to confirm they walk
- [ ] Roll out seeds 2 to 5 at the checkpoints between 45M and 70M (does the switch land in the same window?)
- [ ] Make one figure: `track` against steps for the seeds, with reward on the same axes
- [ ] Write Test9.md (setup, seed table, the seed 1 collapse, "in my runs" wording)
- [ ] Check his lab page and the UROP/UREx listing: takes first-years? deadline? how to apply?
- [ ] Read the paper's perception parts (local navigation section, Fig. 2 and Fig. 5) and write down 2 questions
- [ ] Be able to explain each figure myself: what `track` is, what a seed is, why the switch is sudden
- [ ] Draft the email (5 to 7 lines): who I am, repo link, one figure, one finding with its limits, one real link to his paper, one small ask
- [ ] Have Claude review the draft, then cut it under 150 words
- [ ] Open the repo front page and check that the README, links and Test9 read well
- [ ] Send the email and note the date in the diary
- [ ] If no reply after 7 days, send one short follow-up

**Test 9 follow-ups (flat ground, seeds 1 to 5)**
- [ ] Roll out `go1_final` of seeds 2 to 5 on 1 / 0 / 0 (do they walk? the reward says probably)
- [ ] Roll out the checkpoints between 45M and 70M of seeds 2 to 5 (does the switch land in the same window?)
- [ ] Rerun seed 1 with 31 evaluations, and one other seed with 60 (is the collapse the seed, or the 60-evaluation schedule?)
- [ ] Video of seed 1 at its peak (about 26M) and at the end, to see what the collapsed robot does
- [ ] Fast sweep script that loads many checkpoints in one process (compile once), then `plot_sweep.py` with all seeds on one graph
- [ ] Write Test9.md, and one clip for the README preview (Test 9 is a whole number, so the preview switches)

**Accessories (render only, weightless)**
- [ ] Create 3 accessories (I model the STL files): a **pumpkin head** (about 0.14 m wide), a **cone birthday hat** (about 0.10 m base, 0.15 m tall) and a **backpack** (about 0.16 × 0.14 × 0.10 m, on the back)
- [ ] All three must be weightless and must not change the movement: visual only (no mass, no collisions), in a render-only copy of the model, so training and rollouts are untouched
- [ ] Modelling rules: metres, origin at the base of each piece, +x towards the nose, +z up, low poly, binary STL, one file per colour
- [ ] Test each on a rollout, and check that the legs do not visually poke through the backpack

**Vision (from the paper, arXiv 2410.03076)**
- [ ] Read the rest of the paper (the PDF is in `Reference/`, which git ignores) and write down questions for the lab
- [ ] Idea: a small depth or height-map input for the Go1. MJX has ray casting (`mjx.ray`); Playground's Go1 does not use it

**Done today**
- [x] Test 9: five seeds on flat ground (seed 1 with 60 evaluations collapsed; seeds 2 to 5 look like Test 7)
- [x] Checkpoint sweep of the Test 7 run: walking starts between 57.3M and 65.5M
- [x] Looked at the paper's vision part (a low-resolution simulated depth input)
- [x] Diary, findings and todo updated

---

## 2026-10-21

**Next tests (rollouts only, no training, about 2 minutes each with `--no-video`)**
- [x] Roll out `ckpt_57344000` and `ckpt_65536000` of the 120M run on 1 / 0 / 0: stands at 57.3M (`track` 0.019), walks at 65.5M (0.79)
- [x] Checkpoint sweep of all 16 checkpoints of the 120M run (results in the findings)
- [ ] Small `plot_sweep.py` for `track` against steps (see the 2026-10-22 list for the all-seed version)
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
- [x] More seeds: Test 9 trained seeds 1 to 5 (about 20 minutes each)
- [ ] 200M steps, and `num_envs` 8192
- [ ] Print each reward term in the rollout to see what the standing policy earns

**Ideas**
- [ ] The 3 accessories (pumpkin head, cone birthday hat, backpack) are in the 2026-10-22 list above (see TestingAndFinding, "How the Go1 model is built")
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
