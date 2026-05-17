from __future__ import annotations

import argparse
import time

from isaaclab.app import AppLauncher


parser = argparse.ArgumentParser(description="Sweep each Mirobot joint to its env lower/upper limits in the GUI.")
parser.add_argument("--task", default="Mirobot-Reach-Pregrasp-Direct-v0")
parser.add_argument("--num_envs", type=int, default=1)
parser.add_argument("--move_time", type=float, default=0.9, help="Seconds for each move segment.")
parser.add_argument("--hold_time", type=float, default=0.35, help="Seconds to hold each limit pose.")
parser.add_argument("--settle_time", type=float, default=1.0, help="Seconds to show home pose before sweeping.")
parser.add_argument("--post_time", type=float, default=2.0, help="Seconds to keep the final home pose visible.")
parser.add_argument(
    "--mode",
    choices=("full", "upper"),
    default="full",
    help="'full' sweeps lower and upper. 'upper' shows each joint's maximum angle only.",
)
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()

app_launcher = AppLauncher(args)
simulation_app = app_launcher.app

import gymnasium as gym
import torch

import mirobot_reach_direct  # noqa: F401
from isaaclab_tasks.utils.parse_cfg import parse_env_cfg


def write_pose(unwrapped, action_joint_pos: torch.Tensor):
    sim_joint_pos = unwrapped._action_to_sim_joint_pos(action_joint_pos)
    joint_pos = unwrapped.robot.data.joint_pos.clone()
    joint_vel = torch.zeros_like(unwrapped.robot.data.joint_vel)
    joint_pos[:, unwrapped.sim_joint_ids] = sim_joint_pos

    unwrapped.action_joint_targets[:] = action_joint_pos
    unwrapped.sim_joint_targets[:] = sim_joint_pos
    unwrapped.robot.write_joint_state_to_sim(joint_pos, joint_vel)
    unwrapped.robot.set_joint_position_target(sim_joint_pos, joint_ids=unwrapped.sim_joint_ids)
    unwrapped.scene.write_data_to_sim()
    unwrapped.sim.step(render=True)
    unwrapped.scene.update(dt=unwrapped.physics_dt)


def run_for(env, unwrapped, duration: float, target: torch.Tensor):
    start = time.time()
    while simulation_app.is_running() and time.time() - start < duration:
        write_pose(unwrapped, target)


def interpolate_and_run(env, unwrapped, start: torch.Tensor, end: torch.Tensor, duration: float):
    start_time = time.time()
    while simulation_app.is_running() and time.time() - start_time < duration:
        alpha = min(max((time.time() - start_time) / max(duration, 1.0e-6), 0.0), 1.0)
        target = (1.0 - alpha) * start + alpha * end
        write_pose(unwrapped, target)


def main() -> int:
    env_cfg = parse_env_cfg(
        args.task,
        device=args.device if args.device is not None else "cuda:0",
        num_envs=args.num_envs,
        use_fabric=False,
    )
    env_cfg.episode_length_s = 600.0
    env = gym.make(args.task, cfg=env_cfg)
    env.reset()

    unwrapped = env.unwrapped
    unwrapped.sim.set_camera_view(eye=[0.48, -0.74, 0.48], target=[0.02, 0.0, 0.17])
    home = unwrapped.action_home_joint_pos.repeat(unwrapped.num_envs, 1)
    lower = unwrapped.action_joint_lower.repeat(unwrapped.num_envs, 1)
    upper = unwrapped.action_joint_upper.repeat(unwrapped.num_envs, 1)

    print("[INFO] Mirobot joint limit sweep is running.", flush=True)
    if args.mode == "upper":
        print("[INFO] Watch the GUI. Each policy joint moves home -> upper(max) -> home.", flush=True)
    else:
        print("[INFO] Watch the GUI. Each policy joint moves lower -> upper -> home.", flush=True)
    print("[INFO] policy joints:", unwrapped.action_joint_names, flush=True)
    for name, lo, hi in zip(unwrapped.action_joint_names, unwrapped.action_joint_lower, unwrapped.action_joint_upper):
        print(f"[INFO] {name}: lower={float(lo): .3f} rad upper={float(hi): .3f} rad", flush=True)

    run_for(env, unwrapped, args.settle_time, home)

    current = home.clone()
    for joint_index, joint_name in enumerate(unwrapped.action_joint_names):
        high_target = home.clone()
        high_target[:, joint_index] = upper[:, joint_index]

        if args.mode == "full":
            low_target = home.clone()
            low_target[:, joint_index] = lower[:, joint_index]
            print(f"[SWEEP] {joint_name}: home -> lower", flush=True)
            interpolate_and_run(env, unwrapped, current, low_target, args.move_time)
            run_for(env, unwrapped, args.hold_time, low_target)

            print(f"[SWEEP] {joint_name}: lower -> upper(max)", flush=True)
            interpolate_and_run(env, unwrapped, low_target, high_target, args.move_time)
        else:
            print(f"[SWEEP] {joint_name}: home -> upper(max)", flush=True)
            interpolate_and_run(env, unwrapped, current, high_target, args.move_time)
        run_for(env, unwrapped, args.hold_time, high_target)

        print(f"[SWEEP] {joint_name}: upper(max) -> home", flush=True)
        interpolate_and_run(env, unwrapped, high_target, home, args.move_time)
        run_for(env, unwrapped, args.hold_time, home)
        current = home.clone()

    run_for(env, unwrapped, args.post_time, home)
    env.close()
    return 0


try:
    raise SystemExit(main())
finally:
    simulation_app.close()
