from __future__ import annotations

import argparse
import time

from isaaclab.app import AppLauncher


parser = argparse.ArgumentParser(description="Show the Mirobot arm moving into and pushing the dynamic red cube.")
parser.add_argument("--task", default="Mirobot-Reach-Pregrasp-Direct-v0")
parser.add_argument("--body_name", default="link_2", help="Robot body whose sweep path is used for the push demo.")
parser.add_argument("--cycles", type=int, default=3)
parser.add_argument("--settle_time", type=float, default=1.0)
parser.add_argument("--move_time", type=float, default=3.0)
parser.add_argument("--hold_time", type=float, default=1.0)
parser.add_argument("--post_time", type=float, default=8.0)
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()

app_launcher = AppLauncher(args)
simulation_app = app_launcher.app

import gymnasium as gym
import torch

import mirobot_reach_direct  # noqa: F401
from isaaclab_tasks.utils.parse_cfg import parse_env_cfg


START_POSE = (-0.75, 0.35, 0.75, 0.0)
END_POSE = (0.75, 0.35, 0.75, 0.0)


def update_markers(unwrapped):
    unwrapped._compute_intermediate_values()
    unwrapped._update_target_markers()


def write_action_pose(unwrapped, action_pose: torch.Tensor, render: bool = True):
    sim_joint_pos = unwrapped._action_to_sim_joint_pos(action_pose)
    joint_pos = unwrapped.robot.data.joint_pos.clone()
    joint_vel = torch.zeros_like(unwrapped.robot.data.joint_vel)
    joint_pos[:, unwrapped.sim_joint_ids] = sim_joint_pos

    unwrapped.action_joint_targets[:] = action_pose
    unwrapped.sim_joint_targets[:] = sim_joint_pos
    unwrapped.robot.write_joint_state_to_sim(joint_pos, joint_vel)
    unwrapped.robot.set_joint_position_target(sim_joint_pos, joint_ids=unwrapped.sim_joint_ids)
    unwrapped.scene.write_data_to_sim()
    unwrapped.sim.step(render=render)
    unwrapped.scene.update(dt=unwrapped.physics_dt)
    update_markers(unwrapped)


def step_hold(unwrapped, action_pose: torch.Tensor, duration: float):
    start = time.time()
    while simulation_app.is_running() and time.time() - start < duration:
        write_action_pose(unwrapped, action_pose)


def interpolate_pose(unwrapped, start_pose: torch.Tensor, end_pose: torch.Tensor, duration: float):
    start_time = time.time()
    while simulation_app.is_running() and time.time() - start_time < duration:
        alpha = min(max((time.time() - start_time) / max(duration, 1.0e-6), 0.0), 1.0)
        action_pose = (1.0 - alpha) * start_pose + alpha * end_pose
        write_action_pose(unwrapped, action_pose)


def set_cube_pose(unwrapped, pos_env: torch.Tensor):
    root_state = unwrapped.target_cube.data.default_root_state[:1].clone()
    root_state[:, :3] = pos_env.unsqueeze(0) + unwrapped.scene.env_origins[:1]
    root_state[:, 3:7] = torch.tensor((1.0, 0.0, 0.0, 0.0), device=unwrapped.device)
    root_state[:, 7:] = 0.0
    unwrapped.target_cube.write_root_state_to_sim(root_state, env_ids=torch.tensor([0], device=unwrapped.device))
    update_markers(unwrapped)


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
    unwrapped.sim.set_camera_view(eye=[0.42, -0.56, 0.42], target=[0.04, 0.02, 0.19])
    body_id = unwrapped.robot.find_bodies(args.body_name)[0][0]
    start_pose = torch.tensor(START_POSE, device=unwrapped.device).repeat(1, 1)
    end_pose = torch.tensor(END_POSE, device=unwrapped.device).repeat(1, 1)

    print("[INFO] Dynamic cube contact GUI is running.", flush=True)
    print("[INFO] The robot arm moves through the red cube; blue sphere follows the guide zone.", flush=True)
    print(f"[INFO] Sweep demo body: {args.body_name}", flush=True)

    for cycle in range(args.cycles):
        if not simulation_app.is_running():
            break

        env.reset()
        write_action_pose(unwrapped, start_pose)
        start_body_pos = unwrapped.robot.data.body_pos_w[0, body_id] - unwrapped.scene.env_origins[0]
        write_action_pose(unwrapped, end_pose)
        end_body_pos = unwrapped.robot.data.body_pos_w[0, body_id] - unwrapped.scene.env_origins[0]

        cube_pos = 0.58 * start_body_pos + 0.42 * end_body_pos
        cube_pos[2] = 0.5 * (start_body_pos[2] + end_body_pos[2])
        set_cube_pose(unwrapped, cube_pos)
        write_action_pose(unwrapped, start_pose)
        before = unwrapped.target_cube.data.root_pos_w[:1].clone()

        print(f"[CYCLE {cycle + 1}] cube placed on {args.body_name} sweep path: {cube_pos.detach().cpu().tolist()}", flush=True)
        print(f"[CYCLE {cycle + 1}] moving robot arm into cube", flush=True)
        step_hold(unwrapped, start_pose, args.settle_time)
        interpolate_pose(unwrapped, start_pose, end_pose, args.move_time)
        step_hold(unwrapped, end_pose, args.hold_time)

        after = unwrapped.target_cube.data.root_pos_w[:1].clone()
        delta = torch.linalg.norm(after - before, dim=-1)
        print(f"[CYCLE {cycle + 1}] cube displacement after robot push: {float(delta[0]):.4f} m", flush=True)

    step_hold(unwrapped, end_pose, args.post_time)
    env.close()
    return 0


try:
    raise SystemExit(main())
finally:
    simulation_app.close()
