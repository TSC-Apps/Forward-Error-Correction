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


def bin_to_dec(bin_matrix):
    dec_list = []

    for bin_list in bin_matrix:
        temp = [str(bin_element) for bin_element in bin_list]
        temp = ''.join(temp)
        dec_list.append(temp)
    return [int(number, 2) for number in dec_list]


rs = reedsolo.RSCodec(10)
encoded = rs.encode([1, 0, 1, 0, 1])
prepared_for_channel = dec_to_bin(list(encoded))
decoded = bin_to_dec(prepared_for_channel)

pprint.pprint(encoded)
pprint.pprint(bytearray(decoded))
