from generator import generate_bits
from decoder import decode
from triple_coder import triple_code
from channels import bsc, gilbert
from ber import ber
import hamming

quantity = int(input('Podaj ilosc bitow informacji do wygenerowania: '))

# generacja
lst = generate_bits(quantity)
print(f"Przykładowy ciąg:{lst}")

# kodowanie
coded_lst = triple_code(lst)
print(f"Zakodowany ciąg:{coded_lst}")

# przepusczenie przez kanał
output = bsc(coded_lst, 0.2)
print(f"Ciąg po przejsciu przez kanał: {output}")

# dekodowanie
decoded_lst = decode(output)
print(f"Odkodowany ciąg:{decoded_lst}")
print(f"BER: {ber(lst, decoded_lst)}")  # BER ma sie odnosic do zakodowanej czy nie zakodowanej liczby?

print('\nKodowanie Hamminga')
print(f"Przykładowy ciąg:{lst}")
hamming_encoded = hamming.encode(lst)
print(f"Zakodowany ciąg: {hamming_encoded}")
hamming_decoded = hamming.decode(hamming_encoded)
print(f"Odkodowany ciąg: {hamming_decoded}")

