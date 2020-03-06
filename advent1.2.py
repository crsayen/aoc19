from functools import reduce
from math import floor

with open('mass', 'r') as f:
    masses = [int(l) for l in f]

def calcfuel(a,b):
    def f(mass, total):
        requiredfuel = floor(mass / 3) - 2
        if requiredfuel < 1:
            return total
        return f(requiredfuel, total + requiredfuel)
    return a + f(b, 0)

fuel = reduce(
    calcfuel, masses, 0
)

print(fuel)