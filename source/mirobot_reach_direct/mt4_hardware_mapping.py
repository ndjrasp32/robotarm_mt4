from __future__ import annotations

from math import degrees
from typing import Iterable


ACTION_JOINT_NAMES = ("joint_1", "joint_2_1", "joint_3", "gripper_body_joint")
SIM_JOINT_NAMES = (
    "joint_1",
    "joint_2_1",
    "joint_2_2",
    "joint_3",
    "joint_4",
    "joint_l4",
    "gripper_body_joint",
)
SDK_ANGLE_FIELDS = ("X", "Y", "Z", "A")

ACTION_JOINT_LOWER = (-1.57, -1.00, 0.00, -1.57)
ACTION_JOINT_UPPER = (1.57, 1.57, 1.57, 1.57)
ACTION_HOME_JOINT_POS = (0.0, 0.35, 0.75, 0.0)

JOINT_2_2_FOLLOWS = "joint_2_1"
PASSIVE_HOME_JOINT_POS = {
    "joint_4": 0.65,
    "joint_l4": 0.35,
}


def radians_to_sdk_degrees(joint_pos_rad: Iterable[float]) -> dict[str, float]:
    joint_pos = list(joint_pos_rad)
    if len(joint_pos) != len(SDK_ANGLE_FIELDS):
        raise ValueError(f"expected {len(SDK_ANGLE_FIELDS)} policy joints, got {len(joint_pos)}")
    return {field: degrees(value) for field, value in zip(SDK_ANGLE_FIELDS, joint_pos)}


def format_mt4_angle_fields(joint_pos_rad: Iterable[float]) -> str:
    angle_degrees = radians_to_sdk_degrees(joint_pos_rad)
    return " ".join(f"{field}{angle_degrees[field]:.3f}" for field in SDK_ANGLE_FIELDS)
