import random


# prosty generator
def generate_bits(quantity):
    lst = []
    for i in range(0, quantity):
        lst.append(random.randint(0, 1))
    return lst
