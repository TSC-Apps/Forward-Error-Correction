from random import random
import numpy as np


def gilbert(input_word, b, g): #kanał Gilberta; # b to pr. przejścia ze stanu 'dobrego' do 'zlego', g - odwrotne przejscie
    output_word = []
    good_state = True #true oznacza stan poprawnej transmisji, false - stan przekłamań
    for bit in input_word:
        if good_state:
            output_word.append(bit)
            good_state = random() > b
        else:
            if bit == 1:
                output_word.append(0)
            else:
                output_word.append(1)
            good_state = random() > (1 - g)
    return output_word


def gilbert_mtrx(input_matrix, b, g):
    output_matrix = np.empty(shape=input_matrix.shape, dtype='int')
    good_state = True
    for i in range(len(input_matrix)):
        for j in range(len(input_matrix[i])):
            if good_state:
                output_matrix[i][j] = input_matrix[i][j]
                good_state = random() > b
            else:
                if input_matrix[i][j] == 0:
                    output_matrix[i][j] = 1
                else:
                    output_matrix[i][j] = 0
                good_state = random() > (1 - g)
    return output_matrix
