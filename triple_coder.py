from numpy import array


def triple_code(lst):
    return array([i for i in lst for j in range(0, 3)])
