import random


# prosty generator
def generate_bits(quantity):
    return [random.randint(0, 1) for i in range(0, quantity)]
