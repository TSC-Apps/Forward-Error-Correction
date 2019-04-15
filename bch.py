import bchlib
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
        return np.array(packet)

    def decode(self, packet):
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

            return np.array(data_dec)
        except:
            print('Nie udalo sie odkodowac ciagu danych.')


BCH_POLYNOMIAL = 8219
BCH_BITS = 160

bch = BCH(BCH_POLYNOMIAL, BCH_BITS)

data = generator.generate_bits(10)
# data = list(os.urandom(10))
encoded = bch.encode(data)


# TODO w zasadzie wystarczy zamieniac tylko liczby kontrolne, czyli dopiero te po dlugosci ciagu do zakodowania
def prepareForChannel(lst):
    s = ''
    for number in lst:
        a = bin(number).split('b')[1]
        if len(a) < 8:
            for _ in range(8 - len(a)):
                a = '0' + str(a)
        s += a
    l = list(s)
    l2 = []
    for each in l:
        each = int(each)
        l2.append(each)
    return np.array(l2)

print(f'\nData:                                           {data}')
print(f'Encoded (before channel):                       {list(encoded)}')
print(f'Encoded (before channel, every number 8 bits):  {list(prepareForChannel(encoded))}')


# TODO pracowac na np.ndarray


# # coś w rodzaju kanału
# def bitflip(packet):
#     byte_num = random.randint(0, len(packet) - 1)
#     bit_num = random.randint(0, 7)
#     # packet[byte_num] = packet[byte_num] ^ (1 << bit_num)     ; xor, left bitshift
#     packet[byte_num] ^= (1 << bit_num)
#
#
# # bitflip bedzie zrobiony BCH_BITS razy
# for _ in range(BCH_BITS):
#     bitflip(encoded)
#
# print(f'Encoded (after channel):   {list(encoded)}')
#
# # odkodowanie
# decoded = bch.decode(encoded)
#
# print(f'Decoded:                   {list(decoded)}')
# print(f'\nBitflips: {bch.bitflips}\n')
#
# if data == list(decoded):
#     print('Odkodowany w 100% poprawnie')
# else:
#     print('Nie udalo sie odkodować w 100% poprawnie.')


