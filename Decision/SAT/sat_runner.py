# SAT/sat_runner.py

from SAT.sat_solve import solve_sat_instance

def run_single_sat(n):
    # Write to the required relative path per project spec
    solve_sat_instance(n, output_dir="res/SAT", approach_name="sat_z3")

def run_multiple_sat(n_values):
    for n in n_values:
        run_single_sat(n)
