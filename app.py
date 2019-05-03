from generator import generate_bits
from triple_code import code_triple, decode_triple, ber_triple
from reed_solomon import dec_to_bin, bin_to_dec
from channels import bsc, gilbert, bsc_lists, gilbert_lists
import hamming
import matplotlib.pyplot as plt
import unireedsolomon

quantity_parameters = [200000, 400000, 600000, 800000, 1000000]

bsc_parameters = [0.000096854, 0.00096854, 0.0096854, 0.096854, 0.96854]
gilbert_parameters = [(0.000001, 0.000101648, 0.31, 0.914789), (0.000053513, 0.000196854, 0.65, 0.509547),
                      (0.0003631513, 0.000396854, 0.9, 0.2768), (0.0003631513, 0.00496854, 0.99999, 0.04)]

for error_probability in bsc_parameters:
    ber_list = []
    for quantity in quantity_parameters:
        lst = generate_bits(quantity)
        coded_lst = code_triple(lst)
        output = bsc(coded_lst, error_probability)
        decoded_lst = decode_triple(output)
        ber_list.append(ber_triple(lst, decoded_lst))

    plt.clf()
    plt.plot(quantity_parameters, ber_list, label='Kodowanie potrojeniowe')

    ber_list_2 = []
    for quantity in quantity_parameters:
        lst = generate_bits(quantity)
        hamming_encoded = hamming.encode(lst)
        output_hamming = bsc(hamming_encoded, error_probability)
        hamming_decoded = hamming.decode(output_hamming)
        ber_list_2.append(ber_triple(lst, hamming_decoded))

    plt.plot(quantity_parameters, ber_list_2, label='Kodowanie Hamminga')
    plt.title('Zaleznosc BER od dlugosci wiadomosci w kanale BSC')
    plt.xlabel('Dlugosc wiadomosci')
    plt.ylabel('BER')
    plt.legend()
    plt.savefig('bsc_ber_err_prob=' + str(error_probability) + '.png')

for parameter_list in gilbert_parameters:
    ber_list = []
    for quantity in quantity_parameters:
        lst = generate_bits(quantity)
        coded_lst = code_triple(lst)
        output2 = gilbert(coded_lst, *parameter_list)
        decoded_lst2 = decode_triple(output2)
        ber_list.append(ber_triple(lst, decoded_lst2))

    plt.clf()
    plt.plot(quantity_parameters, ber_list, label='Kodowanie potrojeniowe')

    ber_list_2 = []
    for quantity in quantity_parameters:
        lst = generate_bits(quantity)
        hamming_encoded = hamming.encode(lst)
        output_hamming2 = gilbert(hamming_encoded, *parameter_list)
        hamming_decoded2 = hamming.decode(output_hamming2)
        ber_list_2.append(ber_triple(lst, hamming_decoded2))

    plt.plot(quantity_parameters, ber_list_2, label='Kodowanie Hamminga')
    plt.title('Zaleznosc BER od dlugosci wiadomosci w kanale Gilberta')
    plt.xlabel('Dlugosc wiadomosci')
    plt.ylabel('BER')
    plt.legend()
    plt.savefig('gilbert_ber_err_prob=' + str(parameter_list) + '.png')

# print('\nKodowanie BCH\n')
#
# bch_obj = bch.BCH(8219, 160)  # bch_polynomial, bch_bits
#
# bch_encoded = bch_obj.encode(lst)
#
# print(f"Przykładowy ciąg:{lst}")
# print(f"Zakodowany ciąg: {bch_encoded}\n")

# przepuszczenie przez kanał BSC
# output_bch = bsc_lists(bch_encoded, 0.2)
# print(f"Ciag po przejsciu przez kanał BSC: {output_bch}")
# bch_decoded = bch_obj.decode(output_bch)
# print(f"Odkodowany ciąg po przejściu przez kanał BSC: {bch_decoded}")
# print(f"BER po przejściu przez kanał BSC: {ber_triple(lst, bch_decoded)}\n")
#
# # przepuszczenie przez kanał Gilberta
# output_bch2 = gilbert_lists(bch_encoded, 0.22, 0.02, 0.65, 0.55)
# print(f"Ciag po przejsciu przez kanał Gilberta: {output_bch2}")
# bch_decoded2 = bch_obj.decode(output_bch2)
# print(f"Odkodowany ciąg po przejściu przez kanał Gilberta: {bch_decoded2}")
# print(f"BER po przejściu przez kanał Gilberta: {ber_triple(lst, bch_decoded2)}\n")

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
