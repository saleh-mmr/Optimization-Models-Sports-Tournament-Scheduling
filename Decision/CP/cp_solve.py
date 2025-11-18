# CP/cp_solve.py
import json, os, time, subprocess

def solve_cp_instance(n, output_dir="res/CP", approach_name="chuffed"):
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/{n}.json"

    solver_flag = ["--solver", approach_name]  # "gecode" or "chuffed"
    cmd = ["minizinc", *solver_flag, "--time-limit", "300000", "CP/cp_model.mzn", "-D", f"n={n}"]

    start = time.perf_counter()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=305)
        elapsed = time.perf_counter() - start
        solved = False
        sol = None
        # Default: unknown unless we find SOL or UNSAT
        status_text = proc.stdout + "\n" + proc.stderr

        # Look for solution line
        for line in proc.stdout.splitlines():
            s = line.strip()
            if s.startswith("SOL="):
                payload = s[len("SOL="):]
                sol = json.loads(payload)
                solved = True  # feasible solution found
                break

        # Detect UNSAT (MiniZinc typically prints "=====UNSATISFIABLE=====")
        if not solved and "UNSATISFIABLE" in status_text:
            solved = True  # decision instance conclusively solved with no solution
            sol = None

        # Apply 300s rule for non-solved terminations
        time_value = int(elapsed) if solved else 300

        # Merge/append under approach key if file exists
        result = {}
        if os.path.exists(output_path):
            with open(output_path) as f:
                result = json.load(f)

        result[approach_name] = {
            "time": time_value,
            "optimal": bool(solved),
            "obj": None,
            "sol": sol
        }

        with open(output_path, "w") as f:
            json.dump(result, f)

        print(f"[CP] n={n}, approach={approach_name}, "
              f"result={'sat' if sol else ('unsat' if solved else 'unknown')}, time={time_value}s → {output_path}")

    except subprocess.TimeoutExpired:
        # Hard timeout: record unsolved with time=300
        result = {}
        if os.path.exists(output_path):
            with open(output_path) as f:
                result = json.load(f)
        result[approach_name] = {"time": 300, "optimal": False, "obj": None, "sol": None}
        with open(output_path, "w") as f:
            json.dump(result, f)
        print(f"[CP] n={n}, approach={approach_name}, result=timeout, time=300s → {output_path}")
