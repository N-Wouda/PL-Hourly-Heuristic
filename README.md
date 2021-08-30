# PL-Heuristic

This repository hosts all code used in the development of an hourly
scheduling heuristic for personalised learning. The repository exposes
several executable packages: one for the heuristic, the integer linear program
model, the validator, and an analysis tools for the heuristic and ILP results.
The heuristic quickly solves a problem using a sub-optimal method (minutes). 
The ILP takes considerably longer (hours to days), but does guarantee 
optimality. The validator tool verifies a given solution satisfies the imposed 
constraints.

> **Note** that this repository assumes an `/experiments` directory is
set-up, and populated with the experimental data. The data is of considerable
size, and as such not part of the repository itself. The data may be downloaded
from [the data repository](https://doi.org/10.34894/E2L6WC).
This archive also contains a static version of the code hosted here.

## Analysis

The analysis tool is available in `/analysis`. It can be used to analyse results
from an ILP or heuristic run on an entire experiment. Usage,

```
pipenv run python -m analysis heuristic 1
```

Which analyses the heuristic output in experiment `1`. If an output does not
exist, it is skipped - you are informed of this. After analysing all files in an
experiment, a cached file is created in `analysis/cache` to speed-up subsequent
analyses - this can be overridden using the `--force` flag. Use the `--help`
flag to see all options. 

A notebook analysing the cached files is available in the repository root as
`analysis.ipynb`. This contains most results described in the paper.

## How to use

Ensure you have an environment with at least Python 3.7. To run the validator
and/or heuristic, you need to install the required packages via `pipenv`.

For the ILP formulation, more is needed: you need to ensure a valid
instance of the CPLEX programme is installed on your machine, with the
relevant Python bindings exposed. CPLEX is commercial software offered
by IBM, so this cannot easily be done via `pip`.

## Heuristic

Available in `/heuristic`. The heuristic is based on the adaptive
large neighbourhood search (ALNS) metaheuristic, and performs several
operators to achieve a reasonable solution in little time. No
optimality guarantees are made. Usage,

```
pipenv run python -m heuristic 1 5
```

For experiment `1`, instance `5`. The assignment output will be written
to the `experiments` directory, as `experiments/1/5-heuristic.json`.

## ILP

Available in `/ilp`. The ILP solves the indicated experiment instance
to optimality, but might take a considerable amount of time to achieve
this. Furthermore, the ILP relies on IBM CPLEX, which is commercial
software. Should you wish to run the ILP formulation yourself, you need
to ensure your Python installation is configured with the CPLEX
bindings for Python. Usage,

```
pipenv run python -m ilp 1 5
```

For experiment `1`, instance `5`. The assignment output will be written
to the `experiments` directory, as `experiments/1/5-ilp.json`.

## Validator

Available in `/validator`. Given the by now familiar experiment and
instance arguments, the validator confirms the ILP and heuristic
solutions (where available) satisfy the problem constraints. Usage,

```
pipenv run python -m validator 1 5
```

For experiment `1`, instance `5`. An exit code of `0` indicates the ILP and
heuristic solutions both meet the problem constraints, `1` suggests one or more
constraints fail. In this case output is printed hinting which constraint is
violated.
