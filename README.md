# PL-Heuristic

This repository hosts all code used in the development of an hourly
scheduling heuristic for personalised learning. The repository exposes
three executable packages: one for the heuristic, the integer linear
model, and the validator respectively. The heuristic quickly solves a
problem using a sub-optimal method (seconds). The ILP takes considerably
longer (days), but does guarantee optimality. The validator tool
verifies a given solution satisfies the imposed constraints.

> **Note** that this repository assumes an `/experiments` directory is
set-up, and populated with the experiment data. This data is of
considerable size, and as such not part of the repository itself. It is
available upon request. TODO

## Article and analysis

The `/analysis` directory hosts some Jupyter notebooks that contain
all results presented in the paper. The paper itself is available in
pre-print in the repository, as `article.pdf`. TODO

## How to use

Ensure you have an environment with at least Python 3.6. Then, to run
the validator and/or heuristic, you may install the required packages
as,

```
pip install -r requirements.txt
```

For the ILP formulation, more is needed: you need to ensure a valid
instance of the CPLEX programme is installed on your machine, with the
relevant Python bindings exposed. CPLEX is commercial software offered
by IBM, so this cannot easily be done via `pip`.

## Heuristic

Available in `/heuristic`. The heuristic is inspired by the adaptive
large neighbourhood search (ALNS) metaheuristic, and performs several
operators to achieve a reasonable solution in little time. No
optimality guarantees are made. Usage,

```
python -m heuristic 1 5
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
python -m ilp 1 5
```

For experiment `1`, instance `5`. The assignment output will be written
to the `experiments` directory, as `experiments/1/5-ilp.json`.

## Validator

Available in `/validator`. Given the by now familiar experiment and
instance arguments, the validator confirms the ILP and heuristic
solutions (where available) satisfy the problem constraints. Usage,

```
>>>python -m validator 1 5

Solution (ilp) satisfies constraints for exp. 1, inst. 5? True
Solution (heuristic) satisfies constraints for exp. 1, inst. 5? True
```

For experiment `1`, instance `5`. Since validating *all* instances in
a given experiment quickly turns tedious, there is the option to pass
in a wildcard, like so,

```
python -m validator 1 *
```

This will run the validator over all instances in the given experiment,
`1` in this example.
