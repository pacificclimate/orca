def test_numpy():
    import numpy as np

    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    c = np.add(a, b)
    assert np.array_equal(c, np.array([5, 7, 9]))
