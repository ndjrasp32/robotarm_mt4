# 2026-05-16 Mirobot URDF 기반 시작 기록

## 발견한 파일

- 실제 URDF/xacro 후보:
  - `/home/spark-robotics/work/robotarm/mt4_ws/src/complex_mobile_robot_description/urdf/complex_mobile_robot_description.urdf.xacro`
  - `/home/spark-robotics/work/robotarm/generated/mt4_from_wlkata_isaac_clean.urdf`
- Isaac Sim USD 변환 결과:
  - `/home/spark-robotics/work/robotarm/generated/mt4_from_wlkata_isaac_clean/mt4_from_wlkata_isaac_clean.usd`

## URDF 요약

- robot name: `complex_mobile_robot_description`
- links: 8
- joints: 7
- active chain 후보:
  - `joint_1`
  - `joint_2_1`
  - `joint_3`
  - `joint_4`
  - `joint_l4`
  - `gripper_body_joint`
- 보조 parallelogram/link 후보:
  - `joint_2_2`

`joint_2_2`는 첫 task에서는 policy action에는 넣지 않고, `joint_2_1` 목표값을 따라가도록 내부 target에 복제했다.

## 첫 설계

- task name: `Mirobot-Reach-Pregrasp-Direct-v0`
- action: 실제 arm chain 기준 6개 joint position delta
- observation:
  - action joint position/velocity
  - gripper center pose
  - red target / blue pregrasp target
  - target/pregrasp error
  - gripper forward axis / approach direction
- reward:
  - blue pregrasp distance
  - gripper approach alignment
  - red target distance shaping
  - target 조기 접촉/근접 벌점
  - action, joint velocity, time penalty

## 아직 확인할 것

- `gripper_body` local +X가 실제 gripper forward axis인지
- `gripper_center_offset_b = (0.055, 0, 0)`가 실제 집게 중앙과 맞는지
- `joint_2_2`가 `joint_2_1`과 같은 방향으로 따라가야 하는지, 반대 방향/고정이어야 하는지
- 첫 GUI run에서 target range가 실제 작업공간 안에 들어오는지

