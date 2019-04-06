from random import random
import numpy as np


# binary symmetric channel; p to prawdopodobieństwo przekłamania bitu

def bsc(input_array, p):
    output_array = np.empty(shape=input_array.shape, dtype='int')
    for i in range(len(input_array)):
        for j in range(len(input_array[i])):
            if random() < p:
                if input_array[i][j] == 0:
                    output_array[i][j] = 1
                else:
                    output_array[i][j] = 0
            else:
                output_array[i][j] = input_array[i][j]
    return output_array


# kanał Gilberta; p_good_to_bad to pr. przejścia ze stanu 'dobrego' do 'zlego', p_bad_to_good - pr. odwrotnego przejscia

def gilbert(input_array, p_good_to_bad, p_bad_to_good):
    output_array = np.empty(shape=input_array.shape, dtype='int')
    good_state = True  # true oznacza stan poprawnej transmisji, false - stan przekłamań
    for i in range(len(input_array)):
        for j in range(len(input_array[i])):
            if good_state:
                output_array[i][j] = input_array[i][j]
                good_state = random() > p_good_to_bad
            else:
                if input_array[i][j] == 0:
                    output_array[i][j] = 1
                else:
                    output_array[i][j] = 0
                good_state = random() > (1 - p_bad_to_good)
    return output_array
