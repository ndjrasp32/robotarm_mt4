from pathlib import Path
import csv
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tensorboard.backend.event_processing import event_accumulator


LOG_ROOT = Path.home() / "work/isaac/src/IsaacLab/logs/rsl_rl/mirobot_reach_pregrasp_direct"
PROJECT_DIR = Path.home() / "work/robotarm/mirobot_arm_test"
OUT_DIR = PROJECT_DIR / "logs/plots"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def latest_run_dir() -> Path:
    ckpts = sorted(LOG_ROOT.rglob("model_*.pt"), key=lambda path: path.stat().st_mtime)
    if ckpts:
        return ckpts[-1].parent
    events = sorted(LOG_ROOT.rglob("events.out.tfevents.*"), key=lambda path: path.stat().st_mtime)
    if events:
        return events[-1].parent
    raise SystemExit(f"[ERROR] no checkpoints or tensorboard events under {LOG_ROOT}")


def find_tag(tags: list[str], candidates: list[str]) -> str | None:
    for candidate in candidates:
        for tag in tags:
            if candidate.lower() in tag.lower():
                return tag
    return None


def get_series(ea: event_accumulator.EventAccumulator, tag: str | None) -> tuple[list[int], list[float]]:
    if tag is None:
        return [], []
    events = ea.Scalars(tag)
    return [event.step for event in events], [event.value for event in events]


def parse_ckpt_iter(path: Path) -> int:
    match = re.search(r"model_(\d+)\.pt$", path.name)
    return int(match.group(1)) if match else -1


def nearest_value(xs: list[int], ys: list[float], target_step: int) -> float | None:
    if not xs:
        return None
    idx = min(range(len(xs)), key=lambda i: abs(xs[i] - target_step))
    return ys[idx]


def plot_tag(ea: event_accumulator.EventAccumulator, tag: str | None, filename: str, title: str) -> None:
    xs, ys = get_series(ea, tag)
    if not xs:
        print(f"[WARN] no scalar for {title}")
        return
    plt.figure(figsize=(10, 4))
    plt.plot(xs, ys, label=tag)
    plt.title(title)
    plt.xlabel("step")
    plt.grid(True)
    plt.legend()
    out = OUT_DIR / filename
    plt.tight_layout()
    plt.savefig(out, dpi=160)
    plt.close()
    print("[OK] wrote", out)


def main() -> int:
    run_dir = latest_run_dir()
    ea = event_accumulator.EventAccumulator(str(run_dir))
    ea.Reload()
    tags = ea.Tags().get("scalars", [])

    selected = {
        "success_rate": find_tag(tags, ["mirobot/success_rate", "success_rate"]),
        "pregrasp_distance": find_tag(tags, ["mirobot/mean_pregrasp_distance", "mean_pregrasp_distance"]),
        "entry_distance": find_tag(tags, ["mirobot/mean_pregrasp_entry_distance", "mean_pregrasp_entry_distance"]),
        "target_distance": find_tag(tags, ["mirobot/mean_target_distance", "mean_target_distance"]),
        "alignment": find_tag(tags, ["mirobot/mean_alignment", "mean_alignment"]),
        "contact_penalty": find_tag(tags, ["mirobot/mean_target_contact_penalty", "mean_target_contact_penalty"]),
        "reward": find_tag(tags, ["Train/mean_reward", "mean_reward", "reward"]),
    }
    print("[INFO] run:", run_dir)
    for name, tag in selected.items():
        print(f"[INFO] {name}: {tag}")

    plot_tag(ea, selected["success_rate"], "mirobot_success_curve.png", "Mirobot success rate")
    plot_tag(ea, selected["pregrasp_distance"], "mirobot_pregrasp_distance_curve.png", "Mirobot pregrasp distance")
    plot_tag(ea, selected["alignment"], "mirobot_alignment_curve.png", "Mirobot alignment")
    plot_tag(ea, selected["contact_penalty"], "mirobot_contact_penalty_curve.png", "Mirobot contact penalty")
    plot_tag(ea, selected["reward"], "mirobot_reward_curve.png", "Mirobot reward")

    series = {name: get_series(ea, tag) for name, tag in selected.items()}
    summary_path = OUT_DIR / "mirobot_checkpoint_summary.csv"
    ckpts = sorted(run_dir.glob("model_*.pt"), key=parse_ckpt_iter)
    with summary_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "checkpoint",
                "iteration",
                "success_rate",
                "pregrasp_distance",
                "entry_distance",
                "target_distance",
                "alignment",
                "contact_penalty",
                "reward",
            ],
        )
        writer.writeheader()
        for ckpt in ckpts:
            iteration = parse_ckpt_iter(ckpt)
            row = {"checkpoint": str(ckpt), "iteration": iteration}
            for name, (xs, ys) in series.items():
                row[name] = nearest_value(xs, ys, iteration)
            writer.writerow(row)

    print("[OK] wrote", summary_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

