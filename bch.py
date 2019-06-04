import bchlib
from reed_solomon import dec_to_bin
from reed_solomon import bin_to_dec
import numpy as np
import generator
import random
import os

class BCH:
    def __init__(self, p, t):
        self.bch_polynomial = p
        self.bch_bits = t
        self.bitflips = 0

        # utworzenie obiektu klasy z biblioteki bchlib
        self.obj = bchlib.BCH(self.bch_polynomial, self.bch_bits)
        # self.boj = bchlib.BCH.__init__()

    def encode(self, data):
        # konwersja listy do bytearray (na potrzeby biblioteki bchlib)
        data = bytearray(data)

        # zakodowanie ciagu danych
        data_enc = self.obj.encode(data)

        # utworzenie pakietu
        packet = data + data_enc

        lst = dec_to_bin(list(packet))

        return lst

    def decode(self, packet):
        # konwersja binary -> dec
        packet = bin_to_dec(packet)

        # konwersja listy do bytearray (na potrzeby biblioteki bchlib)
        packet = bytearray(packet)

        # rozpakowanie pakietu
        data, data_enc = packet[:-self.obj.ecc_bytes], packet[-self.obj.ecc_bytes:]

        # odkodowanie
        try:
            decoded = self.obj.decode(data, data_enc)

            self.bitflips = decoded[0]
            data_dec = decoded[1]
            # data_enc = decoded[2]

            return list(data_dec)
        except:
            print('Nie udalo sie odkodowac ciagu danych.')


# BCH_BITS - t, zdolnosc korekcji bledow, liczba bitow, ktore maksymalnie mozna naprawic
# BCH_POLYNOMIAL - wielomian. Na jego podstawie wyznaczane jest automatycznie m,

BCH_POLYNOMIAL = 8219

# BCH_BITS = 10
# data = generator.generate_bits(1007)

# BCH_BITS = 50
# data = generator.generate_bits(942)

BCH_BITS = 100
data = generator.generate_bits(864)

# BCH_BITS = 200
# data = generator.generate_bits(718)

# BCH_BITS = 500
# data = generator.generate_bits(362)

# BCH_BITS = 630
# data = generator.generate_bits(297)

    # bch = BCH(BCH_POLYNOMIAL, BCH_BITS)
    #
    # print(f'\n{len(data)} Data:                      {data}')
    #
    # encoded = bch.encode(data)
    # print(f'{len(encoded)} Encoded (before channel):  {encoded}')
    #
    # decoded = bch.decode(encoded)
    # print(f'{len(decoded)} Decoded:                   {decoded}')
    #
    #
    # lenSum = 0
    #
    # for each in encoded:
    #     lenSum += len(each)
    #
    # print(f'SUM length (enc): {lenSum}')

# BCH_POLYNOMIAL = 8219
# ------+--------------+-----------------+-------------------------+-----------------------------#
#       | BCH_BITS - t | MAX_DATA_LENGTH | ENCODED_BITS            | n - k                       #
#       | zdolność     | w pojedynczym   | ilosc bitow             | liczba pozycji kontrolnych  #
#       | korekcyjna   | pakiecie        | zakodowanej informacji  |                             #
# ------+--------------+-----------------+-------------------------+-----------------------------#
# a)    | 10           | 1007            | 1120                    | 113                         #
# b)    | 50           | 942             | 1510                    | 568                         #
# c)    | 100          | 864             | 1980                    | 1116                        #
# d)    | 200          | 718             | 2870                    | 2006                        #
# e)    | 500          | 362             | 5150                    | 4788                        #
# f)    | 630          | 297             | 5680                    | 5383                        #
# ------+--------------+-----------------+-------------------------+-----------------------------#

# BCH_BITS - t, zdolnosc korekcji bledow, liczba bitow, ktore maksymalnie mozna naprawic
# MAX_DATA_LENGTH - wiadomosc dzielimy na pakiety o maksymalnie tej dlugosci
# ENCODED_LENGTH - ilosc podlist zakodowanego ciagu (useless)
# ENCODED_BITS - ilosc bitow w zakodowanym ciagu wraz z ciagiem oryginalnym
# n - k = ENCODED_BITS - MAX_DATA_LENGTH



