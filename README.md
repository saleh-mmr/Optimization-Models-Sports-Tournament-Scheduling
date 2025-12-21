

# **Sports Tournament Scheduling (STS)**


This repository contains the complete implementation of the **Sports Tournament Scheduling (STS)** problem, developed for the *Combinatorial Decision Making & Optimization* (CDMO) course (A.Y. 2024/2025).
The project models and solves the STS problem using:

* **Constraint Programming (CP)** with MiniZinc
* **Propositional Satisfiability (SAT)**
* **Mixed-Integer Linear Programming (MIP)**
* Optional optimization to balance home/away games

All models are executed through a unified Docker-based environment ensuring full reproducibility.

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
4. *(Optional)* Home/away assignments should be **balanced** for fairness

The project implements decision and optional optimization versions of these requirements.

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
│       └── (placeholder for future extensions)
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
└── README.md
```

---

## **3. Approaches Implemented**

### **3.1 Constraint Programming (MiniZinc)**

Located in `source/CP/`

* `cp_model.mzn`
  Defines variables for week, period, teams, and home/away assignment.
  Includes global constraints enforcing:

  * All-different pairs
  * Weekly participation
  * Period frequency limit
  * Optional home/away balancing objective

* `cp_solve.py`
  Runs the MiniZinc model programmatically, invoking solvers such as **Gecode**.

* `cp_runner.py`
  Automates running all instances within time limits and exporting outputs to `.json`.

---

### **3.2 SAT Encoding**

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

---

### **3.3 Mixed-Integer Linear Programming (MIP)**

A placeholder directory is included for future extension with a linear formulation.

---



## 4. Running the Project (Docker)

All commands must be executed from the **project root directory**, i.e. the folder containing
`Decision/`, `Optimization/`, and `Dockerfile`.

### 4.1 Build the Docker Image

Build the Docker image once:

```bash
docker build -t sts_project .
````

---

### 4.2 Run SAT Model

#### Single instance

```bash
docker run --rm sts_project \
  python3 Decision/run.py --model SAT --n 6
```

#### Batch execution

```bash
docker run --rm sts_project \
  python3 Decision/run.py --model SAT --batch 6 8 10
```

---

### 4.3 Run CP Model

#### Single instance

```bash
docker run --rm sts_project \
  python3 Decision/run.py --model CP --n 6
```

#### Batch execution

```bash
docker run --rm sts_project \
  python3 Decision/run.py --model CP --batch 6 8 10
```

---

### 4.4 Persisting Results

To store results on the host machine, mount the results directory:

```bash
docker run --rm \
  -v "$(pwd)/Decision/res:/app/Decision/res" \
  sts_project \
  python3 Decision/run.py --model SAT --n 6
```

All generated outputs will be saved in:

```
Decision/res/
```



---

## **5. Output Format**

All solutions follow the official format required by the course.
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

Where:

* `time` → floor of runtime
* `optimal` → boolean
* `obj` → integer or `null`
* `sol` → (n/2) × (n−1) matrix of home/away pairs

Example matrix entry:

```
[ [2,4], [5,1], [3,6], ... ]
```


---

## **6. File Description**

## 📂 `Decision/`

This folder contains all **decision-version models and solvers** used to solve the Sports Tournament Scheduling problem using different technologies.

---

### 📄 `Decision/run.py`

**Main entry point of the Decision project.**

* Parses command-line arguments (`--model`, `--n`, `--batch`)
* Dispatches execution to the selected approach:

  * SAT (`Decision/SAT`)
  * CP (`Decision/CP`)
* Supports:

  * single instance execution (`--n`)
  * batch execution (`--batch`)

Example:

```bash
python3 Decision/run.py --model CP --batch 6 8 10
```

---

## 📂 `Decision/CP/`

Contains the **Constraint Programming (CP)** formulation and execution logic using **MiniZinc**.

### 📄 `cp_model.mzn`

* MiniZinc model encoding the **decision version** of the tournament scheduling problem
* Defines:

  * teams, weeks, periods
  * home/away assignments
  * all problem constraints (one match per team per week, unique pairings, etc.)
* Outputs solutions in the form:

  ```
  SOL=[[[home,away], ...], ...]
  ```

---

### 📄 `cp_solve.py`

**Low-level CP solver interface.**

* Executes MiniZinc via command line using:

  * `gecode`
  * `chuffed`
* Measures runtime
* Robustly parses MiniZinc output (handles different environments, including Docker)
* Converts MiniZinc solutions into Python structures
* Writes results to:

  ```
  Decision/res/CP/<n>.json
  ```
* Ensures full compliance with the course specification (§2.4):

  * integer runtime
  * `time = 300 ⇔ optimal = false`
  * `obj = null` for decision problems

---

### 📄 `cp_runner.py`

**High-level CP experiment runner.**

* Calls `solve_cp_instance` for:

  * a single instance
  * or multiple instances in batch
* Ensures both CP solvers (`gecode`, `chuffed`) are run for each instance
* Produces a single JSON file per instance containing all CP approaches

---

## 📂 `Decision/SAT/`

Contains the **SAT-based formulation** of the decision problem using the **Z3 solver**.

### 📄 `sat_model.py`

* Encodes the tournament scheduling problem as a **Boolean SAT model**
* Defines variables and constraints corresponding to matches and schedules

---

### 📄 `sat_solve.py`

* Interfaces directly with the Z3 solver
* Solves a single SAT instance
* Measures runtime and extracts satisfiability result

---

### 📄 `sat_runner.py`

* Runs SAT experiments for:

  * single instance
  * batch of instances
* Writes results to:

  ```
  Decision/res/SAT/<n>.json
  ```
* Uses approach name `z3_sat` in result files

---

## 📂 `Decision/res/`

**Results directory (generated automatically).**

* Stores all experimental results in JSON format
* Organized by technology:

  ```
  res/
  ├── CP/
  │   ├── 6.json
  │   ├── 8.json
  │   └── 10.json
  └── SAT/
      ├── 6.json
      ├── 8.json
      └── 10.json
  ```
* Each file strictly follows the course-required format:

  ```json
  {
    "approach_name": {
      "time": 0,
      "optimal": true,
      "obj": null,
      "sol": [...]
    }
  }
  ```

---

## 📂 `Optimization/`

Contains the **optimization-version models** of the problem (not used in the Decision experiments).
This folder is reserved for the optimization task required by the project.

---

## 📄 `Dockerfile`

Defines the **Docker environment** used to run the project reproducibly.

* Installs:

  * Python
  * MiniZinc (with Gecode and Chuffed)
  * Z3 solver
* Copies the full project into the container
* Allows running both SAT and CP experiments inside Docker

Example usage:

```bash
docker build -t sts_project .
docker run --rm -v "$(pwd)/Decision/res:/app/Decision/res" sts_project \
python3 Decision/run.py --model CP --batch 6 8 10
```



---

## **7. Reproducibility Requirements**

* All models must run inside Docker
* Only free/open-source solvers are used (MiniZinc + Gecode, Z3, CBC optional for MIP)
* All code required to reproduce the experiments is included
* Outputs must pass the official `check_solution.py` validator

---

