import bchlib


class BCH:
    def __init__(self, p=8219, b=16):
        self.bch_polynomial = p
        self.bch_bits = b

        # utworzenie obiektu klasy z biblioteki bchlib
        self.obj = bchlib.BCH(self.bch_polynomial, self.bch_bits)

    def encode(self, data):
        # konwersja listy do bytearray (na potrzeby biblioteki bchlib)
        data = bytearray(data)

        # zakodowanie ciagu danych
        data_enc = self.obj.encode(data)

        # utworzenie pakietu
        packet = data + data_enc
        return list(packet)

    def decode(self, packet):
        # konwersja listy do bytearray (na potrzeby biblioteki bchlib)
        packet = bytearray(packet)

        # rozpakowanie pakietu
        data, data_enc = packet[:-self.obj.ecc_bytes], packet[-self.obj.ecc_bytes:]

        # odkodowanie
        try:
            decoded = self.obj.decode(data, data_enc)

            # bitflips = decoded[0]
            # data_enc = decoded[2]
            data_dec = decoded[1]

            return list(data_dec)
        except:
            print('Nie udalo sie odkodowac ciagu danych.')


# przykladowe dzialanie:
obj = BCH(8219, 16)  # bch_polynomial, bch_bits

code = [0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0]
b_enc = obj.encode(code)
b_dec = obj.decode(b_enc)

print('\nData:      ', code)
print('Encoded packet:   ', b_enc)
print('Decoded:   ', b_dec)