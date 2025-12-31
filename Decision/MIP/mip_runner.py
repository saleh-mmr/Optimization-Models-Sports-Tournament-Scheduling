# MIP/mip_runner.py

from MIP.mip_solve import solve_mip_decision, solve_mip_optimization


def run_single_mip(n, optimize=False):
    """
    Run a single MIP instance.

    Parameters:
    -----------
    n : int
        Number of teams
    optimize : bool
        If True, run optimization version; if False, run decision version
    """
    if optimize:
        print(f"\n{'='*60}")
        print(f"Running MIP Optimization for n={n}")
        print(f"{'='*60}\n")
        solve_mip_optimization(n)
    else:
        print(f"\n{'='*60}")
        print(f"Running MIP Decision for n={n}")
        print(f"{'='*60}\n")
        solve_mip_decision(n)


def run_multiple_mip(n_values, optimize=False):
    """
    Run multiple MIP instances.

    Parameters:
    -----------
    n_values : list of int
        List of n values to solve
    optimize : bool
        If True, run optimization version; if False, run decision version
    """
    total = len(n_values)
    for idx, n in enumerate(n_values, 1):
        print(f"\n{'='*60}")
        print(f"Progress: {idx}/{total} - Running MIP for n={n}")
        print(f"{'='*60}\n")

        if optimize:
            solve_mip_optimization(n)
        else:
            solve_mip_decision(n)

    print(f"\n{'='*60}")
    print(f"Completed all {total} instances")
    print(f"{'='*60}\n")


def run_all_standard_instances(optimize=False):
    """
    Run all standard instances (n = 4, 6, 8, 10, 12, ...).
    """
    standard_instances = [4, 6, 8, 10, 12, 14, 16, 18, 20]
    run_multiple_mip(standard_instances, optimize=optimize)
