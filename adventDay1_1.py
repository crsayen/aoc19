from functools import reduce
from math import floor

with open('mass', 'r') as f:
    masses = [int(l) for l in f]

fuel = reduce(
    lambda a, b: a + floor(b / 3) - 2, masses, 0
)

print(fuel)