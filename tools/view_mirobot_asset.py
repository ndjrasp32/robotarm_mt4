from __future__ import annotations

import argparse
import time

from isaaclab.app import AppLauncher


parser = argparse.ArgumentParser(description="Open the Mirobot IsaacLab asset in the Isaac Sim GUI.")
parser.add_argument("--task", default="Mirobot-Reach-Pregrasp-Direct-v0")
parser.add_argument("--num_envs", type=int, default=1)
parser.add_argument("--duration", type=float, default=300.0, help="Viewer lifetime in seconds.")
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()

app_launcher = AppLauncher(args)
simulation_app = app_launcher.app

import gymnasium as gym
import torch

import mirobot_reach_direct  # noqa: F401
from isaaclab_tasks.utils.parse_cfg import parse_env_cfg


def main() -> int:
    env_cfg = parse_env_cfg(
        args.task,
        device=args.device if args.device is not None else "cuda:0",
        num_envs=args.num_envs,
        use_fabric=False,
    )
    env = gym.make(args.task, cfg=env_cfg)
    env.reset()

    unwrapped = env.unwrapped
    actions = torch.zeros((unwrapped.num_envs, unwrapped.cfg.action_space), device=unwrapped.device)

    print("[INFO] Mirobot GUI viewer is running.")
    print("[INFO] task:", args.task)
    print("[INFO] duration:", args.duration)
    print("[INFO] action joints:", getattr(unwrapped, "action_joint_names_found", []))
    print("[INFO] sim joints:", getattr(unwrapped, "sim_joint_names_found", []))
    print("[INFO] ee body:", unwrapped.cfg.ee_body_name)

    start = time.time()
    while simulation_app.is_running() and time.time() - start < args.duration:
        env.step(actions)

    env.close()
    return 0


try:
    raise SystemExit(main())
finally:
    simulation_app.close()

