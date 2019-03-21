from generator import generate_bits


def triple_code(lst):
    coded_lst = []
    for i in lst:
        for j in range(0, 3):
            coded_lst.append(i)

    return coded_lst


quantity = int(input('Podaj ilosc bitow informacji do wygenerowania: '))

lst = generate_bits(quantity)
coded_lst = triple_code(lst)
print(lst)
print(coded_lst)
