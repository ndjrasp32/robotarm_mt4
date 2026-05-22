from __future__ import annotations

import argparse
import time

from isaaclab.app import AppLauncher


TASK_BY_MISSION = {
    "pick": "Mirobot-Mars-Twin-Pick-Direct-v0",
    "place": "Mirobot-Mars-Twin-Place-Direct-v0",
    "stack": "Mirobot-Mars-Twin-Stack-Direct-v0",
    "push": "Mirobot-Mars-Twin-Push-Direct-v0",
    "pull": "Mirobot-Mars-Twin-Pull-Direct-v0",
}


parser = argparse.ArgumentParser(description="Open the MT4 Mars rover digital twin in Isaac Lab.")
parser.add_argument("--mission", choices=sorted(TASK_BY_MISSION), default="push")
parser.add_argument("--task", default=None, help="Override the Gym task id.")
parser.add_argument("--num_envs", type=int, default=1)
parser.add_argument("--duration", type=float, default=120.0)
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()

app_launcher = AppLauncher(args)
simulation_app = app_launcher.app

import gymnasium as gym
import torch

import mirobot_reach_direct  # noqa: F401
from isaaclab_tasks.utils.parse_cfg import parse_env_cfg


def main() -> int:
    task = args.task if args.task is not None else TASK_BY_MISSION[args.mission]
    env_cfg = parse_env_cfg(
        task,
        device=args.device if args.device is not None else "cuda:0",
        num_envs=args.num_envs,
        use_fabric=False,
    )
    env_cfg.episode_length_s = max(args.duration, 1.0)
    env = gym.make(task, cfg=env_cfg)
    env.reset()

    unwrapped = env.unwrapped
    unwrapped.sim.set_camera_view(eye=[0.48, -0.58, 0.40], target=[0.14, 0.02, 0.10])

    print(f"[INFO] Running {task}", flush=True)
    print("[INFO] Green marker is the mission goal. Yellow marker is a home-pose reference.", flush=True)
    print("[INFO] Zero actions hold the calibrated home pose so object gravity/contact can be checked first.", flush=True)

    actions = torch.zeros((args.num_envs, unwrapped.cfg.action_space), device=unwrapped.device)
    start = time.time()
    while simulation_app.is_running() and time.time() - start < args.duration:
        env.step(actions)

    env.close()
    return 0


try:
    raise SystemExit(main())
finally:
    simulation_app.close()
