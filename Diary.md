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

---

## What I know now

- Reward isn't enough. Standing still can score about 19, and walking scored 26. I have to measure speed and watch the video.
- At about 29.5M steps the robot stands still. At about 100M it walks. (One run each, so I say "in my runs".)
- The Colab notebook wasn't broken. It was just undertrained.
- The step count in the log is the real number, not the setting. Asking for 18M gave 29.5M.

## Still don't know

- Where between 50M and 100M steps walking starts.
- Whether it also walks backward, sideways and turning.
- How much a different random seed changes things.
- Whether more `num_envs` (8192) changes the result.

## Next

1. Test the 100M policy in every direction.
2. Retrain 100M with more checkpoints and plot speed vs steps.
3. A few seeds, then one reward-term experiment.
4. Push recovery, then a short write-up with figures.
