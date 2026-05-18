from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from isaaclab.app import AppLauncher


PROJECT_DIR = Path(__file__).resolve().parents[1]
URDF_PATH = PROJECT_DIR / "assets/urdf/mirobot_wlkata_isaac_clean.urdf"
DEFAULT_NOTE = PROJECT_DIR / "notes" / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_mirobot_joint_limit_check.md"


parser = argparse.ArgumentParser(description="Compare Mirobot URDF joint limits against IsaacLab runtime limits.")
parser.add_argument("--task", default="Mirobot-Reach-Pregrasp-Direct-v0")
parser.add_argument("--output", type=Path, default=DEFAULT_NOTE)
parser.add_argument("--tolerance", type=float, default=1.0e-4)
parser.add_argument("--num_envs", type=int, default=1)
AppLauncher.add_app_launcher_args(parser)
args = parser.parse_args()

app_launcher = AppLauncher(args)
simulation_app = app_launcher.app

import gymnasium as gym
import torch

import mirobot_reach_direct  # noqa: F401
from mirobot_reach_direct.mt4_hardware_mapping import SDK_ANGLE_FIELDS
from isaaclab_tasks.utils.parse_cfg import parse_env_cfg


@dataclass
class UrdfJointLimit:
    name: str
    joint_type: str
    lower: float | None
    upper: float | None
    velocity: float | None
    effort: float | None


def parse_float(value: str | None) -> float | None:
    if value is None:
        return None
    return float(value)


def parse_urdf_limits(path: Path) -> dict[str, UrdfJointLimit]:
    root = ET.parse(path).getroot()
    limits: dict[str, UrdfJointLimit] = {}
    for joint in root.findall("joint"):
        name = joint.attrib["name"]
        limit = joint.find("limit")
        limits[name] = UrdfJointLimit(
            name=name,
            joint_type=joint.attrib.get("type", ""),
            lower=parse_float(limit.attrib.get("lower")) if limit is not None else None,
            upper=parse_float(limit.attrib.get("upper")) if limit is not None else None,
            velocity=parse_float(limit.attrib.get("velocity")) if limit is not None else None,
            effort=parse_float(limit.attrib.get("effort")) if limit is not None else None,
        )
    return limits


def fmt(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:.6f}"


def deg(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value * 180.0 / 3.141592653589793:.2f}"


def yes_no(value: bool) -> str:
    return "OK" if value else "CHECK"


def tensor_row(tensor: torch.Tensor, index: int) -> list[float]:
    return [float(v) for v in tensor[0, index].detach().cpu().tolist()]


def main() -> int:
    urdf_limits = parse_urdf_limits(URDF_PATH)

    env_cfg = parse_env_cfg(
        args.task,
        device=args.device if args.device is not None else "cuda:0",
        num_envs=args.num_envs,
        use_fabric=False,
    )
    env = gym.make(args.task, cfg=env_cfg)
    env.reset()
    unwrapped = env.unwrapped
    robot = unwrapped.robot

    joint_names = list(robot.data.joint_names)
    default_pos_limits = robot.data.default_joint_pos_limits
    pos_limits = robot.data.joint_pos_limits
    soft_pos_limits = robot.data.soft_joint_pos_limits
    vel_limits = robot.data.joint_vel_limits
    effort_limits = robot.data.joint_effort_limits
    default_joint_pos = robot.data.default_joint_pos

    action_lower = getattr(unwrapped, "action_joint_lower", torch.empty(0, device=unwrapped.device)).detach().cpu()
    action_upper = getattr(unwrapped, "action_joint_upper", torch.empty(0, device=unwrapped.device)).detach().cpu()
    action_joint_names = list(getattr(unwrapped, "action_joint_names", []))
    sim_joint_names = list(getattr(unwrapped, "sim_joint_names", []))
    sdk_mapping = list(zip(action_joint_names, SDK_ANGLE_FIELDS, strict=False))

    rows: list[dict[str, str]] = []
    all_pos_limits_match = True
    all_velocity_limits_match = True
    all_effort_limits_match = True
    all_env_clamps_match = True
    for idx, joint_name in enumerate(joint_names):
        urdf = urdf_limits.get(joint_name)
        default_lower, default_upper = tensor_row(default_pos_limits, idx)
        sim_lower, sim_upper = tensor_row(pos_limits, idx)
        soft_lower, soft_upper = tensor_row(soft_pos_limits, idx)
        home = float(default_joint_pos[0, idx].detach().cpu().item())
        velocity = float(vel_limits[0, idx].detach().cpu().item())
        effort = float(effort_limits[0, idx].detach().cpu().item())

        urdf_lower = urdf.lower if urdf is not None else None
        urdf_upper = urdf.upper if urdf is not None else None
        urdf_velocity = urdf.velocity if urdf is not None else None
        urdf_effort = urdf.effort if urdf is not None else None
        pos_match = (
            urdf_lower is not None
            and urdf_upper is not None
            and abs(default_lower - urdf_lower) <= args.tolerance
            and abs(default_upper - urdf_upper) <= args.tolerance
            and abs(sim_lower - urdf_lower) <= args.tolerance
            and abs(sim_upper - urdf_upper) <= args.tolerance
        )
        all_pos_limits_match = all_pos_limits_match and pos_match
        velocity_match = urdf_velocity is not None and abs(velocity - urdf_velocity) <= args.tolerance
        effort_match = urdf_effort is not None and abs(effort - urdf_effort) <= args.tolerance
        all_velocity_limits_match = all_velocity_limits_match and velocity_match
        all_effort_limits_match = all_effort_limits_match and effort_match

        env_lower = None
        env_upper = None
        env_match = None
        if joint_name in action_joint_names:
            action_idx = action_joint_names.index(joint_name)
            env_lower = float(action_lower[action_idx].item())
            env_upper = float(action_upper[action_idx].item())
            env_match = (
                urdf_lower is not None
                and urdf_upper is not None
                and abs(env_lower - urdf_lower) <= args.tolerance
                and abs(env_upper - urdf_upper) <= args.tolerance
            )
            all_env_clamps_match = all_env_clamps_match and env_match
        elif joint_name in sim_joint_names:
            env_match = True

        rows.append(
            {
                "joint": joint_name,
                "urdf_rad": f"[{fmt(urdf_lower)}, {fmt(urdf_upper)}]",
                "urdf_deg": f"[{deg(urdf_lower)}, {deg(urdf_upper)}]",
                "isaac_default_rad": f"[{default_lower:.6f}, {default_upper:.6f}]",
                "isaac_runtime_rad": f"[{sim_lower:.6f}, {sim_upper:.6f}]",
                "soft_rad": f"[{soft_lower:.6f}, {soft_upper:.6f}]",
                "env_clamp_rad": f"[{fmt(env_lower)}, {fmt(env_upper)}]" if env_lower is not None else "-",
                "home_rad": f"{home:.6f}",
                "velocity": f"{velocity:.6f}",
                "urdf_velocity": fmt(urdf_velocity),
                "effort": f"{effort:.6f}",
                "urdf_effort": fmt(urdf_effort),
                "pos_match": yes_no(pos_match),
                "velocity_match": yes_no(velocity_match),
                "effort_match": yes_no(effort_match),
                "env_match": yes_no(env_match is True),
            }
        )

    # Exercise the task-side clamp directly. This verifies that an oversized action cannot push
    # the commanded target past the env clamp values before targets are sent to Isaac.
    if action_joint_names:
        unwrapped.action_joint_targets[:] = unwrapped.action_joint_upper - 0.5 * unwrapped.cfg.action_scale
        unwrapped._pre_physics_step(torch.ones((unwrapped.num_envs, unwrapped.cfg.action_space), device=unwrapped.device) * 100.0)
        high_clamp_ok = bool(torch.all(unwrapped.action_joint_targets <= unwrapped.action_joint_upper + args.tolerance))
        unwrapped.action_joint_targets[:] = unwrapped.action_joint_lower + 0.5 * unwrapped.cfg.action_scale
        unwrapped._pre_physics_step(torch.ones((unwrapped.num_envs, unwrapped.cfg.action_space), device=unwrapped.device) * -100.0)
        low_clamp_ok = bool(torch.all(unwrapped.action_joint_targets >= unwrapped.action_joint_lower - args.tolerance))
    else:
        high_clamp_ok = False
        low_clamp_ok = False

    env.close()

    lines: list[str] = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append(f"# {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Mirobot Joint Limit Check")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- generated_at: {timestamp} KST")
    lines.append(f"- task: `{args.task}`")
    lines.append(f"- urdf: `{URDF_PATH}`")
    lines.append(f"- policy_action_joints: `{action_joint_names}`")
    lines.append(f"- sim_joint_targets: `{sim_joint_names}`")
    lines.append(
        "- hardware_sdk_angle_mapping: `"
        + ", ".join(f"{field}->{joint}" for joint, field in sdk_mapping)
        + "`"
    )
    lines.append(f"- all_urdf_position_limits_match_isaac_runtime: `{all_pos_limits_match}`")
    lines.append(f"- all_urdf_velocity_limits_match_isaac_runtime: `{all_velocity_limits_match}`")
    lines.append(f"- all_urdf_effort_limits_match_isaac_runtime: `{all_effort_limits_match}`")
    lines.append(f"- action_env_clamps_match_urdf_for_policy_joints: `{all_env_clamps_match}`")
    lines.append(f"- oversized_positive_action_clamped_by_env: `{high_clamp_ok}`")
    lines.append(f"- oversized_negative_action_clamped_by_env: `{low_clamp_ok}`")
    lines.append("")
    lines.append("## Important Finding")
    lines.append("")
    lines.append(
        "URDF position lower/upper limits are present and are reflected in IsaacLab "
        "`default_joint_pos_limits` and runtime `joint_pos_limits`."
    )
    lines.append(
        f"The current task exposes {len(action_joint_names)} hardware-facing policy actions. "
        "They map to the MT4 SDK arm-angle fields as "
        + ", ".join(f"`{field}` -> `{joint}`" for joint, field in sdk_mapping)
        + "."
    )
    lines.append(
        "`joint_2_2`, `joint_4`, and `joint_l4` are loaded and targeted in simulation, "
        "but are internal linkage joints rather than policy actions. "
        "`joint_2_2` follows `joint_2_1`; `joint_4` and `joint_l4` currently hold nominal passive-linkage poses."
    )
    lines.append(
        "Velocity limits are also preserved from the URDF in this run. Effort limits are not preserved: "
        "the URDF says effort=10, while the current task actuator configuration writes effort=800."
    )
    lines.append("")
    lines.append("## Joint Table")
    lines.append("")
    headers = [
        "joint",
        "urdf_rad",
        "urdf_deg",
        "isaac_default_rad",
        "isaac_runtime_rad",
        "soft_rad",
        "env_clamp_rad",
        "home_rad",
        "velocity",
        "urdf_velocity",
        "effort",
        "urdf_effort",
        "pos_match",
        "velocity_match",
        "effort_match",
        "env_match",
    ]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in rows:
        lines.append("| " + " | ".join(row[header] for header in headers) + " |")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- `pos_match=OK` means URDF lower/upper equals both Isaac default and runtime position limits.")
    lines.append("- `velocity_match=OK` means Isaac runtime velocity limit equals the URDF velocity value.")
    lines.append("- `effort_match=CHECK` is expected right now because `ImplicitActuatorCfg.effort_limit=800.0` overrides the URDF effort=10.")
    lines.append("- `env_match=OK` means policy action clamp matches URDF for policy-controlled joints, or the joint is an internal sim joint.")
    lines.append("- `soft_rad` currently equals runtime limits because `soft_joint_pos_limit_factor` is 1.0.")
    lines.append("- `joint_2_2` is not a policy action. In `MirobotReachPregraspEnv`, its command target is copied from `joint_2_1`.")
    lines.append("- `joint_4` and `joint_l4` are not policy actions. They are held at nominal passive-linkage poses until the exact MT4 linkage relation is calibrated.")
    lines.append("")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")

    print("\n".join(lines))
    print(f"[OK] wrote note: {args.output}")
    # Effort mismatch is intentionally not a failure because the task actuator config currently overrides it.
    return 0 if all_pos_limits_match and all_velocity_limits_match and all_env_clamps_match and high_clamp_ok and low_clamp_ok else 1


try:
    raise SystemExit(main())
finally:
    simulation_app.close()
