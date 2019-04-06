import bchlib
import os


class BCH:
    def __init__(self, p=8219, b=16):
        self.bch_polynomial = p
        self.bch_bits = b

        # utworzenie obiektu klasy z biblioteki bchlib
        self.obj = bchlib.BCH(self.bch_polynomial, self.bch_bits)

    def encode(self, data):
        # zakodowanie ciagu danych
        data_enc = self.obj.encode(data)

        # utworzenie pakietu
        packet = data + data_enc
        return packet

    def decode(self, packet):
        # rozpakowanie pakietu
        data, data_enc = packet[:-self.obj.ecc_bytes], packet[-self.obj.ecc_bytes:]

        # odkodowanie
        try:
            decoded = self.obj.decode(data, data_enc)
        except:
            print('Nie udalo sie odkodowac ciagu danych.')

        bitflips = decoded[0]
        data_dec = decoded[1]
        data_enc = decoded[2]

        return data_dec


# przykladowe dzialanie:
obj = BCH(8219, 16)  # bch_polynomial, bch_bits
length = 12

# wygenerowanie ciagu danych (bytearray) o odpowiedniej dlugosci
b_data = bytearray(os.urandom(length))
b_enc = obj.encode(b_data)
b_dec = obj.decode(b_enc)

# wyswietlenie w formie bytearray
print('\nData:      ', b_data)
print('Encoded:   ', b_enc)
print('Decoded:   ', b_dec)

# wyswietlenie w formie listy
print('\nData:      ', list(b_data))
print('Encoded:   ', list(b_enc))
print('Decoded:   ', list(b_dec))