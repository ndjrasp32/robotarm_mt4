from __future__ import annotations

from pathlib import Path

import torch

import isaaclab.sim as sim_utils
from isaaclab.actuators import ImplicitActuatorCfg
from isaaclab.assets import Articulation, ArticulationCfg, RigidObject, RigidObjectCfg
from isaaclab.envs import DirectRLEnv, DirectRLEnvCfg
from isaaclab.markers import VisualizationMarkers, VisualizationMarkersCfg
from isaaclab.scene import InteractiveSceneCfg
from isaaclab.utils import configclass
from isaaclab.utils import math as math_utils

from .mt4_hardware_mapping import (
    ACTION_HOME_JOINT_POS,
    ACTION_JOINT_LOWER,
    ACTION_JOINT_NAMES,
    ACTION_JOINT_UPPER,
    PASSIVE_HOME_JOINT_POS,
    SIM_JOINT_NAMES,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MIROBOT_USD_PATH = str(PROJECT_ROOT / "assets/usd/mirobot_real/mt4_from_wlkata_isaac_clean.usd")


@configclass
class MirobotReachPregraspEnvCfg(DirectRLEnvCfg):
    decimation = 2
    episode_length_s = 5.0

    action_space = 4
    observation_space = 29
    state_space = 0

    sim: sim_utils.SimulationCfg = sim_utils.SimulationCfg(
        dt=1 / 120,
        render_interval=decimation,
    )

    scene: InteractiveSceneCfg = InteractiveSceneCfg(
        num_envs=64,
        env_spacing=0.85,
        replicate_physics=True,
    )

    robot_cfg: ArticulationCfg = ArticulationCfg(
        prim_path="/World/envs/env_.*/Robot",
        spawn=sim_utils.UsdFileCfg(
            usd_path=MIROBOT_USD_PATH,
            activate_contact_sensors=False,
            collision_props=sim_utils.CollisionPropertiesCfg(
                collision_enabled=True,
                contact_offset=0.004,
                rest_offset=0.0,
            ),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                disable_gravity=False,
                max_depenetration_velocity=5.0,
            ),
            articulation_props=sim_utils.ArticulationRootPropertiesCfg(
                enabled_self_collisions=False,
                solver_position_iteration_count=8,
                solver_velocity_iteration_count=1,
            ),
        ),
        init_state=ArticulationCfg.InitialStateCfg(
            pos=(0.0, 0.0, 0.0),
            joint_pos={
                "joint_1": 0.0,
                "joint_2_1": 0.35,
                "joint_3": 0.75,
                "joint_4": 0.65,
                "joint_l4": 0.35,
                "gripper_body_joint": 0.0,
                "joint_2_2": 0.35,
            },
        ),
        actuators={
            "arm": ImplicitActuatorCfg(
                joint_names_expr=[
                    "joint_1",
                    "joint_2_1",
                    "joint_3",
                    "joint_4",
                    "joint_l4",
                    "gripper_body_joint",
                    "joint_2_2",
                ],
                stiffness=1800.0,
                damping=220.0,
                effort_limit=800.0,
                velocity_limit=1.5,
            )
        },
    )

    target_cube_cfg: RigidObjectCfg = RigidObjectCfg(
        prim_path="/World/envs/env_.*/TargetCube",
        spawn=sim_utils.CuboidCfg(
            size=(0.044, 0.044, 0.044),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                disable_gravity=True,
                solver_position_iteration_count=16,
                solver_velocity_iteration_count=2,
                max_depenetration_velocity=2.0,
                max_linear_velocity=0.45,
                max_angular_velocity=180.0,
                linear_damping=2.0,
                angular_damping=2.0,
            ),
            collision_props=sim_utils.CollisionPropertiesCfg(
                collision_enabled=True,
                contact_offset=0.004,
                rest_offset=0.0,
            ),
            mass_props=sim_utils.MassPropertiesCfg(mass=0.2),
            physics_material=sim_utils.RigidBodyMaterialCfg(
                static_friction=0.8,
                dynamic_friction=0.6,
                restitution=0.05,
            ),
            visual_material=sim_utils.PreviewSurfaceCfg(
                diffuse_color=(1.0, 0.05, 0.05),
                emissive_color=(0.12, 0.0, 0.0),
            ),
        ),
        init_state=RigidObjectCfg.InitialStateCfg(pos=(0.22, 0.0, 0.12), rot=(1.0, 0.0, 0.0, 0.0)),
    )

    pregrasp_marker_cfg = VisualizationMarkersCfg(
        prim_path="/Visuals/MirobotPregraspTargets",
        markers={
            "pregrasp": sim_utils.SphereCfg(
                radius=0.095,
                visual_material=sim_utils.PreviewSurfaceCfg(
                    diffuse_color=(0.05, 0.25, 1.0),
                    emissive_color=(0.0, 0.03, 0.20),
                    opacity=0.28,
                ),
            ),
        },
    )

    pregrasp_center_marker_cfg = VisualizationMarkersCfg(
        prim_path="/Visuals/MirobotPregraspCenters",
        markers={
            "pregrasp_center": sim_utils.SphereCfg(
                radius=0.012,
                visual_material=sim_utils.PreviewSurfaceCfg(
                    diffuse_color=(0.0, 0.85, 1.0),
                    emissive_color=(0.0, 0.10, 0.35),
                ),
            ),
        },
    )

    success_marker_cfg = VisualizationMarkersCfg(
        prim_path="/Visuals/MirobotReachSuccess",
        markers={
            "success": sim_utils.SphereCfg(
                radius=0.030,
                visual_material=sim_utils.PreviewSurfaceCfg(
                    diffuse_color=(0.05, 1.0, 0.05),
                    emissive_color=(0.0, 0.30, 0.0),
                ),
            ),
        },
    )

    action_scale = 0.035
    success_radius = 0.055
    alignment_success = 0.40

    target_x_range = (0.14, 0.30)
    target_y_range = (-0.15, 0.15)
    target_z_range = (0.08, 0.20)
    min_target_base_radius = 0.13

    ee_body_name = "gripper_body"
    gripper_center_offset_b = (0.055, 0.0, 0.0)
    gripper_forward_axis_b = (1.0, 0.0, 0.0)
    target_radius = 0.038
    min_robot_target_clearance = 0.040

    pregrasp_horizontal_offset = 0.070
    pregrasp_vertical_offset = 0.055
    pregrasp_entry_offset = 0.030
    pregrasp_entry_radius = 0.095

    alignment_weight = 1.2
    pregrasp_weight = 8.0
    pregrasp_entry_weight = 2.5
    target_weight = 1.5
    contact_penalty_weight = 0.0
    action_penalty_weight = 0.012
    joint_velocity_penalty_weight = 0.0004
    time_penalty_weight = 0.003
    success_bonus_weight = 18.0


class MirobotReachPregraspEnv(DirectRLEnv):
    cfg: MirobotReachPregraspEnvCfg

    def __init__(self, cfg: MirobotReachPregraspEnvCfg, render_mode: str | None = None, **kwargs):
        super().__init__(cfg, render_mode, **kwargs)

        # MT4 hardware exposes four arm-angle commands (X/Y/Z/A in the SDK).
        # The CAD URDF contains extra revolute joints for the parallel linkage;
        # those are driven internally here so the policy cannot learn commands
        # that do not exist on the real robot.
        self.action_joint_names = list(ACTION_JOINT_NAMES)
        self.sim_joint_names = list(SIM_JOINT_NAMES)
        self.action_joint_ids, self.action_joint_names_found = self.robot.find_joints(self.action_joint_names)
        self.sim_joint_ids, self.sim_joint_names_found = self.robot.find_joints(self.sim_joint_names)
        self.ee_body_id = self.robot.find_bodies(self.cfg.ee_body_name)[0][0]

        self.action_joint_lower = torch.tensor(ACTION_JOINT_LOWER, device=self.device)
        self.action_joint_upper = torch.tensor(ACTION_JOINT_UPPER, device=self.device)
        self.action_home_joint_pos = torch.tensor(ACTION_HOME_JOINT_POS, device=self.device)
        self.passive_home_joint_pos = torch.tensor(
            [PASSIVE_HOME_JOINT_POS["joint_4"], PASSIVE_HOME_JOINT_POS["joint_l4"]], device=self.device
        )

        self.sim_joint_lower = torch.tensor([-1.57, -1.00, -1.00, 0.00, 0.00, 0.00, -1.57], device=self.device)
        self.sim_joint_upper = torch.tensor([1.57, 1.57, 1.57, 1.57, 1.57, 1.57, 1.57], device=self.device)
        self.sim_home_joint_pos = self._action_to_sim_joint_pos(self.action_home_joint_pos.unsqueeze(0))[0]

        self.actions = torch.zeros((self.num_envs, self.cfg.action_space), device=self.device)
        self.action_joint_targets = self.action_home_joint_pos.repeat(self.num_envs, 1)
        self.sim_joint_targets = self.sim_home_joint_pos.repeat(self.num_envs, 1)

        self.targets = torch.zeros((self.num_envs, 3), device=self.device)
        self.pregrasp_entry_targets = torch.zeros((self.num_envs, 3), device=self.device)
        self.pregrasp_targets = torch.zeros((self.num_envs, 3), device=self.device)
        self.approach_dir = torch.zeros((self.num_envs, 3), device=self.device)
        self.ee_pos = torch.zeros((self.num_envs, 3), device=self.device)
        self.gripper_center_pos = torch.zeros((self.num_envs, 3), device=self.device)
        self.gripper_forward = torch.zeros((self.num_envs, 3), device=self.device)
        self.to_target = torch.zeros((self.num_envs, 3), device=self.device)
        self.to_pregrasp = torch.zeros((self.num_envs, 3), device=self.device)
        self.to_pregrasp_entry = torch.zeros((self.num_envs, 3), device=self.device)
        self.distance = torch.zeros((self.num_envs,), device=self.device)
        self.pregrasp_distance = torch.zeros((self.num_envs,), device=self.device)
        self.pregrasp_entry_distance = torch.zeros((self.num_envs,), device=self.device)
        self.alignment = torch.zeros((self.num_envs,), device=self.device)
        self.target_contact_penalty = torch.zeros((self.num_envs,), device=self.device)

        self.pregrasp_zone_markers = VisualizationMarkers(self.cfg.pregrasp_marker_cfg)
        self.pregrasp_center_markers = VisualizationMarkers(self.cfg.pregrasp_center_marker_cfg)
        self.success_markers = VisualizationMarkers(self.cfg.success_marker_cfg)

        self._sample_targets(torch.arange(self.num_envs, device=self.device))

    def _setup_scene(self):
        self.robot = Articulation(self.cfg.robot_cfg)
        self.scene.articulations["robot"] = self.robot
        self.target_cube = RigidObject(self.cfg.target_cube_cfg)
        self.scene.rigid_objects["target_cube"] = self.target_cube

        ground_cfg = sim_utils.GroundPlaneCfg()
        ground_cfg.func("/World/defaultGroundPlane", ground_cfg)

        light_cfg = sim_utils.DomeLightCfg(intensity=1800.0, color=(0.85, 0.85, 0.85))
        light_cfg.func("/World/Light", light_cfg)

        self.scene.clone_environments(copy_from_source=False)
        self.scene.filter_collisions(global_prim_paths=["/World/defaultGroundPlane"])

    def _pre_physics_step(self, actions: torch.Tensor):
        self.actions = actions.clamp(-1.0, 1.0)
        self.action_joint_targets = self.action_joint_targets + self.cfg.action_scale * self.actions
        self.action_joint_targets = torch.max(
            torch.min(self.action_joint_targets, self.action_joint_upper), self.action_joint_lower
        )
        self.sim_joint_targets = self._action_to_sim_joint_pos(self.action_joint_targets)

    def _apply_action(self):
        self.robot.set_joint_position_target(self.sim_joint_targets, joint_ids=self.sim_joint_ids)

    def _get_observations(self):
        self._compute_intermediate_values()

        joint_pos = self.robot.data.joint_pos[:, self.action_joint_ids]
        joint_vel = self.robot.data.joint_vel[:, self.action_joint_ids]

        obs = torch.cat(
            [
                joint_pos,
                0.1 * joint_vel,
                self.gripper_center_pos,
                self.targets,
                self.pregrasp_targets,
                self.to_pregrasp,
                self.to_target,
                self.gripper_forward,
                self.approach_dir,
            ],
            dim=-1,
        )
        return {"policy": obs}

    def _get_rewards(self):
        self._compute_intermediate_values()

        alignment_reward = torch.clamp(0.5 * (self.alignment + 1.0), min=0.0, max=1.0)
        entry_reward = torch.exp(-90.0 * self.pregrasp_entry_distance * self.pregrasp_entry_distance)
        pregrasp_reward = torch.exp(-120.0 * self.pregrasp_distance * self.pregrasp_distance)
        target_reward = torch.exp(-60.0 * self.distance * self.distance)
        action_penalty = torch.sum(self.actions * self.actions, dim=-1)
        joint_vel = self.robot.data.joint_vel[:, self.action_joint_ids]
        joint_velocity_penalty = torch.sum(joint_vel * joint_vel, dim=-1)
        time_fraction = self.episode_length_buf.float() / max(float(self.max_episode_length), 1.0)

        success = self._success()
        reward = (
            self.cfg.alignment_weight * alignment_reward
            + self.cfg.pregrasp_entry_weight * entry_reward
            + self.cfg.pregrasp_weight * pregrasp_reward * alignment_reward
            + self.cfg.target_weight * target_reward
            + self.cfg.success_bonus_weight * success.float()
            - self.cfg.contact_penalty_weight * self.target_contact_penalty
            - self.cfg.action_penalty_weight * action_penalty
            - self.cfg.joint_velocity_penalty_weight * joint_velocity_penalty
            - self.cfg.time_penalty_weight * time_fraction * (~success).float()
        )
        return reward

    def _get_dones(self):
        self._compute_intermediate_values()

        success = self._success()
        time_out = self.episode_length_buf >= self.max_episode_length - 1
        entry_ready = self.pregrasp_entry_distance < self.cfg.pregrasp_entry_radius
        pregrasp_ready = self.pregrasp_distance < self.cfg.success_radius

        self.extras["log"] = {
            "mirobot/success_rate": success.float().mean(),
            "mirobot/pregrasp_entry_ready_rate": entry_ready.float().mean(),
            "mirobot/pregrasp_ready_rate": pregrasp_ready.float().mean(),
            "mirobot/mean_pregrasp_entry_distance": self.pregrasp_entry_distance.mean(),
            "mirobot/mean_pregrasp_distance": self.pregrasp_distance.mean(),
            "mirobot/mean_target_distance": self.distance.mean(),
            "mirobot/mean_alignment": self.alignment.mean(),
            "mirobot/mean_target_contact_penalty": self.target_contact_penalty.mean(),
            "mirobot/min_pregrasp_distance": self.pregrasp_distance.min(),
        }

        self._update_target_markers(success)
        return success, time_out

    def _reset_idx(self, env_ids: torch.Tensor | None):
        if env_ids is None:
            env_ids = self.robot._ALL_INDICES

        super()._reset_idx(env_ids)
        self.robot.reset(env_ids)
        self.target_cube.reset(env_ids)

        joint_pos = self.robot.data.default_joint_pos[env_ids].clone()
        joint_vel = self.robot.data.default_joint_vel[env_ids].clone()
        joint_pos[:, self.sim_joint_ids] = self.sim_home_joint_pos
        joint_vel[:, self.sim_joint_ids] = 0.0
        self.robot.write_joint_state_to_sim(joint_pos, joint_vel, env_ids=env_ids)

        self.action_joint_targets[env_ids] = self.action_home_joint_pos
        self.sim_joint_targets[env_ids] = self.sim_home_joint_pos
        self._sample_targets(env_ids)

    def _sample_targets(self, env_ids: torch.Tensor):
        n = len(env_ids)
        x = torch.empty(n, device=self.device).uniform_(*self.cfg.target_x_range)
        y = torch.empty(n, device=self.device).uniform_(*self.cfg.target_y_range)
        z = torch.empty(n, device=self.device).uniform_(*self.cfg.target_z_range)

        for _ in range(4):
            radial = torch.sqrt(x * x + y * y)
            too_close = radial < self.cfg.min_target_base_radius
            if not torch.any(too_close):
                break
            count = int(too_close.sum().item())
            x[too_close] = torch.empty(count, device=self.device).uniform_(*self.cfg.target_x_range)
            y[too_close] = torch.empty(count, device=self.device).uniform_(*self.cfg.target_y_range)

        self.targets[env_ids, 0] = x
        self.targets[env_ids, 1] = y
        self.targets[env_ids, 2] = z
        self._write_target_cube_pose(env_ids)
        self._compute_target_geometry(env_ids)
        self._update_target_markers()

    def _write_target_cube_pose(self, env_ids: torch.Tensor):
        root_state = self.target_cube.data.default_root_state[env_ids].clone()
        root_state[:, :3] = self.targets[env_ids] + self.scene.env_origins[env_ids]
        root_state[:, 3:7] = torch.tensor((1.0, 0.0, 0.0, 0.0), device=self.device)
        root_state[:, 7:] = 0.0
        self.target_cube.write_root_state_to_sim(root_state, env_ids=env_ids)

    def _compute_target_geometry(self, env_ids: torch.Tensor | None = None):
        if env_ids is None:
            env_ids = torch.arange(self.num_envs, device=self.device)

        targets = self.targets[env_ids]
        radial_dir = targets.clone()
        radial_dir[:, 2] = 0.0
        fallback = torch.tensor([1.0, 0.0, 0.0], device=self.device).repeat(len(env_ids), 1)
        radial_norm = torch.linalg.norm(radial_dir, dim=-1, keepdim=True)
        radial_dir = torch.where(radial_norm > 1e-6, radial_dir / torch.clamp(radial_norm, min=1e-6), fallback)
        up_dir = torch.tensor([0.0, 0.0, 1.0], device=self.device).repeat(len(env_ids), 1)

        pregrasp_targets = (
            targets
            - self.cfg.pregrasp_horizontal_offset * radial_dir
            + self.cfg.pregrasp_vertical_offset * up_dir
        )
        approach_dir = targets - pregrasp_targets
        approach_dir = approach_dir / torch.clamp(torch.linalg.norm(approach_dir, dim=-1, keepdim=True), min=1e-6)

        self.approach_dir[env_ids] = approach_dir
        self.pregrasp_targets[env_ids] = pregrasp_targets
        self.pregrasp_entry_targets[env_ids] = pregrasp_targets - self.cfg.pregrasp_entry_offset * approach_dir

    def _compute_intermediate_values(self):
        self.targets[:] = self.target_cube.data.root_pos_w - self.scene.env_origins
        self._compute_target_geometry()

        ee_pos_w = self.robot.data.body_pos_w[:, self.ee_body_id, :]
        ee_quat_w = self.robot.data.body_quat_w[:, self.ee_body_id, :]
        self.ee_pos = ee_pos_w - self.scene.env_origins

        center_offset_b = torch.tensor(self.cfg.gripper_center_offset_b, device=self.device).repeat(self.num_envs, 1)
        forward_axis_b = torch.tensor(self.cfg.gripper_forward_axis_b, device=self.device).repeat(self.num_envs, 1)
        self.gripper_center_pos = self.ee_pos + math_utils.quat_apply(ee_quat_w, center_offset_b)
        self.gripper_forward = math_utils.quat_apply(ee_quat_w, forward_axis_b)
        self.gripper_forward = self.gripper_forward / torch.clamp(
            torch.linalg.norm(self.gripper_forward, dim=-1, keepdim=True), min=1e-6
        )

        self.to_target = self.targets - self.gripper_center_pos
        self.to_pregrasp = self.pregrasp_targets - self.gripper_center_pos
        self.to_pregrasp_entry = self.pregrasp_entry_targets - self.gripper_center_pos
        self.distance = torch.linalg.norm(self.to_target, dim=-1)
        self.pregrasp_distance = torch.linalg.norm(self.to_pregrasp, dim=-1)
        self.pregrasp_entry_distance = torch.linalg.norm(self.to_pregrasp_entry, dim=-1)
        self.alignment = torch.sum(self.gripper_forward * self.approach_dir, dim=-1)

        body_pos = self.robot.data.body_pos_w - self.scene.env_origins.unsqueeze(1)
        body_to_target = body_pos - self.targets.unsqueeze(1)
        body_target_distance = torch.linalg.norm(body_to_target, dim=-1)
        body_target_distance[:, self.ee_body_id] = 10.0
        min_body_target_distance = torch.min(body_target_distance, dim=-1).values
        self.target_contact_penalty = torch.clamp(
            self.cfg.min_robot_target_clearance - min_body_target_distance, min=0.0
        )

    def _update_target_markers(self, success: torch.Tensor | None = None):
        if not hasattr(self, "pregrasp_zone_markers"):
            return

        target_pos_w = self.targets + self.scene.env_origins
        pregrasp_pos_w = self.pregrasp_targets + self.scene.env_origins
        self.pregrasp_zone_markers.visualize(pregrasp_pos_w)
        self.pregrasp_center_markers.visualize(pregrasp_pos_w)

        if success is None:
            success = torch.zeros((self.num_envs,), dtype=torch.bool, device=self.device)
        success_pos_w = target_pos_w.clone()
        success_pos_w[~success, 2] = -10.0
        self.success_markers.visualize(success_pos_w)

    def _success(self) -> torch.Tensor:
        return (
            (self.pregrasp_distance < self.cfg.success_radius)
            & (self.alignment > self.cfg.alignment_success)
        )

    def _action_to_sim_joint_pos(self, action_joint_pos: torch.Tensor) -> torch.Tensor:
        joint_1 = action_joint_pos[:, 0:1]
        joint_2_1 = action_joint_pos[:, 1:2]
        joint_2_2 = joint_2_1
        joint_3 = action_joint_pos[:, 2:3]
        joint_4 = torch.full_like(joint_1, self.passive_home_joint_pos[0])
        joint_l4 = torch.full_like(joint_1, self.passive_home_joint_pos[1])
        gripper_body_joint = action_joint_pos[:, 3:4]
        return torch.cat([joint_1, joint_2_1, joint_2_2, joint_3, joint_4, joint_l4, gripper_body_joint], dim=-1)
