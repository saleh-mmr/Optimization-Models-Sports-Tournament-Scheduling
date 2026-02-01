# MIP/mip_solve.py

import json
import os
import time
from pathlib import Path
from pulp import PULP_CBC_CMD, LpStatusOptimal
from MIP.mip_model import build_mip_model, extract_solution_from_model


def solve_mip_instance(n, output_dir="res/MIP", approach_name="pulp_cbc", time_limit=300):
    """
    Solve a MIP instance for the Sports Tournament Scheduling problem.

    Parameters:
    -----------
    n : int
        Number of teams (must be even)
    output_dir : str
        Directory to save the results
    approach_name : str
        Name of the approach (e.g., "pulp_cbc")
    time_limit : int
        Time limit in seconds (default: 300)

    Returns:
    --------
    None (writes results to JSON file)
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{n}.json")

    # Build the MIP model
    print(f"[MIP] Building model for n={n}...")
    model, M, W, P = build_mip_model(n)

    # Configure the solver
    # PULP_CBC_CMD is the default open-source solver that comes with PuLP
    # timeLimit is in seconds
    solver = PULP_CBC_CMD(
        timeLimit=time_limit,
        msg=1,  # Print solver messages
        options=[
            'threads 1',  # Use single core as per project requirements
        ]
    )

    # Solve the model
    print(f"[MIP] Solving with {approach_name}...")
    start = time.perf_counter()
    model.solve(solver)
    elapsed = time.perf_counter() - start
    elapsed_floor = int(elapsed)

    # Check the solution status
    status = model.status
    status_name = {
        1: "Optimal",
        0: "Not Solved",
        -1: "Infeasible",
        -2: "Unbounded",
        -3: "Undefined"
    }.get(status, "Unknown")

    print(f"[MIP] Solver status: {status_name} (code: {status})")
    print(f"[MIP] Time elapsed: {elapsed:.2f}s")

    # Prepare the result
    if status == LpStatusOptimal or status == 1:
        # Solution found
        sol = extract_solution_from_model(model, M, n, W, P)

        if sol is None:
            # Something went wrong in extraction
            result_data = {
                "time": 300,
                "optimal": False,
                "obj": None,
                "sol": []
            }
            print(f"[MIP] ERROR: Could not extract solution despite optimal status")
        else:
            result_data = {
                "time": elapsed_floor,
                "optimal": True,
                "obj": None,
                "sol": sol
            }
            print(f"[MIP] Solution found! time={elapsed_floor}s")
    else:
        # No solution found (timeout, infeasible, or error)
        # Per project specs: if not solved, time=300 and optimal=False
        result_data = {
            "time": 300,
            "optimal": False,
            "obj": None,
            "sol": []
        }
        print(f"[MIP] No solution found within time limit")

    # Load existing results if the file exists (to merge multiple approaches)
    existing_results = {}
    if os.path.exists(output_path):
        try:
            with open(output_path, "r") as f:
                existing_results = json.load(f)
        except Exception as e:
            print(f"[MIP] Warning: Could not load existing results: {e}")
            existing_results = {}

    # Add this approach's results
    existing_results[approach_name] = result_data

    # Write the results to JSON
    with open(output_path, "w") as f:
        json.dump(existing_results, f, indent=2)

    print(f"[MIP] Results written to {output_path}")


def solve_mip_decision(n, output_dir="res/MIP", approach_name="pulp_cbc"):
    """
    Convenience function to solve the MIP instance.
    """
    solve_mip_instance(n, output_dir, approach_name)
