# run.py (only the relevant parts shown)
import argparse
from SAT.sat_runner import run_single_sat, run_multiple_sat
from CP.cp_runner import run_single_cp, run_multiple_cp

parser = argparse.ArgumentParser()
parser.add_argument("--model", required=True, choices=["SAT", "CP"])
parser.add_argument("--n", type=int)
parser.add_argument("--batch", nargs="*", type=int)
args = parser.parse_args()

if args.model == "SAT":
    if args.n:
        run_single_sat(args.n)
    elif args.batch:
        run_multiple_sat(args.batch)

elif args.model == "CP":
    if args.n:
        run_single_cp(args.n)
    elif args.batch:
        run_multiple_cp(args.batch)
