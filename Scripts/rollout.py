import os
os.environ["MUJOCO_GL"] = "egl"   # must be set before mujoco is imported

import sys
import jax
import jax.numpy as jp
import mujoco
import mediapy as media
from brax.io import model
from brax.training.acme import running_statistics
from brax.training.agents.ppo import networks as ppo_networks
from mujoco_playground import registry
from mujoco_playground.config import locomotion_params

# command and checkpoint: python rollout.py <x> <y> <yaw> [checkpoint]
x_vel, y_vel, yaw_vel = (float(a) for a in sys.argv[1:4])
ckpt = sys.argv[4] if len(sys.argv) > 4 else "go1_final"

env_name = "Go1JoystickFlatTerrain"
env = registry.load(env_name)
env_cfg = registry.get_default_config(env_name)
ppo_params = locomotion_params.brax_ppo_config(env_name)

# rebuild the policy network the same way training did, then load the saved weights
network = ppo_networks.make_ppo_networks(
    env.observation_size, env.action_size,
    preprocess_observations_fn=running_statistics.normalize,
    **ppo_params.network_factory,
)
make_inference_fn = ppo_networks.make_inference_fn(network)
params = model.load_params(ckpt)
inference_fn = jax.jit(make_inference_fn(params, deterministic=True))

jit_reset = jax.jit(env.reset)
jit_step = jax.jit(env.step)

command = jp.array([x_vel, y_vel, yaw_vel])
rng = jax.random.PRNGKey(0)
state = jit_reset(rng)
state.info["command"] = command

rollout, track, linvel = [], [], []
for _ in range(env_cfg.episode_length):
    act_rng, rng = jax.random.split(rng)
    ctrl, _ = inference_fn(state.obs, act_rng)
    state = jit_step(state, ctrl)
    state.info["command"] = command
    rollout.append(state)
    v = env.get_local_linvel(state.data)
    linvel.append(v)
    track.append(env._reward_tracking_lin_vel(command, v))

print("command:", x_vel, y_vel, yaw_vel)
print("mean track:", float(sum(track) / len(track)))
print("mean linvel (body frame):", sum(linvel) / len(linvel))

scene_option = mujoco.MjvOption()
scene_option.geomgroup[2] = True
scene_option.geomgroup[3] = False
scene_option.flags[mujoco.mjtVisFlag.mjVIS_CONTACTPOINT] = True
scene_option.flags[mujoco.mjtVisFlag.mjVIS_TRANSPARENT] = False

render_every = 2
fps = 1.0 / env.dt / render_every
traj = rollout[::render_every]
for cam in ["top", "side", "track"]:
    frames = env.render(traj, camera=cam, scene_option=scene_option, width=640, height=480)
    media.write_video(f"{cam}_x{x_vel}_y{y_vel}_yaw{yaw_vel}_{ckpt}.mp4", frames, fps=fps)
    del frames
print("done")
