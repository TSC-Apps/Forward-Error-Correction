from collections import Counter
from numpy import array


# dekoder dekodujący bity, ktore przyszły z kanału
def decode_triple(arr):
    dec_lst = []
    lst = arr[0]
    for i in range(0, len(lst), 3):
        counter = Counter()
        for j in range(0, 3):
            counter[lst[i + j]] += 1

        # zabieg konieczny ze wzgledu na zwracanie przez most_commot listy krotek
        val, times = zip(*counter.most_common())
        dec_lst.append(val[0])
        counter.clear()

    return dec_lst


def code_triple(lst):
    return array([[i for i in lst for j in range(0, 3)]])


def ber_triple(input, output):
    wrong_bits = 0

    for i in range(len(input)):
        wrong_bits += (input[i] ^ output[i])

    return wrong_bits / len(input)
