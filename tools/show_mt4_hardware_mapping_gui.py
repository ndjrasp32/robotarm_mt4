from __future__ import annotations

import argparse
from math import degrees
import time

from isaaclab.app import AppLauncher


parser = argparse.ArgumentParser(description="Show the MT4 hardware-facing X/Y/Z/A command mapping in Isaac Sim GUI.")
parser.add_argument("--task", default="Mirobot-Reach-Pregrasp-Direct-v0")
parser.add_argument("--num_envs", type=int, default=1)
parser.add_argument("--move_time", type=float, default=1.0, help="Seconds for each move segment.")
parser.add_argument("--hold_time", type=float, default=0.6, help="Seconds to hold each demonstrated pose.")
parser.add_argument("--settle_time", type=float, default=1.0, help="Seconds to show home pose before moving.")
parser.add_argument("--post_time", type=float, default=3.0, help="Seconds to keep the final home pose visible.")
parser.add_argument(
    "--profile",
    choices=("axis-sweep", "workspace"),
    default="axis-sweep",
    help="'axis-sweep' moves one MT4 SDK field at a time. 'workspace' shows a few combined arm poses.",
)
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()

app_launcher = AppLauncher(args)
simulation_app = app_launcher.app

import gymnasium as gym
import torch

import mirobot_reach_direct  # noqa: F401
from mirobot_reach_direct.mt4_hardware_mapping import SDK_ANGLE_FIELDS, format_mt4_angle_fields
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


def run_for(unwrapped, duration: float, target: torch.Tensor):
    start = time.time()
    while simulation_app.is_running() and time.time() - start < duration:
        write_pose(unwrapped, target)


def interpolate_and_run(unwrapped, start: torch.Tensor, end: torch.Tensor, duration: float):
    start_time = time.time()
    while simulation_app.is_running() and time.time() - start_time < duration:
        alpha = min(max((time.time() - start_time) / max(duration, 1.0e-6), 0.0), 1.0)
        target = (1.0 - alpha) * start + alpha * end
        write_pose(unwrapped, target)


def print_pose(unwrapped, label: str, action_pose: torch.Tensor):
    action_values = [float(value) for value in action_pose[0].detach().cpu()]
    sim_values = [float(value) for value in unwrapped._action_to_sim_joint_pos(action_pose)[0].detach().cpu()]
    action_desc = ", ".join(
        f"{field}/{joint}={value:+.3f} rad ({degrees(value):+.1f} deg)"
        for field, joint, value in zip(SDK_ANGLE_FIELDS, unwrapped.action_joint_names, action_values, strict=False)
    )
    sim_desc = ", ".join(
        f"{joint}={value:+.3f}" for joint, value in zip(unwrapped.sim_joint_names, sim_values, strict=False)
    )
    print(f"[POSE] {label}", flush=True)
    print(f"       SDK command fields: {format_mt4_angle_fields(action_values)}", flush=True)
    print(f"       policy action: {action_desc}", flush=True)
    print(f"       sim targets: {sim_desc}", flush=True)


def run_axis_sweep(unwrapped, home: torch.Tensor, lower: torch.Tensor, upper: torch.Tensor):
    print("[INFO] profile=axis-sweep: X/Y/Z/A move one at a time using URDF/env limits.", flush=True)
    current = home.clone()
    for joint_index, (field, joint_name) in enumerate(
        zip(SDK_ANGLE_FIELDS, unwrapped.action_joint_names, strict=False)
    ):
        low_target = home.clone()
        high_target = home.clone()
        low_target[:, joint_index] = lower[:, joint_index]
        high_target[:, joint_index] = upper[:, joint_index]

        print_pose(unwrapped, f"{field}/{joint_name}: home -> lower", low_target)
        interpolate_and_run(unwrapped, current, low_target, args.move_time)
        run_for(unwrapped, args.hold_time, low_target)

        print_pose(unwrapped, f"{field}/{joint_name}: lower -> upper", high_target)
        interpolate_and_run(unwrapped, low_target, high_target, args.move_time)
        run_for(unwrapped, args.hold_time, high_target)

        print_pose(unwrapped, f"{field}/{joint_name}: upper -> home", home)
        interpolate_and_run(unwrapped, high_target, home, args.move_time)
        run_for(unwrapped, args.hold_time, home)
        current = home.clone()


def run_workspace_profile(unwrapped, home: torch.Tensor, lower: torch.Tensor, upper: torch.Tensor):
    print("[INFO] profile=workspace: combined X/Y/Z/A poses inside the same hardware-facing limits.", flush=True)
    fractions = [
        ("front_mid", (0.50, 0.55, 0.65, 0.50)),
        ("left_reach", (0.30, 0.60, 0.55, 0.30)),
        ("right_reach", (0.70, 0.60, 0.55, 0.70)),
        ("high_pregrasp", (0.50, 0.78, 0.82, 0.50)),
        ("low_pregrasp", (0.50, 0.42, 0.35, 0.50)),
    ]
    current = home.clone()
    span = upper - lower
    for label, pose_fraction in fractions:
        target = lower + span * torch.tensor(pose_fraction, device=home.device).repeat(unwrapped.num_envs, 1)
        print_pose(unwrapped, label, target)
        interpolate_and_run(unwrapped, current, target, args.move_time)
        run_for(unwrapped, args.hold_time, target)
        current = target

    print_pose(unwrapped, "return_home", home)
    interpolate_and_run(unwrapped, current, home, args.move_time)


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
    unwrapped.sim.set_camera_view(eye=[0.52, -0.78, 0.50], target=[0.03, 0.0, 0.18])
    home = unwrapped.action_home_joint_pos.repeat(unwrapped.num_envs, 1)
    lower = unwrapped.action_joint_lower.repeat(unwrapped.num_envs, 1)
    upper = unwrapped.action_joint_upper.repeat(unwrapped.num_envs, 1)

    print("[INFO] MT4 hardware mapping GUI is running.", flush=True)
    print("[INFO] Watch the Isaac Sim GUI, while the terminal prints X/Y/Z/A and sim joint targets.", flush=True)
    print("[INFO] policy action joints:", unwrapped.action_joint_names, flush=True)
    print("[INFO] sim target joints:", unwrapped.sim_joint_names, flush=True)
    for field, joint, lo, hi in zip(
        SDK_ANGLE_FIELDS, unwrapped.action_joint_names, unwrapped.action_joint_lower, unwrapped.action_joint_upper, strict=False
    ):
        print(
            f"[LIMIT] {field}->{joint}: lower={float(lo):+.3f} rad ({degrees(float(lo)):+.1f} deg), "
            f"upper={float(hi):+.3f} rad ({degrees(float(hi)):+.1f} deg)",
            flush=True,
        )

    print_pose(unwrapped, "home", home)
    run_for(unwrapped, args.settle_time, home)

    if args.profile == "axis-sweep":
        run_axis_sweep(unwrapped, home, lower, upper)
    else:
        run_workspace_profile(unwrapped, home, lower, upper)

    run_for(unwrapped, args.post_time, home)
    env.close()
    return 0


try:
    raise SystemExit(main())
finally:
    simulation_app.close()
