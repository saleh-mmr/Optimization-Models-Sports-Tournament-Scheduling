import subprocess
import time
import ast
import json
from pathlib import Path


def solve_cp_instance(n, output_dir, approach_name="gecode"):
    """
    Solve a CP instance using MiniZinc and store results as JSON.
    Paths are resolved independently of the working directory.
    """

    # Ensure output_dir is a Path
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{n}.json"

    # Absolute path to cp_model.mzn
    BASE_DIR = Path(__file__).resolve().parent.parent  # .../Decision
    model_path = BASE_DIR / "CP" / "cp_model.mzn"

    cmd = [
        "minizinc",
        "--solver", approach_name,
        "--time-limit", "300000",
        str(model_path),
        "-D", f"n={n}",
    ]

    start = time.perf_counter()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.perf_counter() - start

    stdout = proc.stdout.strip()

    # Load existing results (to merge multiple solvers)
    if output_path.exists():
        with open(output_path) as f:
            result = json.load(f)
    else:
        result = {}

    # --- CASE 1: solution found ---
    if "SOL=" in stdout:
        sol_text = stdout.split("=", 1)[1]
        sol_text = sol_text.split("----------")[0].strip()
        sol_data = ast.literal_eval(sol_text)

        result[approach_name] = {
            "time": int(elapsed),
            "optimal": False,
            "obj": None,
            "sol": sol_data
        }

        print(
            f"[CP] n={n}, approach={approach_name}, "
            f"result=sat, time={int(elapsed)}s → {output_path}"
        )

    # --- CASE 2: not solved ---
    else:
        result[approach_name] = {
            "time": 300,
            "optimal": False,
            "obj": None,
            "sol": []
        }

        print(
            f"[CP] n={n}, approach={approach_name}, "
            f"result=unknown, time=300s → {output_path}"
        )

    # Write JSON result
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
