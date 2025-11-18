# CP/cp_runner.py
from CP.cp_solve import solve_cp_instance

def run_single_cp(n):
    # Produce both required Gecode and (optional) Chuffed entries in the same JSON
    solve_cp_instance(n, output_dir="res/CP", approach_name="gecode")
    solve_cp_instance(n, output_dir="res/CP", approach_name="chuffed")

def run_multiple_cp(n_values):
    for n in n_values:
        run_single_cp(n)
