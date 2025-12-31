# test_mip.py - Simple test to verify MIP model constraints

from mip_model import build_mip_model, extract_solution_from_model
from pulp import PULP_CBC_CMD, value

def test_solution_manually(n=4):
    """
    Test with a known valid solution for n=4
    """
    print(f"Testing MIP model for n={n}")

    # Build the model without optimize
    model, M, W, P = build_mip_model(n, optimize=False)

    # Print model statistics
    print(f"Number of weeks (W): {W}")
    print(f"Number of periods (P): {P}")
    print(f"Number of variables: {len(model.variables())}")
    print(f"Number of constraints: {len(model.constraints)}")

    # Try to solve
    solver = PULP_CBC_CMD(timeLimit=60, msg=1)
    model.solve(solver)

    print(f"Status: {model.status}")
    print(f"Status value: {model.sol_status}")

    if model.status == 1:
        sol = extract_solution_from_model(model, M, n, W, P)
        print("Solution found:")
        for p in range(P):
            print(f"  Period {p}: {sol[p]}")
    else:
        print("No solution found - problem is infeasible!")
        print("\nChecking which constraints might be problematic...")

        # Try without symmetry breaking
        print("\nTrying without symmetry breaking...")
        model2, M2, W2, P2 = build_mip_model_no_symbreak(n)
        model2.solve(solver)
        print(f"Status without symbreak: {model2.status}")

        if model2.status == 1:
            sol = extract_solution_from_model(model2, M2, n, W2, P2)
            print("Solution found without symmetry breaking:")
            for p in range(P2):
                print(f"  Period {p}: {sol[p]}")


def build_mip_model_no_symbreak(n):
    """Build model without symmetry breaking for testing"""
    from pulp import LpVariable, LpProblem, LpMinimize, lpSum, LpBinary

    W = n - 1
    P = n // 2

    model = LpProblem("STS_Test", LpMinimize)

    M = {}
    for i in range(n):
        M[i] = {}
        for j in range(n):
            if i == j:
                continue
            M[i][j] = {}
            for p in range(P):
                M[i][j][p] = {}
                for w in range(W):
                    M[i][j][p][w] = LpVariable(f"M_{i}_{j}_{p}_{w}", cat=LpBinary)

    # Constraint 1: One match per slot
    for w in range(W):
        for p in range(P):
            match_vars = [M[i][j][p][w] for i in range(n) for j in range(n) if i != j]
            model += lpSum(match_vars) == 1

    # Constraint 2: Each team plays once per week
    for t in range(n):
        for w in range(W):
            involved_vars = []
            for j in range(n):
                if j != t:
                    for p in range(P):
                        involved_vars.append(M[t][j][p][w])
            for i in range(n):
                if i != t:
                    for p in range(P):
                        involved_vars.append(M[i][t][p][w])
            model += lpSum(involved_vars) == 1

    # Constraint 3: Each pair plays once
    for i in range(n):
        for j in range(i + 1, n):
            pair_vars = []
            for w in range(W):
                for p in range(P):
                    pair_vars.append(M[i][j][p][w])
                    pair_vars.append(M[j][i][p][w])
            model += lpSum(pair_vars) == 1

    # Constraint 4: At most twice per period
    for t in range(n):
        for p in range(P):
            period_appearances = []
            for j in range(n):
                if j != t:
                    for w in range(W):
                        period_appearances.append(M[t][j][p][w])
            for i in range(n):
                if i != t:
                    for w in range(W):
                        period_appearances.append(M[i][t][p][w])
            model += lpSum(period_appearances) <= 2

    model += 0

    return model, M, W, P


if __name__ == "__main__":
    test_solution_manually(4)
