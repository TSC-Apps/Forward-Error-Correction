from generator import generate_bits

quantity = int(input('Podaj ilosc bitow informacji do wygenerowania: '))

arr = generate_bits(quantity)
coded_arr = []

for i in range(0, quantity):
    for j in range(0, 3):
        coded_arr.append(arr[i])
print(arr)
print(coded_arr)
