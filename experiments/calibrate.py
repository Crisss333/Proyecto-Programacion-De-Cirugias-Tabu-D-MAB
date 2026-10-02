"""Calibrate tabu memory, UCB scaling C and Page–Hinkley lambda.

Uses only the exploratory seeds 0–5, never the validation seeds, so the
validation study (seeds 40–59) stays independent of the tuning:

    python -m experiments.calibrate --workers 2

Writes ``runs.csv`` (resumable) and ``CALIBRATION.md`` to
``experiments/results/calibration_0_5/``.
"""

from __future__ import annotations

import argparse
import csv
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

from surgery_optim.instances import load_instance
from surgery_optim.tabu import TabuConfig, run_tabu


ROOT = Path(__file__).resolve().parents[1]
SIZES = (15, 20, 25, 30)
EXPLORATION = (0.1, 0.03, 0.01)
PH_LAMBDA = (0.35, 1.0, 3.0)
FIELDS = ("variant", "policy", "memory", "exploration", "ph_lambda", "instance_id",
          "seed", "objective", "makespan_minutes", "dmab_restarts", "repaired_candidates",
          *(f"evaluated_{move}" for move in ("swap", "insert", "room_1", "room_2", "room_pair")))


def variants() -> list[dict]:
    rows = [{"policy": "uniform", "memory": memory, "exploration": 1.0, "ph_lambda": 0.35}
            for memory in ("solution", "attribute")]
    rows += [{"policy": "dmab", "memory": "attribute", "exploration": c, "ph_lambda": lam}
             for c in EXPLORATION for lam in PH_LAMBDA]
    rows.append({"policy": "dmab", "memory": "attribute", "exploration": 1.0,
                 "ph_lambda": 0.35})
    rows += [{"policy": "ucb", "memory": "attribute", "exploration": c, "ph_lambda": 0.35}
             for c in EXPLORATION]
    for row in rows:
        row["variant"] = (f"{row['policy']}|{row['memory']}|C={row['exploration']}"
                          f"|lambda={row['ph_lambda']}")
    return rows


def work(task: tuple[dict, str, int]) -> dict:
    variant, path, seed = task
    context = load_instance(path)
    config = TabuConfig(exploration=variant["exploration"], ph_lambda=variant["ph_lambda"],
                        tabu_memory=variant["memory"])
    result = run_tabu(context, seed, variant["policy"], config)
    return {**variant, "instance_id": context.instance_id, "seed": seed,
            "objective": result.final_quality.objective,
            "makespan_minutes": result.final_quality.makespan,
            "dmab_restarts": result.dmab_restarts,
            "repaired_candidates": result.repaired_candidates,
            **{f"evaluated_{move}": count for move, count in result.evaluated_choices.items()}}


def report(output: Path) -> None:
    with (output / "runs.csv").open(newline="", encoding="utf-8") as stream:
        runs = list(csv.DictReader(stream))
    reference = {(row["instance_id"], row["seed"]): float(row["objective"]) for row in runs
                 if row["variant"].startswith("uniform|solution")}
    lines = ["# Calibración en semillas exploratorias 0–5", "",
             "Diferencia emparejada contra Tabu uniforme con memoria de soluciones "
             "(configuración de la Entrega 1); negativo es mejor. 12 instancias × 6 semillas.",
             "", "| Variante | Media dif. | Mediana de medianas por instancia | Gana / empata / "
             "pierde | Reinicios PH (mediana) | Reparados (mediana) |",
             "|---|---:|---:|---:|---:|---:|"]
    for variant in dict.fromkeys(row["variant"] for row in runs):
        rows = [row for row in runs if row["variant"] == variant]
        diffs = np.array([float(row["objective"]) - reference[row["instance_id"], row["seed"]]
                          for row in rows])
        per_instance = [np.median([float(row["objective"])
                                   - reference[row["instance_id"], row["seed"]]
                                   for row in rows if row["instance_id"] == instance])
                        for instance in dict.fromkeys(row["instance_id"] for row in rows)]
        lines.append(
            f"| `{variant}` | {diffs.mean():+.3f} | {np.median(per_instance):+.3f} | "
            f"{int((diffs < -0.25).sum())} / {int((abs(diffs) <= 0.25).sum())} / "
            f"{int((diffs > 0.25).sum())} | "
            f"{np.median([float(row['dmab_restarts']) for row in rows]):.0f} | "
            f"{np.median([float(row['repaired_candidates']) for row in rows]):.0f} |")
    lines += ["", "Gana/pierde usan el umbral práctico de 0,25 min de la Entrega 1.", ""]
    (output / "CALIBRATION.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--seeds", type=int, default=6)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "experiments/results/calibration_0_5")
    args = parser.parse_args()
    if args.seeds > 20:
        parser.error("calibration must stay within exploratory seeds 0–19")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    run_path = output / "runs.csv"
    done = set()
    if run_path.exists():
        with run_path.open(newline="", encoding="utf-8") as stream:
            done = {(r["variant"], r["instance_id"], r["seed"]) for r in csv.DictReader(stream)}
    else:
        with run_path.open("w", newline="", encoding="utf-8") as stream:
            csv.DictWriter(stream, fieldnames=FIELDS).writeheader()
    paths = [ROOT / "instances/standard" / f"HOSP-STD-{size}-{replica:02d}.yaml"
             for size in SIZES for replica in (1, 2, 3)]
    tasks = [(variant, str(path), seed) for variant in variants() for path in paths
             for seed in range(args.seeds)
             if (variant["variant"], path.stem, str(seed)) not in done]
    with ProcessPoolExecutor(args.workers) as pool, \
            run_path.open("a", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        for index, row in enumerate(pool.map(work, tasks, chunksize=4), 1):
            writer.writerow(row)
            stream.flush()
            if index % 100 == 0:
                print(f"{index}/{len(tasks)}", flush=True)
    report(output)
    print(f"Calibration written to {output / 'CALIBRATION.md'}")


if __name__ == "__main__":
    main()
