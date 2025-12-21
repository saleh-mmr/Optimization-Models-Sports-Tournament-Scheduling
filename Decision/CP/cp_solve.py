# CP/cp_solve.py

import subprocess
import time
import ast
import json
import os


def solve_cp_instance(n, output_dir="res/CP", approach_name="gecode"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/{n}.json"

    cmd = [
        "minizinc",
        "--solver", approach_name,
        "CP/cp_model.mzn",
        "-D", f"n={n}",
    ]

    start = time.perf_counter()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = time.perf_counter() - start

    stdout = proc.stdout.strip()

    # Load existing results (to merge multiple solvers)
    if os.path.exists(output_path):
        with open(output_path) as f:
            result = json.load(f)
    else:
        result = {}

    # --- CASE 1: solution found ---
    if stdout.startswith("SOL="):
        sol_text = stdout.split("=", 1)[1]
        sol_text = sol_text.split("----------")[0].strip()
        sol_data = ast.literal_eval(sol_text)

        result[approach_name] = {
            "time": int(elapsed),     # floor of runtime
            "optimal": True,
            "obj": None,
            "sol": sol_data
        }

        print(
            f"[CP] n={n}, approach={approach_name}, "
            f"result=sat, time={int(elapsed)}s → {output_path}"
        )

    # --- CASE 2: not solved (UNKNOWN / UNSAT not proven) ---
    else:
        result[approach_name] = {
            "time": 300,              # mandatory by spec
            "optimal": False,
            "obj": None,
            "sol": None
        }

        print(
            f"[CP] n={n}, approach={approach_name}, "
            f"result=unknown, time=300s → {output_path}"
        )

    # Write JSON result
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)
