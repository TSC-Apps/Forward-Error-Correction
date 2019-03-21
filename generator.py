import random


def generate_bits(quantity):
    arr = []
    for i in range(0, quantity):
        arr.append(random.randint(0, 1))
    return arr
