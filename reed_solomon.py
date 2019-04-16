import reedsolo
import numpy as np
import pprint


def dec_to_bin(lst):
    bin_matrix = []

    # kazda wartosc ma nowy wiersz w macierzy
    for i in lst:
        bin_matrix.append(list(bin(i)[2:]))

    bin_matrix_int = [list(map(int, x)) for x in bin_matrix]
    return bin_matrix_int


rs = reedsolo.RSCodec(10)

x = dec_to_bin(list(rs.encode([1, 0, 1, 0, 1])))
y = np.array([np.array(xi) for xi in x])
pprint.pprint(np.asarray(y))
