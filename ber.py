#bit error rate danych dwoch ciagow


def ber(input, output):
    wrong_bits = 0

    for i in range(len(input)):
        wrong_bits += (input[i] ^ output[i])

    return wrong_bits/len(input)
