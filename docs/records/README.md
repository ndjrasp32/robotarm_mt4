# MT4 기록 인덱스

## 한국어

이 폴더는 `robotarm_mt4`의 설계 결정, 학습 결과, 과거 확인 기록을 한 곳에서 관리한다. 매일 작업 기준은 `docs/CURRENT_BASELINE.md`와 `README.md`이고, 세부 근거가 필요할 때만 이 인덱스에서 연결된 기록을 연다.

### 위치 기준

| 위치 | 용도 |
| --- | --- |
| `docs/records/design/` | asset, hardware mapping, perception, workspace, safety처럼 기준이 되는 설계 기록 |
| `docs/records/training/` | 학습 실행, 영상, 수치, 분석, 다음 판단 기록 |
| `docs/records/archive/` | 현재 기준에는 직접 쓰지 않지만 보존할 과거 GUI 확인, joint sweep, bring-up 메모 |
| `training_logs/figures/` | 그래프 이미지 산출물 |
| `training_logs/videos/` | 학습/데모 영상 산출물 |

### 제목 기준

파일명은 날짜, 요소, 주제, 기록 종류가 보이게 둔다.

```text
YYYYMMDD_<element>_<topic>_<record_type>.md
```

문서 제목은 한국어를 우선한다.

```text
# YYYY-MM-DD MT4 <요소> <주제> <기록 종류>
```

영어 제목이나 원문 설명이 필요한 경우에는 문서 아래쪽에 `## English` 또는 `## English Notes`로 유지한다.

### 학습 기록 양식

학습 기록은 아래 순서를 기본값으로 사용한다.

1. 목적
2. 코드/스크립트 변경
3. 학습 실행
4. 영상
5. 최종 지표
6. 분석
7. 다음 판단
8. English Notes

### 설계 기록 양식

설계 기록은 아래 순서를 기본값으로 사용한다.

1. 목적
2. 결론
3. 기준 값 또는 변경 내용
4. 검증 방법
5. 다음 작업
6. English Notes

### 핵심 기록

| 구분 | 문서 |
| --- | --- |
| 현재 기준 | `../CURRENT_BASELINE.md` |
| 작업 공간 정의 | `design/20260611_mt4_reach_limited_workspace_audit.md` |
| perception 계획 | `design/20260608_dual_pi_camera_perception_plan.md` |
| MT4 hardware mapping | `design/20260518_mt4_hardware_transfer_mapping.md` |
| 2026-06-11 학습 산출물 묶음 | `training/20260611_artifact_index.md` |
| 최신 Stage 0 엔트리 게이트 결과 | `training/20260611_reach_aware_stage0_entrygate_600iter_analysis.md` |

## English

This folder keeps `robotarm_mt4` design decisions, training results, and archived bring-up notes in one structure. The daily source of truth remains `docs/CURRENT_BASELINE.md` plus `README.md`; use this index when detailed evidence is needed.

Use `design/` for baseline-changing design records, `training/` for run metrics and analysis, and `archive/` for preserved historical checks. Training figures and videos remain under `training_logs/figures/` and `training_logs/videos/`.

Record titles should be Korean-first. Keep English notes at the bottom under `## English` or `## English Notes` when needed.
