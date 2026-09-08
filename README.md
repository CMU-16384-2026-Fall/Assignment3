# Assignment3

## Checking your code before you submit

Run the local autograder on your `Robot.py` to check your forward kinematics
against the provided answers. From the `local_autograder/` folder:

```bash
cd local_autograder
python local_autograder.py
```

It auto-finds `../code/Robot.py`. You can also point it at any `Robot.py`:

```bash
python local_autograder.py path/to/Robot.py
python local_autograder.py path/to/code        # a folder that has Robot.py
```

It runs your `Robot.fk` over each test case, compares the end-effector path
against the shipped outputs within 1 cm, and prints per-chain PASS/FAIL plus an
overall result. You only need `numpy` installed.

## Test cases available to you

`local_autograder/` ships one file per chain length, each with 200 joint-angle
inputs and the reference end-effector outputs (`gt_x`, `gt_y`) for these arms:

| file | links | link lengths |
|---|---|---|
| `expected_2dof.csv` | 2 | `[0.55, 0.4]` |
| `expected_3dof.csv` | 3 | `[0.3, 0.3, 0.3]` |
| `expected_4dof.csv` | 4 | `[0.3, 0.25, 0.2, 0.15]` |
| `expected_5dof.csv` | 5 | `[0.2, 0.2, 0.2, 0.2, 0.2]` |
| `expected_6dof.csv` | 6 | `[0.2, 0.15, 0.15, 0.15, 0.1, 0.1]` |

The link lengths for each file are also on its first line (`# link_lengths=...`).

Gradescope grades the same idea but with a fresh random jitter on the joint
angles and link lengths, and more link-length configs per chain. A correct,
general `forward_kinematics` passes both; code hard-coded to these exact numbers
passes here but fails on Gradescope.
