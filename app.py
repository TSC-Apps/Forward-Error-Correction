from generator import generate_bits
from triple_code import code_triple, decode_triple, ber_triple
from reed_solomon import dec_to_bin, bin_to_dec
from channels import bsc, gilbert, bsc_lists, gilbert_lists
import hamming
import unireedsolomon

quantity = int(input('Podaj ilosc bitow informacji do wygenerowania: '))

# idealny
# error_probability = 0.000096854

# dobry
# error_probability = 0.00096854

# zły
# error_probability = 0.0096854

# fatalny
# error_probability = 0.096854

# chujowy
error_probability = 0.96854

# idealny
# p_of_error_when_good, p_of_good_to_bad, p_of_error_when_bad, p_of_bad_to_good = 0.000001, 0.000101648, 0.31, 0.914789

# dobry
# p_of_error_when_good, p_of_good_to_bad, p_of_error_when_bad, p_of_bad_to_good = 0.000053513, 0.000196854, 0.65, 0.509547

# zły
# p_of_error_when_good, p_of_good_to_bad, p_of_error_when_bad, p_of_bad_to_good = 0.0003631513, 0.000396854, 0.9, 0.2768

# fatalny
# p_of_error_when_good, p_of_good_to_bad, p_of_error_when_bad, p_of_bad_to_good = 0.0003631513, 0.00496854, 0.99999, 0.04

# chujowy
p_of_error_when_good, p_of_good_to_bad, p_of_error_when_bad, p_of_bad_to_good = 0.003631513, 0.0396854, 0.99999, 0.004

print('\nKodowanie z potrajaniem\n')
# generacja
lst = generate_bits(quantity)
# print(f"Przykładowy ciąg:{lst}")

# kodowanie
coded_lst = code_triple(lst)
# print(f"Zakodowany ciąg:{coded_lst}\n")

# przepusczenie przez kanał BSC
output = bsc(coded_lst, error_probability)
# print(f"Ciąg po przejsciu przez kanał BSC: {output}")

# dekodowanie
decoded_lst = decode_triple(output)
# print(f"Odkodowany ciąg po przejściu przez kanał BSC:{decoded_lst}")
print(f"BER po przejściu przez kanał BSC: {ber_triple(lst, decoded_lst)}\n")

# przepuszczenie przez kanał Gilberta
output2 = gilbert(coded_lst, p_of_error_when_good, p_of_good_to_bad, p_of_error_when_bad, p_of_bad_to_good)
# print(f"Ciąg po przejsciu przez kanał Gilberta: {output2}")

# dekodowanie
decoded_lst2 = decode_triple(output2)
# print(f"Odkodowany ciąg po przejściu przez kanał Gilberta:{decoded_lst2}")
print(f"BER po przejściu przez kanał Gilberta: {ber_triple(lst, decoded_lst2)}")

print('\n===========================================================================')

print('\nKodowanie Hamminga\n')
# print(f"Przykładowy ciąg:{lst}")
hamming_encoded = hamming.encode(lst)
# print(f"Zakodowany ciąg: {hamming_encoded}\n")

# przepuszczenie przez kanał BSC
output_hamming = bsc(hamming_encoded, error_probability)
# print(f"Ciag po przejsciu przez kanał BSC: {output_hamming}")
hamming_decoded = hamming.decode(output_hamming)
# print(f"Odkodowany ciąg po przejściu przez kanał BSC: {hamming_decoded}")
print(f"BER po przejściu przez kanał BSC: {ber_triple(lst, hamming_decoded)}\n")

# przepuszczenie przez kanał Gilberta
output_hamming2 = gilbert(hamming_encoded, p_of_error_when_good, p_of_good_to_bad, p_of_error_when_bad,
                          p_of_bad_to_good)
# print(f"Ciag po przejsciu przez kanał Gilberta: {output_hamming2}")
hamming_decoded2 = hamming.decode(output_hamming2)
# print(f"Odkodowany ciąg po przejściu przez kanał Gilberta: {hamming_decoded2}")
print(f"BER po przejściu przez kanał Gilberta: {ber_triple(lst, hamming_decoded2)}\n")

# testy list

print('\n===========================================================================')

print('\nKodowanie BCH\n')

bch_obj = bch.BCH(8219, 160)  # bch_polynomial, bch_bits

bch_encoded = bch_obj.encode(lst)

print(f"Przykładowy ciąg:{lst}")
print(f"Zakodowany ciąg: {bch_encoded}\n")

# przepuszczenie przez kanał BSC
output_bch = bsc_lists(bch_encoded, 0.2)
print(f"Ciag po przejsciu przez kanał BSC: {output_bch}")
bch_decoded = bch_obj.decode(output_bch)
print(f"Odkodowany ciąg po przejściu przez kanał BSC: {bch_decoded}")
print(f"BER po przejściu przez kanał BSC: {ber_triple(lst, bch_decoded)}\n")

# przepuszczenie przez kanał Gilberta
output_bch2 = gilbert_lists(bch_encoded, 0.22, 0.02, 0.65, 0.55)
print(f"Ciag po przejsciu przez kanał Gilberta: {output_bch2}")
bch_decoded2 = bch_obj.decode(output_bch2)
print(f"Odkodowany ciąg po przejściu przez kanał Gilberta: {bch_decoded2}")
print(f"BER po przejściu przez kanał Gilberta: {ber_triple(lst, bch_decoded2)}\n")

#
# print('\n===========================================================================')
# print('Kodowanie Reeda-Solomona')
# print(f"Przykładowy ciąg: {lst}")
#
# rs = unireedsolomon.rs.RSCoder(255, 223)
#
# #potencjalnie tutaj mozna zmienic kodowanie
# encoded = bytearray(rs.encode(lst), 'utf-8')
#
# print(f"Zakodowany ciąg: {encoded}")
#
# prepared_for_channel = dec_to_bin(list(encoded))
#
# print(f"Zbinaryzowany zakodowany ciąg: {prepared_for_channel}")
#
# after_channel = bsc_lists(prepared_for_channel, 0.1)
#
# print(f"Zbinaryzowany ciąg po przejsciu przez kanał: {after_channel}")
#
# decoded = bin_to_dec(after_channel)
# decoded_bytearray = bytearray(decoded)
#
# print(f"Bytearray po przejsciu przez kanal: {decoded_bytearray}")
#
# #potencjalnie tutaj mozna wybrac inna opcje radzenia sobie z bledami
# decoded_string = decoded_bytearray.decode('utf-8', errors='ignore')
#
# print(f"Odkodowany string: {decoded_string}")
#
# message = rs.decode(decoded_string)
#
# print(f"Zdekodowana wiadomosc: {list(message)}")

# bit error rate danych dwoch ciagow
