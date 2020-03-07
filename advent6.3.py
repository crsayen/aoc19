import string

from copy import copy

inp = []
with open('orbits2', 'r') as f:
    for line in f:
        inp.append(line.strip().split(')'))

p1 = 0
p2 = 0

orbits = {outer: inner for inner, outer in inp}
for planet in orbits.keys():
    while orbits.get(planet):
        p1 += 1
        planet = orbits.get(planet)

you = [orbits['YOU']]
while orbits.get(you[-1]):
    you.append(orbits.get(you[-1]))
san = [orbits['SAN']]
while san[-1] not in you:
    san.append(orbits.get(san[-1]))

you = you[:you.index(san[-1])+1]
p2 = len(san) + len(you) - 2

print('Part 1:', p1)
print('Part 2:', p2)