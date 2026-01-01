# MIP Solution for Sports Tournament Scheduling

This directory contains the Mixed-Integer Programming (MIP) solution for the Sports Tournament Scheduling (STS) problem using Python and PuLP.

## Problem Overview

The STS problem schedules a tournament with `n` teams over `n-1` weeks, where:
- Each week has `n/2` periods
- Each period has one game between two teams (home vs away)
- Every team plays with every other team exactly once
- Every team plays exactly once per week
- Every team plays at most twice in the same period across all weeks

## Implementation Details

### Decision Variables

We use binary variables `M[i][j][p][w]` where:
- `i, j ∈ {0, ..., n-1}` are team indices (i ≠ j)
- `p ∈ {0, ..., n/2-1}` is the period
- `w ∈ {0, ..., n-2}` is the week
- `M[i][j][p][w] = 1` if team `i` plays at home against team `j` in period `p` of week `w`

### Constraints

1. **One match per slot**: Exactly one match in each (period, week) pair
2. **One game per team per week**: Each team plays exactly once in each week
3. **Each pair plays once**: Every pair of teams plays exactly once in the tournament
4. **Period limit**: Each team plays at most twice in the same period across all weeks

### Symmetry Breaking

To improve solver performance:
- Fix the first week to a canonical form: (0 vs n-1), (1 vs n-2), etc.
- Team 0 always plays at home against all other teams

### Optimization Version

The optimization version minimizes the maximum imbalance in home/away games across all teams.

Objective: Minimize `max_deviation` where for each team `t`:
```
|home_games[t] - (n-1)/2| ≤ max_deviation
```

## Files

- `mip_model.py`: Model definition with decision variables and constraints
- `mip_solve.py`: Solver interface using PuLP
- `mip_runner.py`: Runner functions for single and batch execution
- `__init__.py`: Package initialization

## Dependencies

- Python 3.8+
- PuLP >= 2.7.0 (open-source MIP solver)

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Single Instance

Run decision version for n=6 teams:
```bash
python run.py --model MIP --n 6
```

Run optimization version for n=6 teams:
```bash
python run.py --model MIP --n 6 --optimize
```

### Batch Execution

Run multiple instances:
```bash
python run.py --model MIP --batch 4 6 8 10
```

Run multiple instances with optimization:
```bash
python run.py --model MIP --batch 4 6 8 10 --optimize
```

## Output Format

Results are saved to `res/MIP/<n>.json` with the following structure:

```json
{
  "pulp_cbc": {
    "time": 42,
    "optimal": true,
    "obj": null,
    "sol": [
      [[2, 4], [5, 1], [3, 6], [3, 4], [6, 2]],
      [[5, 6], [2, 3], [4, 5], [6, 1], [1, 4]],
      [[1, 3], [4, 6], [2, 1], [5, 2], [3, 5]]
    ]
  }
}
```

Where:
- `time`: Runtime in seconds (floor value)
- `optimal`: `true` if solved, `false` if timeout/unsolved
- `obj`: Objective value (for optimization version) or `null` (for decision version)
- `sol`: Solution matrix where `sol[p][w] = [home_team, away_team]` (1-indexed)

## Solver Details

This implementation uses **CBC (COIN-OR Branch and Cut)**, an open-source MIP solver that comes bundled with PuLP. Key configuration:
- Time limit: 300 seconds (5 minutes)
- Single-threaded execution (as per project requirements)
- Binary variables only

## Performance Tips

For better performance:
1. The symmetry breaking constraints significantly reduce the search space
2. For large instances (n > 12), consider using commercial solvers (e.g., Gurobi, CPLEX) if available
3. The optimization version is harder than the decision version due to the min-max objective

## Mathematical Formulation

### Decision Variables
```
M[i,j,p,w] ∈ {0,1}  ∀i,j ∈ {0,...,n-1}, i≠j, p ∈ {0,...,n/2-1}, w ∈ {0,...,n-2}
```

### Constraints
```
1. ∑_{i,j: i≠j} M[i,j,p,w] = 1                           ∀p,w

2. ∑_{j≠t,p} M[t,j,p,w] + ∑_{i≠t,p} M[i,t,p,w] = 1      ∀t,w

3. ∑_{w,p} (M[i,j,p,w] + M[j,i,p,w]) = 1                ∀i<j

4. ∑_{w} (∑_{j≠t} M[t,j,p,w] + ∑_{i≠t} M[i,t,p,w]) ≤ 2  ∀t,p
```

### Optimization Objective
```
Minimize: z

Subject to:
  h[t] = ∑_{j≠t,p,w} M[t,j,p,w]                         ∀t
  h[t] - (n-1)/2 ≤ z                                    ∀t
  (n-1)/2 - h[t] ≤ z                                    ∀t
```

## License

This implementation is part of the CDMO 2024/2025 project work.
