from collections import Counter


# dekoder dekodujący bity, ktore przyszły z kanału
def decode(lst):
    dec_lst = []

    for i in range(0, len(lst), 3):
        counter = Counter()
        for j in range(0, 3):
            counter[lst[i + j]] += 1

        # zabieg konieczny ze wzgledu na zwracanie przez most_commot listy krotek
        val, times = zip(*counter.most_common())
        dec_lst.append(val[0])
        counter.clear()

    return dec_lst
