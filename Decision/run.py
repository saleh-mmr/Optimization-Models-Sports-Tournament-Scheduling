# run.py
import argparse
from SAT.sat_runner import run_single_sat, run_multiple_sat
from CP.cp_runner import run_single_cp, run_multiple_cp
from MIP.mip_runner import run_single_mip, run_multiple_mip

parser = argparse.ArgumentParser(
    description="Run Sports Tournament Scheduling solvers (CP, SAT, or MIP)"
)
parser.add_argument("--model", required=True, choices=["SAT", "CP", "MIP"],
                    help="Model type to use")
parser.add_argument("--n", type=int,
                    help="Number of teams (single instance)")
parser.add_argument("--batch", nargs="*", type=int,
                    help="List of n values for batch execution")
args = parser.parse_args()

if args.model == "SAT":
    if args.n:
        run_single_sat(args.n)
    elif args.batch:
        run_multiple_sat(args.batch)
    else:
        print("Error: Must specify either --n or --batch")

elif args.model == "CP":
    if args.n:
        run_single_cp(args.n)
    elif args.batch:
        run_multiple_cp(args.batch)
    else:
        print("Error: Must specify either --n or --batch")

elif args.model == "MIP":
    if args.n:
        run_single_mip(args.n)
    elif args.batch:
        run_multiple_mip(args.batch)
    else:
        print("Error: Must specify either --n or --batch")
