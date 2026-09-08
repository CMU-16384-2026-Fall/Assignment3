"""Local self-check for Assignment 3 (Forward Kinematics).

    python local_autograder.py                # auto-finds ../code/Robot.py
    python local_autograder.py path/to/Robot.py
    python local_autograder.py path/to/code   # a folder containing Robot.py

It loads your Robot.py and runs your Robot.fk over every published test case
(2- through 6-link arms). Each expected_*.csv next to this script holds the
joint-angle inputs and the reference end-effector outputs (gt_x, gt_y) for one
arm; this compares your path against them within 1 cm and prints PASS/FAIL per
arm plus an overall result.

There is no answer key here: it only compares your output against the shipped
expected outputs. Gradescope runs the same arms with fresh random joint angles
and lightly-perturbed link lengths each run, so a correct, general
forward_kinematics passes both while code hard-coded to these exact numbers
passes here and fails there.
"""

import glob
import importlib.util
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
POINT_TOLERANCE_M = 0.01


def find_robot_py(arg):
    """Resolve a Robot.py path from an optional CLI arg, else search nearby."""
    if arg:
        if os.path.isdir(arg):
            arg = os.path.join(arg, "Robot.py")
        return arg if os.path.exists(arg) else None
    candidates = [
        os.path.join(HERE, "Robot.py"),
        os.path.join(HERE, os.pardir, "code", "Robot.py"),
        os.path.join(os.getcwd(), "Robot.py"),
        os.path.join(os.getcwd(), "code", "Robot.py"),
    ]
    for path in candidates:
        if os.path.exists(path):
            return os.path.normpath(path)
    return None


def load_robot(path):
    """Import the Robot class from a Robot.py file path."""
    folder = os.path.dirname(os.path.abspath(path))
    if folder not in sys.path:
        sys.path.insert(0, folder)     # so Robot.py's own imports resolve
    spec = importlib.util.spec_from_file_location("Robot", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Robot


def load_fixture(path):
    """(link_lengths, theta_rows, gt_xy) from an expected_*.csv.

    Line 1 is a '# link_lengths=...' comment; the rest is
    theta_0..theta_{n-1}, gt_x, gt_y.
    """
    with open(path) as f:
        first = f.readline()
    m = re.search(r"link_lengths=([-0-9.,\s]+)", first)
    if not m:
        raise ValueError(f"{os.path.basename(path)} is missing its "
                         "'# link_lengths=' header line")
    link_lengths = [float(v) for v in m.group(1).split(",") if v.strip()]
    dof = len(link_lengths)
    data = np.genfromtxt(path, delimiter=",", skip_header=2).reshape(-1, dof + 2)
    return link_lengths, data[:, 0:dof], data[:, dof:dof + 2]


def student_ee_path(RobotClass, link_lengths, theta_rows):
    """(N, 2) end-effector (x, y) from a Robot, one row per pose.

    Uses frames[0, 2, -1] / frames[1, 2, -1], exactly like sample_path.py.
    """
    ll = np.asarray(link_lengths, dtype=float).reshape(-1, 1)
    dof = ll.shape[0]
    robot = RobotClass(ll, np.ones((dof, 1)), np.ones((dof, 1)), 0)
    theta_rows = np.asarray(theta_rows, dtype=float)
    out = np.zeros((theta_rows.shape[0], 2))
    for i in range(theta_rows.shape[0]):
        frames = np.asarray(robot.fk(theta_rows[i, :].reshape(-1, 1)), dtype=float)
        out[i, 0] = frames[0, 2, -1]
        out[i, 1] = frames[1, 2, -1]
    return out


def compare_ee_paths(got, expected, tol=POINT_TOLERANCE_M):
    """(passed, total, max_error_m): how many poses land within tol of expected."""
    got = np.asarray(got, dtype=float)
    expected = np.asarray(expected, dtype=float)
    if got.shape != expected.shape or not np.all(np.isfinite(got)):
        return 0, expected.shape[0], float("inf")
    dists = np.sqrt(np.sum((got - expected) ** 2, axis=1))
    passed = int(np.count_nonzero(dists <= tol))
    return passed, len(dists), (float(dists.max()) if len(dists) else 0.0)


def main(argv):
    fixtures = sorted(glob.glob(os.path.join(HERE, "expected_*.csv")))
    if not fixtures:
        sys.exit("No expected_*.csv fixtures were found next to this script.")

    robot_path = find_robot_py(argv[1] if len(argv) > 1 else None)
    if robot_path is None:
        sys.exit("Could not find Robot.py. Pass its path:\n"
                 "    python local_autograder.py path/to/Robot.py")
    print(f"Using {robot_path}\n")
    try:
        RobotClass = load_robot(robot_path)
    except Exception as err:
        sys.exit(f"Could not import Robot.py: {err!r}")

    all_ok = True
    for path in fixtures:
        link_lengths, theta, gt_xy = load_fixture(path)
        dof = len(link_lengths)
        try:
            got = student_ee_path(RobotClass, link_lengths, theta)
        except Exception as err:
            print(f"{dof}-link (link_lengths={link_lengths}):")
            print(f"  FAIL -- forward kinematics raised {err!r}")
            all_ok = False
            continue
        passed, total, max_err = compare_ee_paths(got, gt_xy)
        pct = 100.0 * passed / total if total else 0.0
        status = "PASS" if passed == total else "FAIL"
        print(f"{dof}-link (link_lengths={link_lengths}):")
        print(f"  {passed}/{total} poses within {POINT_TOLERANCE_M * 100:.0f} cm "
              f"({pct:.1f}%), max error {max_err * 100:.2f} cm  {status}")
        all_ok = all_ok and passed == total

    print()
    if all_ok:
        print("PASS -- your forward kinematics matches the reference on every arm.")
        return 0
    print("FAIL -- some arms do not match. Check your homogeneous transforms; "
          "the failing chain length tells you where to look.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
