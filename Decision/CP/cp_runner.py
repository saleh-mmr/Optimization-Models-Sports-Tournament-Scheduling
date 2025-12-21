from pathlib import Path
from .cp_solve import solve_cp_instance

# Absolute path to .../Decision
BASE_DIR = Path(__file__).resolve().parent.parent


def run_single_cp(n):
    """
    Run CP model for a single n using both solvers
    and store results under Decision/res/CP/.
    """
    output_dir = BASE_DIR / "res" / "CP"
    output_dir.mkdir(parents=True, exist_ok=True)

    solve_cp_instance(
        n=n,
        output_dir=output_dir,
        approach_name="gecode"
    )

    solve_cp_instance(
        n=n,
        output_dir=output_dir,
        approach_name="chuffed"
    )


def run_multiple_cp(n_values):
    """
    Run CP model for multiple n values.
    """
    for n in n_values:
        run_single_cp(n)
