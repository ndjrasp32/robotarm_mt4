# 2026-06-08 MT4 dual Pi camera perception 계획

## 배경

실제 MT4 기기 학습과 hardware-transfer 판단은 `robotarm_mt4`에서 관리한다. `robotarm_student`는 학생용 simulation curriculum과 실험 archive로 고정한다.

현재 MT4/Mars twin 환경은 simulation에서 target position을 내부 좌표로 observation에 직접 제공할 수 있다. 이 방식은 baseline 비교에는 유용하지만, 실제 로봇팔에서는 목표 지점과 높이를 카메라로 추정해야 하므로 hardware-transfer 기준으로는 부족하다.

## 결정

Pi Camera 두 대 구성을 perception baseline으로 둔다.

- body/front camera: 로봇팔 몸통 전면에 고정하고 작업 공간 전체와 목표 물체를 관찰한다.
- wrist/downward camera: 집게 끝 근처에 장착하고 아래쪽을 향하게 해 grasp 직전의 상대 위치, 높이, 접촉 후보 영역을 관찰한다.

## 학습 전환 순서

1. 내부 target 좌표를 쓰는 기존 Isaac baseline을 hardware-transfer 비교 기준으로 유지한다.
2. simulation에서 두 카메라의 mount pose, field of view, occlusion을 검증한다.
3. 카메라에서 추정한 target position/height를 내부 좌표와 비교해 오차를 기록한다.
4. policy observation을 내부 좌표에서 카메라 추정 좌표로 바꾼다.
5. 좌표 추정이 안정화된 뒤에만 image feature 또는 end-to-end vision policy를 검토한다.
6. 실제 로봇 motion은 safety gate 이후에만 다룬다.

## 주의점

- 한 대의 카메라만으로도 calibration과 알려진 작업 평면이 있으면 거리 추정은 가능하지만, 높이 변화와 occlusion에 취약하다.
- 두 대 구성은 calibration 부담이 늘지만, 몸통 카메라가 global context를 보고 wrist camera가 final alignment를 보완하므로 pick/push/pull 전환에 더 유리하다.
- 카메라 설계 변경은 `robotarm_mt4`의 asset, mapping, safety 기준과 함께 기록한다.
