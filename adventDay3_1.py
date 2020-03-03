dct = {
    "U": (0,1),
    "R": (1,0),
    "L": (-1,0),
    "D": (0,-1)
}

with open('wires', 'r') as f:
    wires = [
        list(map(lambda x: [dct.get(x[0]), int(x[1:])], 
        wire.split(',')
    )) for wire in f ]

points = [set(),set()]

for p, wire in enumerate(wires):
    x, y = 0 , 0
    for line in wire:
        if line[0][0]:
            for xi in range(0, line[1]):
                x+= line[0][0]
                points[p].add((x, y))
        if line[0][1]:
            for yi in range(0, line[1]):
                y+= line[0][1]
                points[p].add((x,y))

mmd = 100000
for point in points[0]:
    if point in points[1]:
        md = abs(point[0] + point[1])
        if md < mmd:
            mmd = md
print(mmd)
