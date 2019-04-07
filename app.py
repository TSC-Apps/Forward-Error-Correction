from generator import generate_bits
from triple_code import code_triple, decode_triple, ber_triple
from channels import bsc, gilbert
import hamming

quantity = int(input('Podaj ilosc bitow informacji do wygenerowania: '))

# generacja
lst = generate_bits(quantity)
print(f"Przykładowy ciąg:{lst}")

# kodowanie
coded_lst = code_triple(lst)
print(f"Zakodowany ciąg:{coded_lst}")

# przepusczenie przez kanał
output = bsc(coded_lst, 0.2)
print(f"Ciąg po przejsciu przez kanał: {output}")

# dekodowanie
decoded_lst = decode_triple(output)
print(f"Odkodowany ciąg:{decoded_lst}")
print(f"BER: {ber_triple(lst, decoded_lst)}")  # BER ma sie odnosic do zakodowanej czy nie zakodowanej liczby?

print('\nKodowanie Hamminga')
print(f"Przykładowy ciąg:{lst}")
hamming_encoded = hamming.encode(lst)
print(f"Zakodowany ciąg: {hamming_encoded}")
hamming_decoded = hamming.decode(hamming_encoded)
print(f"Odkodowany ciąg: {hamming_decoded}")

#bit error rate danych dwoch ciagow




