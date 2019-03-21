from random import random


def bsc(word, p):  # binary symmetric channel; p to prawdopodobieństwo przekłamania bitu
    outputWord = []
    wrongBits = 0
    for bit in word:
        r = random()
        if (r < p and bit == 0):
            outputWord.append(1)
            wrongBits += 1
        elif (r < p and bit == 1):
            outputWord.append(0)
            wrongBits += 1
        else:
            outputWord.append(bit)
    return outputWord, wrongBits
