import bchlib
from reed_solomon import dec_to_bin
from reed_solomon import bin_to_dec
import numpy as np
import generator
import random
import os

class BCH:
    def __init__(self, p=8219, b=16):
        self.bch_polynomial = p
        self.bch_bits = b
        self.bitflips = 0

        # utworzenie obiektu klasy z biblioteki bchlib
        self.obj = bchlib.BCH(self.bch_polynomial, self.bch_bits)

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


# BCH_POLYNOMIAL = 8219
# BCH_BITS = 160
#
# bch = BCH(BCH_POLYNOMIAL, BCH_BITS)
#
# data = generator.generate_bits(10)
# # data = list(os.urandom(10))
# print(f'\nData:                      {data}')
#
# encoded = bch.encode(data)
# print(f'Encoded (before channel):  {encoded}')
#
# decoded = bch.decode(encoded)
# print(f'Decoded:                   {decoded}')
