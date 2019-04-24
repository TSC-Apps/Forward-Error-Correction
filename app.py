from generator import generate_bits
from triple_code import code_triple, decode_triple, ber_triple
from channels import bsc, gilbert, bsc_lists, gilbert_lists
import hamming
# import bch

quantity = int(input('Podaj ilosc bitow informacji do wygenerowania: '))


print('\nKodowanie z potrajaniem\n')
# generacja
lst = generate_bits(quantity)
print(f"Przykładowy ciąg:{lst}")

# kodowanie
coded_lst = code_triple(lst)
print(f"Zakodowany ciąg:{coded_lst}\n")

# przepusczenie przez kanał BSC
output = bsc(coded_lst, 0.01)
print(f"Ciąg po przejsciu przez kanał BSC: {output}")

# dekodowanie
decoded_lst = decode_triple(output)
print(f"Odkodowany ciąg po przejściu przez kanał BSC:{decoded_lst}")
print(f"BER po przejściu przez kanał BSC: {ber_triple(lst, decoded_lst)}\n")


#przepuszczenie przez kanał Gilberta
output2 = gilbert(coded_lst, 0.01, 0.02, 0.95, 0.25)
print(f"Ciąg po przejsciu przez kanał Gilberta: {output2}")

# dekodowanie
decoded_lst2 = decode_triple(output2)
print(f"Odkodowany ciąg po przejściu przez kanał Gilberta:{decoded_lst2}")
print(f"BER po przejściu przez kanał Gilberta: {ber_triple(lst, decoded_lst2)}")

print('\n===========================================================================')

print('\nKodowanie Hamminga\n')
print(f"Przykładowy ciąg:{lst}")
hamming_encoded = hamming.encode(lst)
print(f"Zakodowany ciąg: {hamming_encoded}\n")

# przepuszczenie przez kanał BSC
output_hamming = bsc(hamming_encoded, 0.01)
print(f"Ciag po przejsciu przez kanał BSC: {output_hamming}")
hamming_decoded = hamming.decode(output_hamming)
print(f"Odkodowany ciąg po przejściu przez kanał BSC: {hamming_decoded}")
print(f"BER po przejściu przez kanał BSC: {ber_triple(lst, hamming_decoded)}\n")

# przepuszczenie przez kanał Gilberta
output_hamming2 = gilbert(hamming_encoded, 0.01, 0.02, 0.95, 0.25)
print(f"Ciag po przejsciu przez kanał Gilberta: {output_hamming2}")
hamming_decoded2 = hamming.decode(output_hamming2)
print(f"Odkodowany ciąg po przejściu przez kanał Gilberta: {hamming_decoded2}")
print(f"BER po przejściu przez kanał Gilberta: {ber_triple(lst, hamming_decoded2)}\n")

# testy list
x = [[0, 1, 1], [1, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]
print(bsc_lists(x, 0.5))
print(gilbert_lists(x, 0.5, 0.5, 0.5, 0.5))


# BCH nie działa, bo generuje niebinarny ciag
# print('\n===========================================================================')
#
# print('\nKodowanie BCH\n')
#
# bch_obj = bch.BCH(8219, 16)  # bch_polynomial, bch_bits
#
# bch_encoded = bch_obj.encode(lst)
#
# print(f"Przykładowy ciąg:{lst}")
# print(f"Zakodowany ciąg: {bch_encoded}\n")
#
# # przepuszczenie przez kanał BSC
# output_bch = bsc(bch_encoded, 0.01)
# print(f"Ciag po przejsciu przez kanał BSC: {output_bch}")
# bch_decoded = bch_obj.decode(output_bch)
# print(f"Odkodowany ciąg po przejściu przez kanał BSC: {bch_decoded}")
# print(f"BER po przejściu przez kanał BSC: {ber_triple(lst, bch_decoded)}\n")
#
# # przepuszczenie przez kanał Gilberta
# output_bch2 = gilbert(bch_encoded, 0.02, 0.25)
# print(f"Ciag po przejsciu przez kanał Gilberta: {output_bch2}")
# bch_decoded2 = bch_obj.decode(output_bch2)
# print(f"Odkodowany ciąg po przejściu przez kanał Gilberta: {bch_decoded2}")
# print(f"BER po przejściu przez kanał Gilberta: {ber_triple(lst, bch_decoded2)}\n")


#bit error rate danych dwoch ciagow




