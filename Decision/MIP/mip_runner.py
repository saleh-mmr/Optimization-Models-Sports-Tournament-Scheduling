# MIP/mip_runner.py

from MIP.mip_solve import solve_mip_decision


def run_single_mip(n):
    """
    Run a single MIP instance.

    Parameters:
    -----------
    n : int
        Number of teams
    """
    print(f"\n{'='*60}")
    print(f"Running MIP for n={n}")
    print(f"{'='*60}\n")
    solve_mip_decision(n)


def run_multiple_mip(n_values):
    """
    Run multiple MIP instances.

    Parameters:
    -----------
    n_values : list of int
        List of n values to solve
    """
    total = len(n_values)
    for idx, n in enumerate(n_values, 1):
        print(f"\n{'='*60}")
        print(f"Progress: {idx}/{total} - Running MIP for n={n}")
        print(f"{'='*60}\n")
        solve_mip_decision(n)

    print(f"\n{'='*60}")
    print(f"Completed all {total} instances")
    print(f"{'='*60}\n")


def run_all_standard_instances():
    """
    Run all standard instances (n = 4, 6, 8, 10, 12, ...).
    """
    standard_instances = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    run_multiple_mip(standard_instances)
