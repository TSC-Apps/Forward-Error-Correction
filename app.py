from generator import generate_bits
from triple_code import code_triple, decode_triple, ber_triple
from reed_solomon import dec_to_bin, bin_to_dec
from channels import bsc, gilbert, bsc_lists, gilbert_lists
import hamming
import matplotlib.pyplot as plt
import unireedsolomon
import bch

quantity_parameters = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000]

bsc_parameters = [0.000016854, 0.00016854, 0.0016854, 0.016854, 0.16854]
gilbert_parameters = [(0.000001, 0.000101648, 0.31, 0.914789), (0.000053513, 0.000196854, 0.65, 0.509547),
                      (0.0003631513, 0.000396854, 0.9, 0.2768), (0.000053513, 0.00496854, 0.9, 0.2768),
                      (0.0003631513, 0.00496854, 0.99999, 0.04), (0.0003631513, 0.00496854, 0.99999, 0.004)]

bch_obj = bch.BCH(8219, 160)  # bch_polynomial, bch_bits


# ======================================================================================================================================================
# BSC
# ======================================================================================================================================================

# for error_probability in bsc_parameters:
#     ber_list = []
#     for quantity in quantity_parameters:
#         ber_test = []
#         for i in range(10):
#             lst = generate_bits(quantity)
#             coded_lst = code_triple(lst)
#             output = bsc(coded_lst, error_probability)
#             decoded_lst = decode_triple(output)
#             ber_test.append(ber_triple(lst, decoded_lst))
#
#         ber_list.append(sum(ber_test)/len(ber_test))
#
#     plt.clf()
#     plt.plot(quantity_parameters, ber_list, label='Kodowanie potrojeniowe')
#
#     ber_list_2 = []
#     for quantity in quantity_parameters:
#         ber_test = []
#         for i in range(10):
#             lst = generate_bits(quantity)
#             hamming_encoded = hamming.encode(lst)
#             output_hamming = bsc(hamming_encoded, error_probability)
#             hamming_decoded = hamming.decode(output_hamming)
#             ber_test.append(ber_triple(lst, hamming_decoded))
#
#         ber_list_2.append(sum(ber_test)/len(ber_test))
#
#     plt.plot(quantity_parameters, ber_list_2, label='Kodowanie Hamminga')
#     plt.title('Zaleznosc BER od dlugosci wiadomosci w kanale BSC')
#     plt.xlabel('Dlugosc wiadomosci')
#     plt.ylabel('BER')
#     plt.legend()
#     plt.savefig('bsc_ber_err_prob=' + str(error_probability) + '.png')


# ======================================================================================================================================================
# Gilbert
# ======================================================================================================================================================

for parameter_list in gilbert_parameters:
    ber_list = []
    for quantity in quantity_parameters:
        ber_test = []
        for i in range(10):
            lst = generate_bits(quantity)
            coded_lst = code_triple(lst)
            output2 = gilbert(coded_lst, *parameter_list)
            decoded_lst2 = decode_triple(output2)
            ber_test.append(ber_triple(lst, decoded_lst2))

        ber_list.append(sum(ber_test)/len(ber_test))

    plt.clf()
    plt.plot(quantity_parameters, ber_list, label='Kodowanie potrojeniowe')

    ber_list_3 = []
    for quantity in quantity_parameters:
        ber_test = []
        for i in range(10):
            lst = generate_bits(quantity)
            chunks = [lst[x:x + 700] for x in range(0, len(lst), 700)]
            bch_decoded_all2 = []
            for each in chunks:
                bch_encoded2 = bch_obj.encode(each)
                bch_output2 = gilbert_lists(bch_encoded2, *parameter_list)
                bch_decoded2 = bch_obj.decode(bch_output2)
                bch_decoded_all2.append(bch_decoded2)
            bch_decoded_all_united2 = []
            for each in bch_decoded_all2:
                bch_decoded_all_united2 += each
            ber_test.append(ber_triple(lst, bch_decoded_all_united2))

        ber_list_3.append(sum(ber_test) / len(ber_test))

    plt.plot(quantity_parameters, ber_list_3, label='Kodowanie BCH')

    ber_list_2 = []
    for quantity in quantity_parameters:
        ber_test = []
        for i in range(10):
            lst = generate_bits(quantity)
            hamming_encoded = hamming.encode(lst)
            output_hamming2 = gilbert(hamming_encoded, *parameter_list)
            hamming_decoded2 = hamming.decode(output_hamming2)
            ber_test.append(ber_triple(lst, hamming_decoded2))

        ber_list_2.append(sum(ber_test)/len(ber_test))

    plt.plot(quantity_parameters, ber_list_2, label='Kodowanie Hamminga')
    plt.title('Zaleznosc BER od dlugosci wiadomosci w kanale Gilberta')
    plt.xlabel('Dlugosc wiadomosci')
    plt.ylabel('BER')
    plt.legend()
    plt.savefig('gilbert_ber_err_prob=' + str(parameter_list) + '.png')

# ======================================================================================================================================================
# Reed-Solomon
# ======================================================================================================================================================

# #
# print('\n===========================================================================')
# print('Kodowanie Reeda-Solomona')
# lst = generate_bits(100)
# print(f"Przykładowy ciąg: {lst}")
#
# rs = unireedsolomon.rs.RSCoder(255, 223)
#
# # potencjalnie tutaj mozna zmienic kodowanie
# encoded = bytearray(rs.encode(lst), 'utf-8')
#
# print(f"Zakodowany ciąg: {encoded}")
#
# prepared_for_channel = dec_to_bin(list(encoded))
#
# print(f"Zbinaryzowany zakodowany ciąg: {prepared_for_channel}")
#
# # after_channel = bsc_lists(prepared_for_channel, 0.1)
#
# # print(f"Zbinaryzowany ciąg po przejsciu przez kanał: {after_channel}")
#
# decoded = bin_to_dec(after_channel)
#
# decoded_bytearray = bytearray(decoded)
#
# print(f"Bytearray po przejsciu przez kanal: {decoded_bytearray}")
#
# message = rs.decode(decoded_bytearray)
#
# print(f"Zdekodowana wiadomosc: {list(message)}")
