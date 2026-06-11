# 2026-05-18 MT4 dynamic cube target 설정 기록

Date: 2026-05-18 13:44:55 KST

## 목적

The first manipulation objective is no longer a pure visual reach target. Since the gripper/tool model is separate from the current arm URDF, the environment now needs a physical object that can be pushed by any robot link. This gives us a useful intermediate stage before modeling a real gripper.

## 변경 사항

- Replaced the red target sphere marker with a real dynamic rigid object:
  - Asset name: `target_cube`
  - Prim path: `/World/envs/env_.*/TargetCube`
  - Shape: red cuboid, `0.044 m` per side
  - Mass: `0.05 kg`
  - Collision enabled
  - Contact offset: `0.004 m`
  - Rest offset: `0.0 m`
- Added explicit collision properties to the robot USD spawn so robot links and the cube participate in PhysX contact solving.
- Kept the policy observation size at `29`.
- The target position in observations is now read from the cube's current simulated root position, so if contact pushes the cube, the policy sees the updated object position.
- Converted the blue pregrasp marker into a translucent guide area with radius `0.095 m`.
- Kept a small cyan center marker inside the guide area.
- Removed the old non-end-effector contact penalty from reward shaping by setting `contact_penalty_weight = 0.0`; touching the cube is now allowed instead of punished.

## 현재 물리 설정

The cube is dynamic and collidable, but gravity is disabled for this intermediate stage. That keeps the object inside the existing reach workspace instead of letting it fall before contact. The next more realistic object-manipulation stage should add a table/support surface and turn cube gravity back on.

## 검증

Headless environment check:

```bash
export PYTHONPATH=/home/spark-robotics/work/robotarm/robotarm_mt4/source:${PYTHONPATH:-}
unset CMEEL_PREFIX
export TERM=xterm-256color
/home/spark-robotics/work/isaac/src/IsaacLab/isaaclab.sh -p -c "<env reset and 8 zero-action steps>"
```

Result:

- Reset succeeded.
- Observation shape: `torch.Size([2, 29])`
- Eight simulation steps completed without error.
- Reward tensor returned normally.

Overlap/contact sanity check:

- The cube was placed at the current gripper/body region and the sim was stepped for 30 frames.
- Cube displacement after solver contact/depenetration: `0.0181 m`
- This confirms the cube is participating in contact resolution instead of acting as a pass-through visual marker.
