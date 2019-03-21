from generator import generate_bits
from decoder import decode
from coder import triple_code

quantity = int(input('Podaj ilosc bitow informacji do wygenerowania: '))

#generacja
lst = generate_bits(quantity)

#kodowanie
coded_lst = triple_code(lst)
print(lst)
print(coded_lst)

#dekodowanie
decoded_lst = decode(coded_lst)
print(decoded_lst)
