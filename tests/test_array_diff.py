import numpy as np
from arc_agi.solve_coding import _array_diff


def test_array_diff_identical():
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([[1, 2], [3, 4]])
    expected = "1 2\n3 4"
    assert _array_diff(arr1, arr2) == expected


def test_array_diff_differences():
    arr1 = np.array([[1, 2], [3, 4]])
    arr2 = np.array([[1, 5], [3, 0]])
    expected = "1 2/5\n3 4/0"
    assert _array_diff(arr1, arr2) == expected


def test_array_diff_random_30x30():
    rng = np.random.default_rng(42)
    a1 = rng.integers(0, 10, size=(30, 30))
    a2 = rng.integers(0, 10, size=(30, 30))

    # Reference implementation
    rows, cols = a1.shape
    out = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if a1[i, j] == a2[i, j]:
                row.append(str(int(a1[i, j])))
            else:
                row.append(f"{int(a1[i, j])}/{int(a2[i, j])}")
        out.append(" ".join(row))
    ref_expected = "\n".join(out)

    assert _array_diff(a1, a2) == ref_expected
