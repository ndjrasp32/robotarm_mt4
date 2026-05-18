from __future__ import annotations

import argparse
import time

from isaaclab.app import AppLauncher


parser = argparse.ArgumentParser(description="Show the dynamic red cube being pushed by Mirobot link collision.")
parser.add_argument("--task", default="Mirobot-Reach-Pregrasp-Direct-v0")
parser.add_argument("--body_name", default="link_2", help="Robot body to place the cube against for contact demo.")
parser.add_argument("--cycles", type=int, default=3)
parser.add_argument("--settle_time", type=float, default=1.0)
parser.add_argument("--contact_time", type=float, default=2.5)
parser.add_argument("--post_time", type=float, default=8.0)
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()

app_launcher = AppLauncher(args)
simulation_app = app_launcher.app

import gymnasium as gym
import torch

import mirobot_reach_direct  # noqa: F401
from isaaclab_tasks.utils.parse_cfg import parse_env_cfg


def step_zero(env, unwrapped, duration: float):
    action = torch.zeros((unwrapped.num_envs, unwrapped.cfg.action_space), device=unwrapped.device)
    start = time.time()
    while simulation_app.is_running() and time.time() - start < duration:
        env.step(action)


def set_cube_pose(unwrapped, pos_env: torch.Tensor):
    root_state = unwrapped.target_cube.data.default_root_state[:1].clone()
    root_state[:, :3] = pos_env.unsqueeze(0) + unwrapped.scene.env_origins[:1]
    root_state[:, 3:7] = torch.tensor((1.0, 0.0, 0.0, 0.0), device=unwrapped.device)
    root_state[:, 7:] = 0.0
    unwrapped.target_cube.write_root_state_to_sim(root_state, env_ids=torch.tensor([0], device=unwrapped.device))


def main() -> int:
    env_cfg = parse_env_cfg(
        args.task,
        device=args.device if args.device is not None else "cuda:0",
        num_envs=1,
        use_fabric=False,
    )
    env_cfg.episode_length_s = 600.0
    env = gym.make(args.task, cfg=env_cfg)
    env.reset()

    unwrapped = env.unwrapped
    unwrapped.sim.set_camera_view(eye=[0.44, -0.62, 0.42], target=[0.03, 0.02, 0.16])
    body_id = unwrapped.robot.find_bodies(args.body_name)[0][0]

    print("[INFO] Dynamic cube contact GUI is running.", flush=True)
    print("[INFO] Red cube is a dynamic rigid object; blue sphere is the guide zone.", flush=True)
    print(f"[INFO] Contact demo body: {args.body_name}", flush=True)

    for cycle in range(args.cycles):
        if not simulation_app.is_running():
            break

        print(f"[CYCLE {cycle + 1}] showing sampled cube target", flush=True)
        step_zero(env, unwrapped, args.settle_time)

        body_pos_env = unwrapped.robot.data.body_pos_w[0, body_id] - unwrapped.scene.env_origins[0]
        set_cube_pose(unwrapped, body_pos_env)
        before = unwrapped.target_cube.data.root_pos_w[:1].clone()
        print(f"[CYCLE {cycle + 1}] cube placed at {args.body_name}: {body_pos_env.detach().cpu().tolist()}", flush=True)

        step_zero(env, unwrapped, args.contact_time)

        after = unwrapped.target_cube.data.root_pos_w[:1].clone()
        delta = torch.linalg.norm(after - before, dim=-1)
        print(f"[CYCLE {cycle + 1}] cube displacement after contact: {float(delta[0]):.4f} m", flush=True)

        env.reset()

    step_zero(env, unwrapped, args.post_time)
    env.close()
    return 0


try:
    raise SystemExit(main())
finally:
    simulation_app.close()
