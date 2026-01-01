# MIP Quick Start Guide

## Installation

```bash
# Install dependencies
pip install pulp z3-solver
```

## Basic Usage

### Run a Single Instance

```bash
# From the Decision directory
cd Decision

# Decision version for n=6
python run.py --model MIP --n 6

# Optimization version for n=6
python run.py --model MIP --n 6 --optimize
```

### Run Multiple Instances

```bash
# Batch execution
python run.py --model MIP --batch 6 8 10

# Batch with optimization
python run.py --model MIP --batch 6 8 10 --optimize
```

## Understanding the Results

Results are saved in `res/MIP/<n>.json`:

```json
{
  "pulp_cbc": {
    "time": 0,           // Runtime in seconds (floor)
    "optimal": true,      // true if solved, false if timeout
    "obj": null,          // Objective value (null for decision version)
    "sol": [              // Solution matrix
      [[1,6], [5,2], ...],  // Period 0: games in each week
      [[2,4], [6,3], ...],  // Period 1: games in each week
      [[5,3], [1,4], ...]   // Period 2: games in each week
    ]
  }
}
```

Each entry `[home, away]` represents a game where the first team plays at home.

## Checking Solutions

Use the project's solution checker (when available):

```bash
python check_solution.py res/MIP/6.json
```

## Common Issues

### Problem: "ModuleNotFoundError: No module named 'pulp'"
**Solution**: Install PuLP: `pip install pulp`

### Problem: "Infeasible" result
**Solution**: Some values of n may be infeasible with these constraints (e.g., n=4). This is expected and correct behavior.

### Problem: Timeout on large instances
**Solution**:
- Increase time limit in `mip_solve.py` (default: 300 seconds)
- Use a commercial solver like Gurobi or CPLEX (modify solver in `mip_solve.py`)
- Add more symmetry breaking constraints

## Advanced: Using Different Solvers

PuLP supports multiple solvers. To use Gurobi or CPLEX (if installed):

Edit `mip_solve.py` line 36-42:

```python
# For Gurobi
from pulp import GUROBI_CMD
solver = GUROBI_CMD(timeLimit=time_limit, threads=1, msg=1)

# For CPLEX
from pulp import CPLEX_CMD
solver = CPLEX_CMD(timeLimit=time_limit, threads=1, msg=1)
```

## File Structure

```
Decision/
├── MIP/
│   ├── __init__.py        # Package initialization
│   ├── mip_model.py       # MIP model definition
│   ├── mip_solve.py       # Solver interface
│   ├── mip_runner.py      # Runner functions
│   ├── README.md          # Full documentation
│   └── QUICKSTART.md      # This file
├── res/
│   └── MIP/              # Results directory (auto-created)
│       ├── 6.json
│       ├── 8.json
│       └── ...
├── run.py                # Main entry point
└── requirements.txt      # Python dependencies
```

## Examples

### Example 1: Test n=6
```bash
python run.py --model MIP --n 6
```

Output:
```
[MIP] Building model for n=6, optimize=False...
[MIP] Solving with pulp_cbc...
[MIP] Solver status: Optimal (code: 1)
[MIP] Solution found! obj=None, time=0s
[MIP] Results written to res/MIP\6.json
```

### Example 2: Optimize n=8
```bash
python run.py --model MIP --n 8 --optimize
```

### Example 3: Batch Run
```bash
python run.py --model MIP --batch 6 8 10 12 14
```

## Performance Tips

1. **Small instances (n ≤ 10)**: Should solve in seconds
2. **Medium instances (n = 12-16)**: May take up to a minute
3. **Large instances (n ≥ 18)**: May timeout with CBC, consider commercial solvers

## Getting Help

- See [README.md](README.md) for detailed documentation
- Check the mathematical formulation section for constraint details
- Review example solutions in `res/MIP/` directory

## Verification

To verify your implementation is working:

```bash
# Test with n=6 (should solve quickly)
python run.py --model MIP --n 6

# Check that res/MIP/6.json was created
# Verify "optimal": true in the JSON
# Check that solution matrix has correct dimensions:
#   - 3 periods (n/2 = 6/2 = 3)
#   - 5 weeks (n-1 = 6-1 = 5)
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Import errors | Run `pip install -r requirements.txt` |
| Slow performance | Try commercial solver or reduce n |
| Wrong output format | Check that solution has [period][week] structure |
| Infeasible for valid n | Check constraints in mip_model.py |

## Next Steps

1. Run tests on standard instances (6, 8, 10, 12)
2. Compare results with CP and SAT implementations
3. Document performance in your project report
4. Verify all solutions with the checker script
