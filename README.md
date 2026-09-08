# Assignment 3 — Forward Kinematics

Implement the forward kinematics of a planar revolute (RR…R) arm in
`code/Robot.py`. Given the link lengths and the joint angles, `Robot.fk` returns
the chain of homogeneous frames, and the end effector is the last frame. See
`assignment3.pdf` for the full writeup and the written questions.

## Folder layout

- `assignment3.tex`, `assignment3.pdf` — the writeup (source and compiled).
- `code/` — the code you work in:
  - `Robot.py` — **the file you edit and submit.** Fill in `forward_kinematics`.
  - `sample_path.py` — plots your end-effector path against the sample ground
    truth, a quick visual sanity check.
  - `create_submission.py` — packages `Robot.py` into the zip to upload.
  - `sample_ground_truth.csv` — the sample 2-link log `sample_path.py` uses.
- `local_autograder/` — the local self-check (see below).
- `latex/` — the document class and figures for the writeup.

The due date is on Canvas.

## Editing the writeup

`assignment3.tex` is the writeup source; `latex/` holds `16384_doc.cls` and the
figures. You can upload this folder to Overleaf and use `assignment3.tex` as the
project's main file.

## Working in the code

From `code/`, visualize your forward kinematics on the sample arm:

```bash
cd code
python sample_path.py
```

You need `numpy` and `matplotlib` for the plot.

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

## Submitting

From `code/`, build the upload zip and submit it to Gradescope:

```bash
cd code
python create_submission.py
```

It asks for your Andrew ID and writes `<andrewid>_hw3.zip` containing `Robot.py`.
Upload that zip to the HW3 autograder on Gradescope.
