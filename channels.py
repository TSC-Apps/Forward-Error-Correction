from random import random
import numpy as np


# binary symmetric channel; p to prawdopodobieństwo przekłamania bitu

def bsc(input_array, p_of_error):
    output_array = np.empty(shape=input_array.shape, dtype='int')
    for i in range(len(input_array)):
        for j in range(len(input_array[i])):
            if random() < p_of_error:
                if input_array[i][j] == 0:
                    output_array[i][j] = 1
                else:
                    output_array[i][j] = 0
            else:
                output_array[i][j] = input_array[i][j]
    return output_array

# bsc działajacy na liście list


def bsc_lists(input_list, p_of_error):
    output_list = [[] for i in range(len(input_list))]
    for i in range(len(input_list)):
        for j in range(len(input_list[i])):
            if random() < p_of_error:
                if input_list[i][j] == 0:
                    output_list[i].append(1)
                else:
                    output_list[i].append(0)
            else:
                output_list[i].append(input_list[i][j])
    return output_list


# kanał Gilberta; p_of_good_to_bad to pr. przejścia ze stanu 'dobrego' do 'zlego', p_of_bad_to_good - pr. odwrotnego przejscia

def gilbert(input_array, p_of_error_when_good, p_of_good_to_bad, p_of_error_when_bad, p_of_bad_to_good):
    output_array = np.empty(shape=input_array.shape, dtype='int')
    good_state = True  # true oznacza stan poprawnej transmisji, false - stan przekłamań
    for i in range(len(input_array)):
        for j in range(len(input_array[i])):
            if good_state: # jestesmy w dobrym stanie
                if random() < p_of_error_when_good:
                    if input_array[i][j] == 0:
                        output_array[i][j] = 1
                    else:
                        output_array[i][j] = 0
                else:
                    output_array[i][j] = input_array[i][j]
                good_state = random() > p_of_good_to_bad
            else: # jestesmy w zlym stanie
                if random() < p_of_error_when_bad:
                    if input_array[i][j] == 0:
                        output_array[i][j] = 1
                    else:
                        output_array[i][j] = 0
                else:
                    output_array[i][j] = input_array[i][j]
                good_state = random() > (1 - p_of_bad_to_good)
    return output_array

# kanał gilberta działający na liście list


def gilbert_lists(input_list, p_of_error_when_good, p_of_good_to_bad, p_of_error_when_bad, p_of_bad_to_good):
    output_list = [[] for i in range(len(input_list))]
    good_state = True  # true oznacza stan poprawnej transmisji, false - stan przekłamań
    for i in range(len(input_list)):
        for j in range(len(input_list[i])):
            if good_state: # jestesmy w dobrym stanie
                if random() < p_of_error_when_good:
                    if input_list[i][j] == 0:
                        output_list[i].append(1)
                    else:
                        output_list[i].append(0)
                else:
                    output_list[i].append(input_list[i][j])
                good_state = random() > p_of_good_to_bad
            else: # jestesmy w zlym stanie
                if random() < p_of_error_when_bad:
                    if input_list[i][j] == 0:
                        output_list[i].append(1)
                    else:
                        output_list[i].append(0)
                else:
                    output_list[i].append(input_list[i][j])
                good_state = random() > (1 - p_of_bad_to_good)
    return output_list


