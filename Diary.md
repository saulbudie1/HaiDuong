# Diary

The short version of [`TestingAndFinding.md`](TestingAndFinding.md). Plain words, only the numbers that matter.

---

## Oct 20 — I first used Colab for simulation.
**Background**I haven't used colab in ages (not since that deepfake video where you can input a photo to make it sing). So I spent the afternoon refamiliarizing with the website.

**Test 1 (6M steps).** The robot took a few steps for about 8 seconds, then fell over. It was about 6million steps that is too little training.

**Test 2 (18M).** Reran only the cells I changed. The robot stayed up but stood still, and the reward looked low and strange. Probably leftover settings from my last test (a guess, not proven).

**Test 3 (18M, clean restart).** Reward jumped to 17 to 19. It looked promisng but the render result disappointed me. the robot stood still when I told it to go forward(x_vel = 1.0), and only spun on the spot when I told it to turn(yaw_vel=1.0). 

**Test 4 (25M).** Same standing robot, and the reward dropped late in training. I decided "more steps makes it worse". That was wrong.

**Late night.** I read the notebook code and found the plot cuts off the data. My "18M" and "25M" runs both really ran about 29.5M steps. Then Colab ran out of compute while I was trying 100M.

---

## Oct 21 — Laptop integration and the first walking not talking

**Switch to Ubuntu.** I installed Ubuntu inside Windows (WSL2), Claude guided my way to get my RTX 5060 working with JAX and Warp, and moved training off Colab. The laptop ran about twice as fast as Colab's free GPU.

**Test 5 (100M steps).** About 19 minutes to train. Reward went to 26, and this time the robot **walked**: I asked for 1 m/s at direction x and it moved at about 0.96 m/s(which is close enough). So concludes the first real walking motion.

**Test 6 (control).** I needed to know the walking came from the extra steps, not from migrating to Ubuntu and the laptop. So I redid the Colab-length run (18M in the file and about 29.5M steps in the terminal) on the laptop. It stood still, just like Tests 3 and 4. So the platform wasn't the cause.

**Test 7 (120M, diagonals).** A new training run. I asked for 120M and it ran 122.9M steps (30 minutes, 16 checkpoints), and the reward ended at 26.9. It sat near 19 from 25M to 57M steps (the standing level), then climbed. I rolled the final policy out on four commands: straight (1 / 0 / 0) and three diagonals (sideways speed 0.5, -0.5 and -1). All four followed the command (`track` 0.93 to 0.95). Even sideways -1, which is outside the range it trained on (up to 0.8).

**The laptop died.** I left it running the rollouts and the battery ran out. The training had already finished and saved, so I only redid the rollouts, not the 30 minutes. Plug in before leaving.

**Test 7.5 (the odd one out).** In Test 7 the new policy walked sideways -1, but the Test 5 policy had stood still on that command. So I tried the Test 5 policy on -0.5: it walked (`track` 0.935). It can walk sideways, so the failure at -1 most likely comes from that command being out of range. Not proven, because the two runs also differ in seed, steps and evaluations.

**It still turns a little.** With the turn command at 0 the robot slowly rotated, -36 degrees over 20 seconds on the -1 diagonal. The turn command is a rate, not a heading, the reward barely notices a tiny rate, and the policy has no heading input. So it is expected, not broken. A fix would be a controller outside the policy, not retraining.

**Tools.** I put the scripts in `Scripts/`: train, rollout (it now saves the motion data), reward plot, motion graphs (distance, velocity against the command, rotation) and a bird's-eye trail map. I also looked for a chase mode. MuJoCo Playground has none, and the gait choices (bound, pace, pronk) exist for the Spot robot, not the Go1.

**Test 8 (rough terrain).** The first different ground: a bumpy rock patch. I asked for 110M steps, but the GPU ran out of memory at about 24 minutes, after 91.75M steps (82% of the plan), so the run stopped early. The checkpoints were saved, so I used the last one. The reward reached 24.1 and was still rising. The robot followed all four commands I tried: straight (`track` 0.93), the -1 diagonal (0.82), the diagonal while turning (0.91) and a slow diagonal with a fast spin of 3 (0.85). With a turn of 1 it walked three laps of a circle about 2.8 m wide. With a turn of 3, far beyond the 1.2 it trained on, it spun about nine laps of a circle about 0.5 m wide.

**Things that broke.** My first rollouts for the two circling commands crashed, because saving every step for the video filled the GPU. Moving each step to the CPU fixed it, at a cost of about 11 minutes per video. The rough patch is only 20 m wide, so a robot walking straight reaches the edge after 7 to 13 seconds. I stop the rollout there. My time guess for the training (1.5 hours) was also too high, because it ran at about 66k steps per second.

---

## What I know now

- Reward isn't enough. Standing still can score about 19, and walking scored 26. I have to measure speed and watch the video.
- At about 29.5M steps the robot stands still. At about 100M it walks. (One run each, so I say "in my runs".)
- The Colab notebook wasn't broken. It was just undertrained.
- The step count in the log is the real number, not the setting. Asking for 18M gave 29.5M.
- Walking sideways and diagonally works when the command is inside the trained range (both policies).
- A command outside the range is not blocked. One policy followed it and one did not (two runs, so not a rule).
- The robot drifts in heading a little, because the turn command is a rate. The tilt is a limit of this kind of policy, not a bug.
- On rough ground the robot still followed every command I tried, even a turn of 3 (one run, stopped at 82%).
- A video rollout can run out of GPU memory. Moving each saved step to the CPU fixes it.

## Still don't know

- Whether walking starts around 57M to 66M steps (the reward climbs there). Needs those checkpoints rolled out.
- Whether it walks backward and turns in place (the diagonals work).
- How much a different random seed changes things, and whether the drift following the sideways command is real.
- Whether more `num_envs` (8192) changes the result.
- Whether the full 111M steps on rough ground would change the result (the reward was still rising), and why the GPU ran out of memory at epoch 14.

## Next

See [`todo.md`](todo.md) for the running list.
