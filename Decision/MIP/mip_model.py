# MIP/mip_model.py

from pulp import LpVariable, LpProblem, LpMinimize, lpSum, LpBinary, LpStatus


def build_mip_model(n, optimize=False):
    """
    Build a MIP model for the Sports Tournament Scheduling problem.

    Parameters:
    -----------
    n : int
        Number of teams (must be even)
    optimize : bool
        If True, optimize for balanced home/away games
        If False, just find a feasible solution

    Returns:
    --------
    model : LpProblem
        The PuLP model
    M : dict
        Decision variables M[i][j][p][w] = 1 if team i plays at home against team j
        in period p of week w
    W : int
        Number of weeks (n-1)
    P : int
        Number of periods per week (n/2)
    """
    assert n % 2 == 0 and n >= 2, "n must be an even integer >= 2"

    W = n - 1  # Number of weeks
    P = n // 2  # Number of periods per week

    # Create the problem
    if optimize:
        model = LpProblem("STS_Optimization", LpMinimize)
    else:
        model = LpProblem("STS_Decision", LpMinimize)

    # Decision variables: M[i][j][p][w] = 1 if team i plays at home vs team j
    # in period p of week w (i,j in 0..n-1)
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
                    M[i][j][p][w] = LpVariable(
                        f"M_{i}_{j}_{p}_{w}",
                        cat=LpBinary
                    )

    # --- CONSTRAINT 1: Exactly one match per slot (period, week) ---
    # In each (period, week), exactly one pair (i,j) with i!=j plays
    for w in range(W):
        for p in range(P):
            match_vars = [
                M[i][j][p][w]
                for i in range(n)
                for j in range(n)
                if i != j
            ]
            model += lpSum(match_vars) == 1, f"OneMatchPerSlot_w{w}_p{p}"

    # --- CONSTRAINT 2: Each team plays exactly once per week ---
    for t in range(n):
        for w in range(W):
            involved_vars = []
            # Team t plays at home against someone
            for j in range(n):
                if j != t:
                    for p in range(P):
                        involved_vars.append(M[t][j][p][w])
            # Team t plays away against someone
            for i in range(n):
                if i != t:
                    for p in range(P):
                        involved_vars.append(M[i][t][p][w])

            model += lpSum(involved_vars) == 1, f"TeamPlaysOncePerWeek_t{t}_w{w}"

    # --- CONSTRAINT 3: Each pair of teams plays exactly once in the tournament ---
    for i in range(n):
        for j in range(i + 1, n):
            pair_vars = []
            for w in range(W):
                for p in range(P):
                    # Either i plays home vs j, or j plays home vs i
                    pair_vars.append(M[i][j][p][w])
                    pair_vars.append(M[j][i][p][w])

            model += lpSum(pair_vars) == 1, f"EachPairPlaysOnce_i{i}_j{j}"

    # --- CONSTRAINT 4: Each team plays at most twice in the same period ---
    # across all weeks
    for t in range(n):
        for p in range(P):
            period_appearances = []
            # Team t at home in period p
            for j in range(n):
                if j != t:
                    for w in range(W):
                        period_appearances.append(M[t][j][p][w])
            # Team t away in period p
            for i in range(n):
                if i != t:
                    for w in range(W):
                        period_appearances.append(M[i][t][p][w])

            model += lpSum(period_appearances) <= 2, f"MaxTwicePerPeriod_t{t}_p{p}"

    # --- SYMMETRY BREAKING (Optional, but recommended for performance) ---
    # Lighter symmetry breaking to avoid over-constraining the problem
    # Fix the first match: team 0 plays at home against team n-1 in period 0, week 0
    model += M[0][n-1][0][0] == 1, "SymBreak_FirstMatch"

    # --- OPTIMIZATION OBJECTIVE (if optimize=True) ---
    if optimize:
        # Minimize the maximum imbalance in home/away games for any team
        # Create auxiliary variables for home games count per team
        home_games = {}
        for t in range(n):
            home_games[t] = LpVariable(f"HomeGames_t{t}", lowBound=0, cat='Integer')
            # Count home games for team t
            model += home_games[t] == lpSum(
                M[t][j][p][w]
                for j in range(n) if j != t
                for p in range(P)
                for w in range(W)
            ), f"CountHomeGames_t{t}"

        # For n teams, each team plays n-1 games total
        # Ideal balance: (n-1)/2 home and (n-1)/2 away
        # Create a variable for maximum deviation from ideal
        max_deviation = LpVariable("MaxDeviation", lowBound=0, cat='Integer')

        ideal = (n - 1) / 2.0
        for t in range(n):
            # |home_games[t] - ideal| <= max_deviation
            # This is modeled as two constraints:
            model += home_games[t] - ideal <= max_deviation, f"MaxDev_Upper_t{t}"
            model += ideal - home_games[t] <= max_deviation, f"MaxDev_Lower_t{t}"

        # Minimize the maximum deviation
        model += max_deviation, "MinimizeMaxDeviation"
    else:
        # For decision version, no objective (or minimize 0)
        model += 0, "NoObjective"

    return model, M, W, P


def extract_solution_from_model(model, M, n, W, P):
    """
    Extract the solution from a solved MIP model.

    Returns:
    --------
    sol : list of lists
        sol[p][w] = [home_team, away_team] (1-indexed)
        Returns None if no solution found
    """
    if model.status != 1:  # LpStatusOptimal = 1
        return None

    sol = [[None for _ in range(W)] for _ in range(P)]

    for w in range(W):
        for p in range(P):
            found = False
            for i in range(n):
                if found:
                    break
                for j in range(n):
                    if i == j:
                        continue
                    # Check if this variable is set to 1
                    if M[i][j][p][w].varValue is not None and M[i][j][p][w].varValue > 0.5:
                        # Convert to 1-indexed teams
                        sol[p][w] = [i + 1, j + 1]
                        found = True
                        break

    return sol


def calculate_objective_value(M, n, W, P):
    """
    Calculate the objective value (max deviation in home/away balance).

    Returns:
    --------
    obj : int
        Maximum deviation from perfect balance
    """
    home_counts = [0] * n

    for t in range(n):
        for j in range(n):
            if j == t:
                continue
            for p in range(P):
                for w in range(W):
                    if M[t][j][p][w].varValue is not None and M[t][j][p][w].varValue > 0.5:
                        home_counts[t] += 1

    ideal = (n - 1) / 2.0
    max_deviation = max(abs(count - ideal) for count in home_counts)

    return int(max_deviation)
