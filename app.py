from generator import generate_bits
from triple_code import code_triple, decode_triple, ber_triple
from reed_solomon import dec_to_bin, bin_to_dec
from channels import bsc, gilbert, bsc_lists, gilbert_lists
import hamming
import matplotlib.pyplot as plt
# import unireedsolomon
import bch

quantity_parameters = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000]

bsc_parameters = [0.000016854, 0.00016854, 0.0016854, 0.016854, 0.16854]
gilbert_parameters = [(0.000001, 0.000101648, 0.31, 0.914789), (0.000053513, 0.000196854, 0.65, 0.509547),
                      (0.0003631513, 0.000396854, 0.9, 0.2768), (0.000053513, 0.00496854, 0.9, 0.2768),
                      (0.0003631513, 0.00496854, 0.99999, 0.04), (0.0003631513, 0.00496854, 0.99999, 0.004)]

for parameter_list in gilbert_parameters:
    plt.clf()
    ber_list = []
    sum1, sum2, sum3, sum4, sum5, sum6 = 0, 0, 0, 0, 0, 0
    for i in range(10):
        lst = generate_bits(1000000)
        coded_lst = code_triple(lst)
        output = gilbert(coded_lst, *parameter_list)
        decoded_lst = decode_triple(output)

        #ber_list.append(ber_triple(lst, decoded_lst))
        sum1 += ber_triple(lst, decoded_lst)
        #plt.plot(ber_list, [3], label='Kodowanie potrojeniowe', marker='o')

        # ========================================================================

        ber_list = []
        hamming_encoded = hamming.encode(lst)
        output_hamming = gilbert(hamming_encoded, *parameter_list)
        hamming_decoded = hamming.decode(output_hamming)
        #ber_list.append(ber_triple(lst, hamming_decoded))
        sum2 += ber_triple(lst, hamming_decoded)
        #plt.plot(ber_list, [2], label='Kodowanie Hamminga(8, 4)', marker='o')

        # ========================================================================

        packet_size = 1007
        t = 10
        redundancy = 1120 / 1007

        ber_list = []
        chunks = [lst[x:x + packet_size] for x in range(0, len(lst), packet_size)]
        bch_decoded_all2 = []
        bch_obj = bch.BCH(8219, t)  # bch_polynomial, bch_bits
        for each in chunks:
            bch_encoded2 = bch_obj.encode(each)
            bch_output2 = gilbert_lists(bch_encoded2, *parameter_list)
            bch_decoded2 = bch_obj.decode(bch_output2)
            bch_decoded_all2.append(bch_decoded2)
        bch_decoded_all_united2 = []
        for each in bch_decoded_all2:
            bch_decoded_all_united2 += each
        #ber_list.append(ber_triple(lst, bch_decoded_all_united2))
        sum3 += ber_triple(lst, bch_decoded_all_united2)
        #plt.plot(ber_list, [redundancy], label='Kodowanie BCH(1120, 1007)', marker='o')

        # ========================================================================

        packet_size = 864
        t = 100
        redundancy = 1980 / 864

        ber_list = []
        chunks = [lst[x:x + packet_size] for x in range(0, len(lst), packet_size)]
        bch_decoded_all2 = []
        bch_obj = bch.BCH(8219, t)  # bch_polynomial, bch_bits
        for each in chunks:
            bch_encoded2 = bch_obj.encode(each)
            bch_output2 = gilbert_lists(bch_encoded2, *parameter_list)
            bch_decoded2 = bch_obj.decode(bch_output2)
            bch_decoded_all2.append(bch_decoded2)
        bch_decoded_all_united2 = []
        for each in bch_decoded_all2:
            bch_decoded_all_united2 += each
        #ber_list.append(ber_triple(lst, bch_decoded_all_united2))
        sum4 += ber_triple(lst, bch_decoded_all_united2)

        #plt.plot(ber_list, [redundancy], label='Kodowanie BCH(1980, 864)', marker='o')

        # ========================================================================

        packet_size = 942
        t = 50
        redundancy = 1510 / 942

        ber_list = []
        chunks = [lst[x:x + packet_size] for x in range(0, len(lst), packet_size)]
        bch_decoded_all2 = []
        bch_obj = bch.BCH(8219, t)  # bch_polynomial, bch_bits
        for each in chunks:
            bch_encoded2 = bch_obj.encode(each)
            bch_output2 = gilbert_lists(bch_encoded2, *parameter_list)
            bch_decoded2 = bch_obj.decode(bch_output2)
            bch_decoded_all2.append(bch_decoded2)
        bch_decoded_all_united2 = []
        for each in bch_decoded_all2:
            bch_decoded_all_united2 += each
        #ber_list.append(ber_triple(lst, bch_decoded_all_united2))
        sum5 += ber_triple(lst, bch_decoded_all_united2)

        #plt.plot(ber_list, [redundancy], label='Kodowanie BCH(1510, 1024)', marker='o')

        # ========================================================================

        packet_size = 718
        t = 200
        redundancy = 2870 / 718

        ber_list = []
        chunks = [lst[x:x + packet_size] for x in range(0, len(lst), packet_size)]
        bch_decoded_all2 = []
        bch_obj = bch.BCH(8219, t)  # bch_polynomial, bch_bits
        for each in chunks:
            bch_encoded2 = bch_obj.encode(each)
            bch_output2 = gilbert_lists(bch_encoded2, *parameter_list)
            bch_decoded2 = bch_obj.decode(bch_output2)
            bch_decoded_all2.append(bch_decoded2)
        bch_decoded_all_united2 = []
        for each in bch_decoded_all2:
            bch_decoded_all_united2 += each
        #ber_list.append(ber_triple(lst, bch_decoded_all_united2))
        sum6 += ber_triple(lst, bch_decoded_all_united2)

        #plt.plot(ber_list, [redundancy], label='Kodowanie BCH(2870, 718)', marker='o')

    # ========================================================================

    plt.plot([sum1/10], [3], label='Kodowanie potrojeniowe', marker='o')
    plt.plot([sum2/10], [2], label='Kodowanie Hamminga(8, 4)', marker='o')
    plt.plot([sum3/10], [1120 / 1007], label='Kodowanie BCH(1120, 1007)', marker='o')
    plt.plot([sum4/10], [1980 / 864], label='Kodowanie BCH(1980, 864)', marker='o')
    plt.plot([sum5/10], [1510 / 1024], label='Kodowanie BCH(1510, 1024)', marker='o')
    plt.plot([sum6/10], [2870 / 718], label='Kodowanie BCH(2870, 718)', marker='o')


    plt.title('Zestawienie nadmiarowości z BER różnych kodowań')
    plt.xlabel('BER')
    plt.ylabel('Nadmiarowość')
    plt.grid(linestyle='-', linewidth=0.5)
    plt.legend()
    plt.savefig('gilbert_ber_err_prob=' + str(parameter_list) + '.png')





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

# for parameter_list in gilbert_parameters:
#     ber_list = []
#     for quantity in quantity_parameters:
#         ber_test = []
#         for i in range(10):
#             lst = generate_bits(quantity)
#             coded_lst = code_triple(lst)
#             output2 = gilbert(coded_lst, *parameter_list)
#             decoded_lst2 = decode_triple(output2)
#             ber_test.append(ber_triple(lst, decoded_lst2))
#
#         ber_list.append(sum(ber_test)/len(ber_test))
#
#     plt.clf()
#     plt.plot(quantity_parameters, ber_list, label='Kodowanie potrojeniowe')
#
#     ber_list_3 = []
#     for quantity in quantity_parameters:
#         ber_test = []
#         for i in range(10):
#             lst = generate_bits(quantity)
#             chunks = [lst[x:x + 700] for x in range(0, len(lst), 700)]
#             bch_decoded_all2 = []
#             for each in chunks:
#                 bch_encoded2 = bch_obj.encode(each)
#                 bch_output2 = gilbert_lists(bch_encoded2, *parameter_list)
#                 bch_decoded2 = bch_obj.decode(bch_output2)
#                 bch_decoded_all2.append(bch_decoded2)
#             bch_decoded_all_united2 = []
#             for each in bch_decoded_all2:
#                 bch_decoded_all_united2 += each
#             ber_test.append(ber_triple(lst, bch_decoded_all_united2))
#
#         ber_list_3.append(sum(ber_test) / len(ber_test))
#
#     plt.plot(quantity_parameters, ber_list_3, label='Kodowanie BCH')
#
#     ber_list_2 = []
#     for quantity in quantity_parameters:
#         ber_test = []
#         for i in range(10):
#             lst = generate_bits(quantity)
#             hamming_encoded = hamming.encode(lst)
#             output_hamming2 = gilbert(hamming_encoded, *parameter_list)
#             hamming_decoded2 = hamming.decode(output_hamming2)
#             ber_test.append(ber_triple(lst, hamming_decoded2))
#
#         ber_list_2.append(sum(ber_test)/len(ber_test))
#
#     plt.plot(quantity_parameters, ber_list_2, label='Kodowanie Hamminga')
#     plt.title('Zaleznosc BER od dlugosci wiadomosci w kanale Gilberta')
#     plt.xlabel('Dlugosc wiadomosci')
#     plt.ylabel('BER')
#     plt.legend()
#     plt.savefig('gilbert_ber_err_prob=' + str(parameter_list) + '.png')

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
