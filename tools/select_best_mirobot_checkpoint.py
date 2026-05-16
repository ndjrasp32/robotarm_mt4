from pathlib import Path
import csv
import math


PROJECT_DIR = Path.home() / "work/robotarm/mirobot_arm_test"
SUMMARY_PATH = PROJECT_DIR / "logs/plots/mirobot_checkpoint_summary.csv"
BEST_FILE = PROJECT_DIR / "logs/plots/best_checkpoint.txt"


def value(row: dict[str, str], key: str, default: float) -> float:
    text = row.get(key)
    if text in (None, "", "None"):
        return default
    try:
        result = float(text)
    except ValueError:
        return default
    return result if math.isfinite(result) else default


def score(row: dict[str, str]) -> float:
    success = value(row, "success_rate", 0.0)
    pregrasp_distance = value(row, "pregrasp_distance", 1.0)
    alignment = value(row, "alignment", -1.0)
    contact = value(row, "contact_penalty", 1.0)
    reward = value(row, "reward", 0.0)
    return 100.0 * success + 4.0 * alignment + 0.01 * reward - 12.0 * pregrasp_distance - 25.0 * contact


def main() -> int:
    if not SUMMARY_PATH.is_file():
        raise SystemExit(f"[ERROR] summary not found: {SUMMARY_PATH}")

    with SUMMARY_PATH.open(newline="") as f:
        rows = list(csv.DictReader(f))
    rows = [row for row in rows if row.get("checkpoint") and Path(row["checkpoint"]).is_file()]
    if not rows:
        raise SystemExit(f"[ERROR] no valid checkpoint rows in {SUMMARY_PATH}")

    best = max(rows, key=score)
    BEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    BEST_FILE.write_text(best["checkpoint"] + "\n")

    print("[OK] best checkpoint:", best["checkpoint"])
    print("[OK] score:", f"{score(best):.4f}")
    print("[OK] success_rate:", best.get("success_rate"))
    print("[OK] pregrasp_distance:", best.get("pregrasp_distance"))
    print("[OK] alignment:", best.get("alignment"))
    print("[OK] contact_penalty:", best.get("contact_penalty"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

