# **Sports Tournament Scheduling (STS)**


This repository contains the complete implementation of the **Sports Tournament Scheduling (STS)** problem, developed for the *Combinatorial Decision Making & Optimization* (CDMO) course (A.Y. 2024/2025).
The project models and solves the STS problem using:

* **Constraint Programming (CP)** with MiniZinc
* **Propositional Satisfiability (SAT)**
* **Mixed-Integer Linear Programming (MIP)**


---

## **1. Problem Overview**

The Sports Tournament Scheduling problem consists of scheduling a round-robin tournament involving ( n ) teams over ( n - 1 ) weeks.
Each week contains ( n/2 ) periods, and every period hosts exactly one match:

* First team → **home**
* Second team → **away**

A valid schedule must satisfy:

1. Each pair of teams plays **exactly once**
2. Every team plays **exactly once per week**
3. Every team appears in the **same period at most twice** across the entire tournament

---

## **2. Repository Structure**

```
.
├── source/
│   ├── CP/
│   │   ├── cp_model.mzn
│   │   ├── cp_runner.py
│   │   └── cp_solve.py
│   ├── SAT/
│   │   ├── sat_model.py
│   │   ├── sat_solve.py
│   │   └── sat_runner.py
│   └── MIP/
│       └── mip_model.py
│       └── mip_solve.py
│       └── mip_runner.py
│
├── res/
│   ├── CP/
│   │   └── *.json
│   ├── SAT/
│   │   └── *.json
│   └── MIP/
│       └── *.json
│
├── Dockerfile
└── CDMO.pdf (report)
```

---


## **3. How to Run**

Defines the **Docker environment** used to run the project reproducibly.

* Installs:

  * Python 3.8
  * MiniZinc + Gecode solver + Chuffed solver
  * Z3 solver
  * CBC solver for MIP
* Copies the full project into the container
* Allows running both SAT and CP experiments inside Docker

Example usage:

```bash
docker build -t sts_project .
docker run --rm -v "$(pwd)/Decision/res:/app/Decision/res" sts_project \
python3 Decision/run.py --model CP --batch 6 8 10
```

---

## **4. Approaches Implemented**

### **4.1 Constraint Programming (MiniZinc)**

Located in `source/CP/`

* `cp_model.mzn`
  Defines variables for week, period, teams, and home/away assignment.
  Includes global constraints enforcing:

  * All-different pairs
  * Weekly participation
  * Period frequency limit

* `cp_solve.py`
  Runs the MiniZinc model programmatically.

* `cp_runner.py`
  Automates running all instances within time limits and exporting outputs to `.json`.

Usage examples (from project root):

Single instance:

```bash
docker run --rm sts_project \
  python3 Decision/run.py --model CP --n 6
```

Batch execution:

```bash
docker run --rm sts_project \
  python3 Decision/run.py --model CP --batch 6 8 10
```


---

### **4.2 SAT**

Located in `source/SAT/`

* `sat_model.py`
  Creates the Boolean encoding for:

  * Match assignment
  * Home/away orientation
  * Weekly participation
  * Period frequency constraints

* `sat_solve.py`
  Uses **Z3** to solve the SAT model.

* `sat_runner.py`
  Runs all instances sequentially, applies a 300-second timeout, and produces the required JSON structure.

Usage examples (from project root):

Single instance:

```bash
docker run --rm sts_project \
  python3 Decision/run.py --model SAT --n 6
```

Batch execution:

```bash
docker run --rm sts_project \
  python3 Decision/run.py --model SAT --batch 6 8 10
```


---

### **4.3 Mixed-Integer Linear Programming (MIP)**

The repository includes a complete decision-version MIP implementation under `Decision/MIP/` using PuLP with the open-source CBC solver.
Key files:

* `Decision/MIP/mip_model.py`
  - Builds the PuLP model and binary decision variables
  - Implements the main constraints.
  - Adds a lightweight symmetry-breaking constraint (fixes the first match: team 0 home vs team n-1 in period 0, week 0).

* `Decision/MIP/mip_solve.py`
  - Configures and runs CBC via `PULP_CBC_CMD`.
  - Measures runtime and maps solver status to the project's JSON result format.
  - Extracts a feasible schedule (when found) with teams converted to 1-indexed values and writes results into `Decision/res/MIP/<n>.json`.

* `Decision/MIP/mip_runner.py`
  - Small helper functions to run single, multiple, or all standard instances (4,6,8,...,20).


Usage examples (from project root):

Single instance:

```bash
docker run --rm sts_project \
  python3 Decision/run.py --model MIP --n 6
```

Batch execution:

```bash
docker run --rm sts_project \
  python3 Decision/run.py --model MIP --batch 6 8 10
```


---

## **5. Output Format**

All solutions follow the format required by the course.
Each solved instance produces a JSON file:

```
{
  "gecode": {
    "time": 120,
    "optimal": true,
    "obj": null,
    "sol": [...]
  },
  "z3_sat": {
    "time": 300,
    "optimal": false,
    "obj": null,
    "sol": [...]
  }
}
```
---

## **6. Reproducibility Requirements**

* All models must run inside Docker
* Only free/open-source solvers are used (MiniZinc + Gecode + Chuffed, Z3, CBC optional for MIP)
* Outputs passed the `check_solution.py` validator

---
