# Local autograder — Assignment 3 (Forward Kinematics)

Check your `Robot.forward_kinematics` before you submit. This runs your `Robot.fk`
over the published test cases for every chain length (2- through 6-link) and
compares the end-effector path against the provided answers, within 1 cm.

## Files

- `local_autograder.py` — the checker. Loads your `Robot.py`, runs it, compares.
- `expected_2dof.csv` … `expected_6dof.csv` — the published test cases. Each holds
  the joint-angle inputs and the expected end-effector outputs (`gt_x`, `gt_y`)
  for one arm; the link lengths are in the first line (`# link_lengths=...`). No
  solution code here, just the answers.

## How to run

From this `local_autograder/` folder, with your code in the sibling `code/`
folder (the default in the assignment):

```bash
python local_autograder.py
```

It auto-finds `../code/Robot.py`. You can also point it at any `Robot.py`:

```bash
python local_autograder.py path/to/Robot.py
python local_autograder.py path/to/code        # a folder that has Robot.py
```

You only need `numpy` installed.

## What you'll see

```
Using .../code/Robot.py

2-link (link_lengths=[0.55, 0.4]):
  200/200 poses within 1 cm (100.0%), max error 0.00 cm  PASS
3-link (link_lengths=[0.3, 0.3, 0.3]):
  200/200 poses within 1 cm (100.0%), max error 0.00 cm  PASS
...
PASS -- your forward kinematics matches the reference on every chain.
```

A chain that FAILs prints how many poses were off and the largest error, so the
failing chain length tells you where to look in your homogeneous transforms.

## Note on Gradescope

Gradescope runs the same check with a fresh random jitter on the joint angles
and link lengths (and more link-length configs per chain). A correct, general
`forward_kinematics` passes both; code hard-coded to these exact published
numbers passes here but fails on Gradescope.
