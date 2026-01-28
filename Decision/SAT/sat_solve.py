# SAT/sat_solve.py

import json, os, time
from z3 import Solver, sat, unsat, BoolVal
from SAT.sat_model import build_vars, one_match_per_slot, team_plays_once_per_week, each_pair_plays_once, limit_period_usage

def extract_solution(model, M, n, W, P):
    """
    Build the (n/2) x (n-1) matrix: sol[p][w] = [home, away]
    Teams are 0..n-1 here; if your checker expects 1..n, add +1 when emitting.
    The project’s example uses 1-based teams, so we convert to 1..n.
    """
    sol = [[None for _ in range(W)] for _ in range(P)]
    for w in range(W):
        for p in range(P):
            found = False
            for i in range(n):
                if found: break
                for j in range(n):
                    if i == j:
                        continue
                    # model_completion ensures a Boolean is returned
                    if model.evaluate(M[i][j][p][w], model_completion=True):
                        sol[p][w] = [i + 1, j + 1]  # convert to 1-based
                        found = True
                        break
    return sol

def solve_sat_instance(n, output_dir="res/SAT", approach_name="sat_z3"):
    M, W, P = build_vars(n)
    s = Solver()
    s.set("timeout", 300000)  # 300 seconds (ms)

    # Core constraints
    for w in range(W):
        for p in range(P):
            one_match_per_slot(s, M, p, w, n)
    team_plays_once_per_week(s, M, n, W, P)
    each_pair_plays_once(s, M, n, W, P)
    limit_period_usage(s, M, n, W, P)

    # Solve
    os.makedirs(output_dir, exist_ok=True)
    output_path = f"{output_dir}/{n}.json"

    start = time.perf_counter()
    z3_result = s.check()
    elapsed = time.perf_counter() - start
    elapsed_floor = int(elapsed)

    # Interpret result per project rules
    # - SAT: feasible solution found -> optimal = True, time = floor(elapsed)
    # - UNSAT: decision instance conclusively solved -> optimal = True, sol = None, time = floor(elapsed)
    # - UNKNOWN (e.g., timeout): not solved -> optimal = False, time = 300
    if z3_result == sat:
        model = s.model()
        sol = extract_solution(model, M, n, W, P)
        time_value = elapsed_floor
        sol_payload = sol
    elif z3_result == unsat:
        time_value = 300
        sol_payload = []
    else:
        # unknown (e.g., timeout) -> enforce 300-second rule
        time_value = 300
        sol_payload = []

    # Merge with existing file if present (so you can add more SAT approaches later)
    result = {}
    if os.path.exists(output_path):
        with open(output_path, "r") as f:
            try:
                result = json.load(f)
            except Exception:
                result = {}

    result[approach_name] = {
        "time": time_value,
        "optimal": False,
        "obj": None,
        "sol": sol_payload
    }

    with open(output_path, "w") as f:
        json.dump(result, f)

    status_str = "sat" if z3_result == sat else ("unsat" if z3_result == unsat else "unknown")
    print(f"[SAT] n={n}, approach={approach_name}, result={status_str}, time={time_value}s → {output_path}")
