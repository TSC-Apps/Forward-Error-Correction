from random import random
import numpy as np


def bsc(input_word, p):  #binary symmetric channel; p to prawdopodobieństwo przekłamania bitu
    output_word = []
    for bit in input_word:
        if random() < p:
            if bit == 0:
                output_word.append(1)
            else:
                output_word.append(0)
        else:
            output_word.append(bit)
    return np.array(output_word)


def bsc_mtrx(input_matrix, p):
    output_matrix = np.empty(shape = input_matrix.shape, dtype='int')
    for i in range(len(input_matrix)):
        for j in range(len(input_matrix[i])):
            if random() < p:
                if input_matrix[i][j] == 0:
                    output_matrix[i][j] = 1
                else:
                    output_matrix[i][j] = 0
            else:
                output_matrix[i][j] = input_matrix[i][j]
    return output_matrix
